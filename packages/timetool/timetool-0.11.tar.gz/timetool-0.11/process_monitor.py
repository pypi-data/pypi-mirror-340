#!/usr/bin/env python3
"""
Process Monitor - A tool to monitor file and network access of a process

This script monitors a process and logs all file and network access events to a SQLite database.
It uses various Linux tools like strace, lsof, and tcpdump to collect the data.
"""

import argparse
import datetime
import json
import os
import re
import signal
import sqlite3
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union


class DatabaseManager:
    """Manages the SQLite database for storing process monitoring events."""

    def __init__(self, db_path: str):
        """Initialize the database manager.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._local = threading.local()
        self.init_db()

    def get_connection(self):
        """Get a thread-local database connection."""
        if not hasattr(self._local, 'conn'):
            self._local.conn = sqlite3.connect(self.db_path)
            self._local.cursor = self._local.conn.cursor()
        return self._local.conn, self._local.cursor

    def init_db(self):
        """Initialize the database and create tables if they don't exist."""
        conn, cursor = self.get_connection()

        # Create events table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            pid INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            category TEXT NOT NULL,
            details TEXT NOT NULL,
            source TEXT NOT NULL
        )
        ''')

        # Create processes table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS processes (
            pid INTEGER PRIMARY KEY,
            ppid INTEGER,
            cmd TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            exit_code INTEGER
        )
        ''')

        conn.commit()

    def log_event(self, pid: int, event_type: str, category: str, details: Dict, source: str):
        """Log an event to the database.

        Args:
            pid: Process ID
            event_type: Type of event (e.g., 'open', 'connect', 'bind')
            category: Category of event (e.g., 'file', 'network')
            details: Dictionary containing event details
            source: Source of the event (e.g., 'strace', 'lsof')
        """
        conn, cursor = self.get_connection()
        timestamp = datetime.datetime.now().isoformat()
        details_json = json.dumps(details)

        cursor.execute(
            "INSERT INTO events (timestamp, pid, event_type, category, details, source) VALUES (?, ?, ?, ?, ?, ?)",
            (timestamp, pid, event_type, category, details_json, source)
        )
        conn.commit()

    def log_process_start(self, pid: int, ppid: int, cmd: str):
        """Log process start information.

        Args:
            pid: Process ID
            ppid: Parent process ID
            cmd: Command line
        """
        conn, cursor = self.get_connection()
        timestamp = datetime.datetime.now().isoformat()

        cursor.execute(
            "INSERT OR REPLACE INTO processes (pid, ppid, cmd, start_time) VALUES (?, ?, ?, ?)",
            (pid, ppid, cmd, timestamp)
        )
        conn.commit()

    def log_process_end(self, pid: int, exit_code: int):
        """Log process end information.

        Args:
            pid: Process ID
            exit_code: Process exit code
        """
        conn, cursor = self.get_connection()
        timestamp = datetime.datetime.now().isoformat()

        cursor.execute(
            "UPDATE processes SET end_time = ?, exit_code = ? WHERE pid = ?",
            (timestamp, exit_code, pid)
        )
        conn.commit()

    def close(self):
        """Close all database connections."""
        if hasattr(self._local, 'conn'):
            self._local.conn.close()
            del self._local.conn
            del self._local.cursor


class StraceMonitor:
    """Monitors file and system call events using strace."""

    def __init__(self, db_manager: DatabaseManager, pid: int = None, cmd: List[str] = None):
        """Initialize the strace monitor.

        Args:
            db_manager: Database manager instance
            pid: Process ID to monitor (if already running)
            cmd: Command to run and monitor (if starting a new process)
        """
        self.db_manager = db_manager
        self.pid = pid
        self.cmd = cmd
        self.process = None
        self.stop_event = threading.Event()

    def _parse_strace_line(self, line: str) -> Optional[Dict]:
        """Parse a line of strace output.

        Args:
            line: Line from strace output

        Returns:
            Dictionary with parsed event information or None if not relevant
        """
        # File access patterns
        file_open_pattern = r'open\("([^"]+)", ([^)]+)\)\s+=\s+(\d+|-\d+)'
        file_read_pattern = r'read\((\d+), "[^"]*", (\d+)\)\s+=\s+(\d+|-\d+)'
        file_write_pattern = r'write\((\d+), "[^"]*", (\d+)\)\s+=\s+(\d+|-\d+)'

        # Network patterns
        connect_pattern = r'connect\((\d+), \{sa_family=([^,]+), sin_port=htons\((\d+)\), sin_addr=inet_addr\("([^"]+)"\)'
        bind_pattern = r'bind\((\d+), \{sa_family=([^,]+), sin_port=htons\((\d+)\), sin_addr=inet_addr\("([^"]+)"\)'

        # Try to match file access patterns
        match = re.search(file_open_pattern, line)
        if match:
            path, flags, result = match.groups()
            return {
                'event_type': 'open',
                'category': 'file',
                'details': {
                    'path': path,
                    'flags': flags,
                    'result': int(result) if result.isdigit() else int(result),
                },
                'source': 'strace'
            }

        match = re.search(file_read_pattern, line)
        if match:
            fd, size, result = match.groups()
            return {
                'event_type': 'read',
                'category': 'file',
                'details': {
                    'fd': int(fd),
                    'size': int(size),
                    'result': int(result) if result.isdigit() else int(result),
                },
                'source': 'strace'
            }

        match = re.search(file_write_pattern, line)
        if match:
            fd, size, result = match.groups()
            return {
                'event_type': 'write',
                'category': 'file',
                'details': {
                    'fd': int(fd),
                    'size': int(size),
                    'result': int(result) if result.isdigit() else int(result),
                },
                'source': 'strace'
            }

        # Try to match network patterns
        match = re.search(connect_pattern, line)
        if match:
            fd, family, port, addr = match.groups()
            return {
                'event_type': 'connect',
                'category': 'network',
                'details': {
                    'fd': int(fd),
                    'family': family,
                    'port': int(port),
                    'addr': addr,
                },
                'source': 'strace'
            }

        match = re.search(bind_pattern, line)
        if match:
            fd, family, port, addr = match.groups()
            return {
                'event_type': 'bind',
                'category': 'network',
                'details': {
                    'fd': int(fd),
                    'family': family,
                    'port': int(port),
                    'addr': addr,
                },
                'source': 'strace'
            }

        return None

    def start(self):
        """Start monitoring with strace."""
        if self.pid:
            cmd = ["strace", "-p", str(self.pid), "-f", "-e", "trace=file,network", "-s", "256", "-o", "-"]
        elif self.cmd:
            cmd = ["strace", "-f", "-e", "trace=file,network", "-s", "256", "-o", "-"] + self.cmd
        else:
            raise ValueError("Either pid or cmd must be provided")

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # If we're starting a new process, get its PID
        if not self.pid and self.cmd:
            self.pid = self.process.pid
            # Log the process start
            self.db_manager.log_process_start(self.pid, os.getpid(), " ".join(self.cmd))

        # Start a thread to read strace output
        threading.Thread(target=self._monitor_strace_output, daemon=True).start()

        return self.pid

    def _monitor_strace_output(self):
        """Monitor strace output and log events."""
        for line in iter(self.process.stdout.readline, ''):
            if self.stop_event.is_set():
                break

            # Extract PID from strace output
            pid_match = re.match(r'(\d+)\s+', line)
            if pid_match:
                current_pid = int(pid_match.group(1))
            else:
                current_pid = self.pid

            event = self._parse_strace_line(line)
            if event:
                self.db_manager.log_event(
                    current_pid,
                    event['event_type'],
                    event['category'],
                    event['details'],
                    event['source']
                )

    def stop(self):
        """Stop monitoring."""
        self.stop_event.set()
        if self.process:
            self.process.terminate()
            try:
                exit_code = self.process.wait(timeout=5)
                if self.cmd:  # Only log process end if we started it
                    self.db_manager.log_process_end(self.pid, exit_code)
            except subprocess.TimeoutExpired:
                self.process.kill()
                if self.cmd:
                    self.db_manager.log_process_end(self.pid, -9)


class LsofMonitor:
    """Monitors file descriptors using lsof."""

    def __init__(self, db_manager: DatabaseManager, pid: int, interval: int = 5):
        """Initialize the lsof monitor.

        Args:
            db_manager: Database manager instance
            pid: Process ID to monitor
            interval: Polling interval in seconds
        """
        self.db_manager = db_manager
        self.pid = pid
        self.interval = interval
        self.stop_event = threading.Event()
        self.thread = None

    def start(self):
        """Start monitoring with lsof."""
        self.thread = threading.Thread(target=self._monitor_lsof, daemon=True)
        self.thread.start()

    def _monitor_lsof(self):
        """Monitor file descriptors using lsof."""
        while not self.stop_event.is_set():
            try:
                # Run lsof for the process
                cmd = ["lsof", "-p", str(self.pid), "-n", "-P"]
                process = subprocess.run(cmd, capture_output=True, text=True)

                if process.returncode == 0:
                    lines = process.stdout.strip().split('\n')
                    if len(lines) > 1:  # Skip header line
                        for line in lines[1:]:
                            parts = line.split()
                            if len(parts) >= 9:
                                fd_type = parts[4]
                                name = parts[8]

                                # Determine category and event type
                                category = "unknown"
                                event_type = "open"

                                if fd_type == "REG":
                                    category = "file"
                                elif fd_type in ["IPv4", "IPv6", "sock"]:
                                    category = "network"
                                    if "->" in name:
                                        event_type = "connect"
                                    else:
                                        event_type = "bind"

                                details = {
                                    "fd": parts[3],
                                    "type": fd_type,
                                    "device": parts[5],
                                    "size": parts[6],
                                    "node": parts[7],
                                    "name": name
                                }

                                self.db_manager.log_event(
                                    self.pid,
                                    event_type,
                                    category,
                                    details,
                                    "lsof"
                                )
            except Exception as e:
                print(f"Error in lsof monitoring: {e}", file=sys.stderr)

            # Sleep for the specified interval
            for _ in range(self.interval):
                if self.stop_event.is_set():
                    break
                time.sleep(1)

    def stop(self):
        """Stop monitoring."""
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=5)


class TcpdumpMonitor:
    """Monitors network traffic using tcpdump."""

    def __init__(self, db_manager: DatabaseManager, pid: int):
        """Initialize the tcpdump monitor.

        Args:
            db_manager: Database manager instance
            pid: Process ID to monitor
        """
        self.db_manager = db_manager
        self.pid = pid
        self.process = None
        self.stop_event = threading.Event()
        self.thread = None

    def start(self):
        """Start monitoring with tcpdump."""
        # First, get the list of ports the process is using
        try:
            cmd = ["lsof", "-p", str(self.pid), "-i", "-n", "-P"]
            process = subprocess.run(cmd, capture_output=True, text=True)

            if process.returncode != 0:
                print(f"Warning: Could not get network information for PID {self.pid}", file=sys.stderr)
                return

            lines = process.stdout.strip().split('\n')
            if len(lines) <= 1:  # Only header line or empty
                print(f"No network connections found for PID {self.pid}", file=sys.stderr)
                return

            # Extract ports from lsof output
            ports = []
            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 9:
                    name = parts[8]
                    if ":" in name:
                        port = name.split(":")[-1]
                        if port.isdigit():
                            ports.append(port)

            if not ports:
                print(f"No ports found for PID {self.pid}", file=sys.stderr)
                return

            # Build tcpdump filter
            port_filter = " or ".join([f"port {port}" for port in ports])

            # Start tcpdump
            cmd = ["tcpdump", "-i", "any", "-n", "-l", port_filter]
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            # Start a thread to read tcpdump output
            self.thread = threading.Thread(target=self._monitor_tcpdump_output, daemon=True)
            self.thread.start()

        except Exception as e:
            print(f"Error starting tcpdump: {e}", file=sys.stderr)

    def _parse_tcpdump_line(self, line: str) -> Optional[Dict]:
        """Parse a line of tcpdump output.

        Args:
            line: Line from tcpdump output

        Returns:
            Dictionary with parsed event information or None if not relevant
        """
        # Basic pattern for IP traffic
        ip_pattern = r'(\d+:\d+:\d+\.\d+) IP (\S+) > (\S+): (\w+)'

        match = re.search(ip_pattern, line)
        if match:
            timestamp, src, dst, protocol = match.groups()

            # Extract IP and port
            src_parts = src.split('.')
            dst_parts = dst.split('.')

            if len(src_parts) >= 5 and len(dst_parts) >= 5:
                src_ip = '.'.join(src_parts[:4])
                src_port = src_parts[4]
                dst_ip = '.'.join(dst_parts[:4])
                dst_port = dst_parts[4]

                return {
                    'event_type': 'packet',
                    'category': 'network',
                    'details': {
                        'timestamp': timestamp,
                        'src_ip': src_ip,
                        'src_port': src_port,
                        'dst_ip': dst_ip,
                        'dst_port': dst_port,
                        'protocol': protocol
                    },
                    'source': 'tcpdump'
                }

        return None

    def _monitor_tcpdump_output(self):
        """Monitor tcpdump output and log events."""
        for line in iter(self.process.stdout.readline, ''):
            if self.stop_event.is_set():
                break

            event = self._parse_tcpdump_line(line)
            if event:
                self.db_manager.log_event(
                    self.pid,
                    event['event_type'],
                    event['category'],
                    event['details'],
                    event['source']
                )

    def stop(self):
        """Stop monitoring."""
        self.stop_event.set()
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
        if self.thread:
            self.thread.join(timeout=5)


class ProcessMonitor:
    """Main class for monitoring process behavior."""

    def __init__(self, pid: int = None, cmd: List[str] = None, db_path: str = "process_monitor.db"):
        """Initialize the process monitor.

        Args:
            pid: Process ID to monitor (if already running)
            cmd: Command to run and monitor (if starting a new process)
            db_path: Path to the SQLite database file
        """
        if pid is None and cmd is None:
            raise ValueError("Either pid or cmd must be provided")

        self.pid = pid
        self.cmd = cmd
        self.db_manager = DatabaseManager(db_path)
        self.monitors = []
        self.running = False

    def start(self):
        """Start monitoring the process."""
        if self.running:
            print("Monitoring is already running", file=sys.stderr)
            return

        # Start strace monitor
        strace_monitor = StraceMonitor(self.db_manager, self.pid, self.cmd)
        if self.pid is None:  # If we're starting a new process
            self.pid = strace_monitor.start()
        else:
            strace_monitor.start()
        self.monitors.append(strace_monitor)

        # Start lsof monitor
        lsof_monitor = LsofMonitor(self.db_manager, self.pid)
        lsof_monitor.start()
        self.monitors.append(lsof_monitor)

        # Start tcpdump monitor
        tcpdump_monitor = TcpdumpMonitor(self.db_manager, self.pid)
        tcpdump_monitor.start()
        self.monitors.append(tcpdump_monitor)

        self.running = True

        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        print(f"Monitoring process with PID {self.pid}")
        print(f"Events are being logged to {self.db_manager.db_path}")
        print("Press Ctrl+C to stop monitoring")

    def stop(self):
        """Stop monitoring the process."""
        if not self.running:
            return

        print("Stopping monitors...")
        for monitor in self.monitors:
            monitor.stop()

        self.db_manager.close()
        self.running = False
        print("Monitoring stopped")

    def _signal_handler(self, sig, frame):
        """Handle signals to stop monitoring gracefully."""
        print("\nReceived signal to stop monitoring")
        self.stop()
        sys.exit(0)


def main():
    """Main function to parse arguments and start monitoring."""
    parser = argparse.ArgumentParser(description="Monitor process behavior including file and network access")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--pid", type=int, help="PID of the process to monitor")
    group.add_argument("-c", "--command", help="Command to run and monitor")
    parser.add_argument("-d", "--database", default="process_monitor.db", help="Path to the SQLite database file")

    args = parser.parse_args()

    try:
        if args.pid:
            monitor = ProcessMonitor(pid=args.pid, db_path=args.database)
        else:
            cmd = args.command.split()
            monitor = ProcessMonitor(cmd=cmd, db_path=args.database)

        monitor.start()

        # Keep the main thread alive
        while monitor.running:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nMonitoring interrupted by user")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
    finally:
        if 'monitor' in locals():
            monitor.stop()


if __name__ == "__main__":
    main()
