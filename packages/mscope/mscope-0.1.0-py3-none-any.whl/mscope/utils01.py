import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor

def is_domain_reachable(domain, timeout=3):
    try:
        ip = socket.gethostbyname(domain)
        for port in (80, 443):
            try:
                with socket.create_connection((ip, port), timeout=timeout):
                    return True
            except:
                continue
        return False
    except:
        return False

def filter_reachable_domains(domains):
    reachable = []
    lock = threading.Lock()
    spinner_running = True

    def spinner():
        chars = ['|', '/', '-', '\\']
        i = 0
        while spinner_running:
            print(f"\rChecking domain availability... {chars[i % 4]}", end='', flush=True)
            i += 1
            time.sleep(0.1)

    def check(domain):
        if is_domain_reachable(domain):
            with lock:
                reachable.append(domain)

    thread = threading.Thread(target=spinner)
    thread.start()

    with ThreadPoolExecutor(max_workers=20) as exec:
        exec.map(check, domains)

    spinner_running = False
    thread.join()
    print("\nDomain check complete.\n")
    return reachable
