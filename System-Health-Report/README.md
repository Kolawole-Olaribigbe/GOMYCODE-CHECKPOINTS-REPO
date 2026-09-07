# System Health Report

A Bash-based server health monitoring script that collects and displays
system performance metrics, network status, running services, and
process information.

## Overview

Server Performance Stats is a lightweight Linux monitoring tool built
with Bash. It provides a quick snapshot of a server's current health
without requiring a full monitoring platform.

The project was built as a hands-on DevOps/Linux project to practice
shell scripting, Linux system administration, process monitoring,
network diagnostics, and service management.

## Features

- Display hostname
- Display operating system
- Display system uptime
- Monitor CPU usage
- Monitor memory usage
- Monitor disk usage
- Display system load average
- Display top 5 CPU-consuming processes
- Display top 5 memory-consuming processes
- Count logged-in users
- Count running processes
- Display server IP address
- Test internet connectivity
- Check important system services
- Generate timestamped health reports
- Save reports to `/var/log/system_health.log`
- Warn when CPU, memory, or disk usage exceeds 80%

## Technologies Used

- Bash
- Linux
- Ubuntu
- WSL
- systemd
- Git
- GitHub

## Linux Commands Used

The project uses several standard Linux utilities:

- `top`
- `free`
- `df`
- `ps`
- `awk`
- `grep`
- `sed`
- `ip`
- `ping`
- `systemctl`
- `who`
- `uptime`

## Requirements

- Linux environment
- Bash
- systemd
- `sudo` privileges for writing to `/var/log/system_health.log`

## Installation

Clone the repository:

```bash
git clone git@github.com:Kolawole-Olaribigbe/GOMYCODE-PROJECTS-REPO.git

```

Move into the project directory:

```bash
cd server-performance-stats
```

Make the script executable:

```bash
chmod +x server-stats.sh
```

Run the script:

```bash
sudo ./server-stats.sh
```

## Usage

The script displays a server health report containing:

- System information
- CPU usage
- Memory usage
- Disk usage
- Load average
- Top CPU processes
- Top memory processes
- Logged-in users
- Process count
- IP address
- Network connectivity
- Important service status

Reports are automatically appended to:

```text
/var/log/system_health.log
```

## Example Output

```text
===================================================
Server Health Check: 2026-09-07 17:35:58
===================================================
Hostname:       Kolawole
OS:             Ubuntu 24.04.4 LTS
Uptime:         up 1 hour, 8 minutes
CPU Usage:      0.0%
Memory Usage:   13.3%
Disk Usage:     1%
Load Average:   0.00 0.00 0.00

Top 5 CPU Processes:
USER PID %CPU %MEM COMMAND
root 908 0.1 1.1 containerd
root 284 0.1 1.2 /usr/bin/containerd

Top 5 Memory Processes:
USER PID %CPU %MEM COMMAND
root 697 0.0 2.2 dockerd
root 366 0.0 2.0 /usr/bin/dockerd

Logged-in Users:  2
Process Count:  46
IP Address:      192.168.1.100
Connectivity:    Online

Important Services:
SSH:             inactive
Docker:          active
Snapd:           active
```

## Project Structure

```text
System-Health-Report/
├── server-stats.sh
└── README.md
```

## What I Learned

This project helped me practice:

- Bash functions and variables
- Conditional statements
- Command substitution
- Text processing with `awk`, `grep`, and `sed`
- Linux process monitoring
- Disk and memory monitoring
- Network diagnostics
- Linux service management with `systemctl`
- Log file management
- Running scripts with elevated privileges
- Git and GitHub workflow

## Future Improvements

Possible future improvements include:

- Add configurable warning thresholds
- Add command-line options
- Add email or Slack notifications
- Add historical performance tracking
- Add automated execution with cron or systemd timers
- Export reports in JSON format
- Integrate with Prometheus and Grafana

## Author

**Kolawole Olaribigbe**
