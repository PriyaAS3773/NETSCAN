#!/usr/bin/env python3

import socket
import threading
import time
import argparse

from colorama import Fore, Style, init
from rich.console import Console
from rich.table import Table

# Initialize colorama
init()

# Rich console
console = Console()

# Banner
banner = f"""
{Fore.GREEN}
███╗   ██╗███████╗████████╗███████╗ ██████╗ █████╗ ███╗   ██╗
████╗  ██║██╔════╝╚══██╔══╝██╔════╝██╔════╝██╔══██╗████╗  ██║
██╔██╗ ██║█████╗     ██║   ███████╗██║     ███████║██╔██╗ ██║
██║╚██╗██║██╔══╝     ██║   ╚════██║██║     ██╔══██║██║╚██╗██║
██║ ╚████║███████╗   ██║   ███████║╚██████╗██║  ██║██║ ╚████║
╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝

        NetScan - Advanced TCP Port Scanner
{Style.RESET_ALL}
"""

print(banner)

# =========================
# Argument Parser
# =========================

parser = argparse.ArgumentParser(
    description="NetScan - Advanced TCP Port Scanner"
)

parser.add_argument(
    "targets",
    nargs='+',
    help="Target IP address or domain"
)

parser.add_argument(
    "-p",
    "--ports",
    default="1-1024",
    help="Port range example: 1-1000"
)

parser.add_argument(
    "--version",
    action="version",
    version="NetScan v1.0"
)

args = parser.parse_args()

# Parse ports
start_port, end_port = map(
    int,
    args.ports.split('-')
)

# =========================
# Multi Target Scanner
# =========================

for target in args.targets:

    open_ports = []

    try:

        target_ip = socket.gethostbyname(target)

        print(
            f"{Fore.CYAN}[+] Target:{Style.RESET_ALL} {target}"
        )

        print(
            f"{Fore.CYAN}[+] IP Address:{Style.RESET_ALL} {target_ip}"
        )

        print(
            f"{Fore.YELLOW}[+] Scanning started..."
            f"{Style.RESET_ALL}\n"
        )

        start_time = time.time()

        lock = threading.Lock()

        def scan_port(port):

            try:

                s = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                )

                s.settimeout(0.3)

                result = s.connect_ex(
                    (target_ip, port)
                )

                if result == 0:

                    try:
                        service = socket.getservbyport(port)

                    except:
                        service = "Unknown"

                    with lock:

                        open_ports.append(
                            (port, service)
                        )

                s.close()

            except:
                pass

        # Thread list
        threads = []

        # Start scanning
        for port in range(
            start_port,
            end_port + 1
        ):

            thread = threading.Thread(
                target=scan_port,
                args=(port,)
            )

            threads.append(thread)
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join()

        end_time = time.time()

        # =========================
        # Rich Table
        # =========================

        table = Table(
            title=f"NetScan Results - {target}"
        )

        table.add_column(
            "Port",
            style="cyan"
        )

        table.add_column(
            "Service",
            style="green"
        )

        table.add_column(
            "Status",
            style="red"
        )

        for port, service in open_ports:

            table.add_row(
                str(port),
                service,
                "OPEN"
            )

        console.print(table)

        # =========================
        # Summary
        # =========================

        print(
            f"\n{Fore.CYAN}"
            f"========== Scan Summary =========="
            f"{Style.RESET_ALL}"
        )

        total_ports = (
            end_port - start_port + 1
        )

        print(
            f"Total Ports Scanned : {total_ports}"
        )

        print(
            f"Open Ports Found    : "
            f"{len(open_ports)}"
        )

        print(
            f"Closed Ports        : "
            f"{total_ports - len(open_ports)}"
        )

        print(
            f"Scan Time           : "
            f"{round(end_time - start_time, 2)} seconds"
        )

        print(
            f"{Fore.CYAN}"
            f"=================================="
            f"{Style.RESET_ALL}"
        )

    # =========================
    # Error Handling
    # =========================

    except KeyboardInterrupt:

        print(
            f"\n{Fore.RED}"
            f"[!] Scan interrupted by user."
            f"{Style.RESET_ALL}"
        )

    except socket.gaierror:

        print(
            f"\n{Fore.RED}"
            f"[!] Hostname could not be resolved."
            f"{Style.RESET_ALL}"
        )

    except Exception as e:

        print(
            f"\n{Fore.RED}"
            f"[!] Error: {e}"
            f"{Style.RESET_ALL}"
        )