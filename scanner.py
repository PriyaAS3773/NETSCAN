import socket
import threading
import time

# ==============================
# NetScan - Fast TCP Port Scanner
# ==============================

print("=" * 60)
print("          NetScan - Fast TCP Port Scanner")
print("=" * 60)

# Get target
target = input("Enter Target Website or IP: ")

try:
    # Convert domain to IP
    target_ip = socket.gethostbyname(target)

    print(f"\nTarget IP: {target_ip}")
    print("-" * 60)

    # Start timer
    start_time = time.time()

    # Open ports list
    open_ports = []

    # Function to scan a single port
    def scan_port(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Faster timeout
            s.settimeout(0.3)

            result = s.connect_ex((target_ip, port))

            if result == 0:

                try:
                    service = socket.getservbyport(port)
                except:
                    service = "Unknown"

                print(f"[OPEN] Port {port} - {service}")

                open_ports.append((port, service))

            s.close()

        except:
            pass

    # Create threads
    threads = []

    # Scan common ports only (much faster)
    common_ports = [
        20, 21, 22, 23, 25, 53, 67, 68, 69,
        80, 110, 111, 119, 123, 135, 137,
        138, 139, 143, 161, 389, 443, 445,
        465, 587, 993, 995, 1433, 1521,
        1723, 3306, 3389, 5432, 5900,
        8080, 8443
    ]

    # Start scanning
    for port in common_ports:

        thread = threading.Thread(target=scan_port, args=(port,))
        threads.append(thread)
        thread.start()

    # Wait for all threads
    for thread in threads:
        thread.join()

    # End timer
    end_time = time.time()

    # ==============================
    # Final Report
    # ==============================

    print("\n" + "=" * 60)
    print("                Scan Report")
    print("=" * 60)

    if open_ports:

        print(f"\nTotal Open Ports Found: {len(open_ports)}\n")

        for port, service in sorted(open_ports):
            print(f"Port {port:<5} | Service: {service}")

    else:
        print("\nNo open common ports found.")

    print("\n" + "-" * 60)
    print(f"Scan Completed in {end_time - start_time:.2f} seconds")
    print("-" * 60)

    # Save results to file
    save = input("\nDo you want to save the report? (y/n): ")

    if save.lower() == 'y':

        filename = "scan_report.txt"

        with open(filename, "w") as file:

            file.write("NetScan - Port Scan Report\n")
            file.write("=" * 50 + "\n")
            file.write(f"Target: {target}\n")
            file.write(f"IP Address: {target_ip}\n\n")

            if open_ports:

                for port, service in sorted(open_ports):
                    file.write(f"Port {port} - {service}\n")

            else:
                file.write("No open ports found.\n")

            file.write(f"\nScan Time: {end_time - start_time:.2f} seconds\n")

        print(f"\nReport saved as '{filename}'")

# ==============================
# Error Handling
# ==============================

except socket.gaierror:
    print("\n[ERROR] Hostname could not be resolved.")

except KeyboardInterrupt:
    print("\n[INFO] Scan interrupted by user.")

except Exception as e:
    print(f"\n[ERROR] {e}")