import re
import smtplib
import time
import threading
import dns.resolver
import sys

smtp_response_times = []
smtp_lock = threading.Lock()
mx_cache = {}
catchall_cache = {}

def is_valid_syntax(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def has_mx_record(domain):
    if domain in mx_cache:
        return mx_cache[domain]
    try:
        mx_cache[domain] = bool(dns.resolver.resolve(domain, 'MX', lifetime=10))
    except:
        mx_cache[domain] = False
    return mx_cache[domain]

def check_via_smtp(email):
    domain = email.split('@')[-1]
    if domain in catchall_cache:
        return catchall_cache[domain].get(email, False)

    start = time.time()
    try:
        mx_records = dns.resolver.resolve(domain, 'MX', lifetime=10)
        if not mx_records:
            return False
        mx_record = str(mx_records[0].exchange)
        with smtplib.SMTP(mx_record, timeout=15) as server:
            server.ehlo()
            server.mail('test@example.com')
            code, _ = server.rcpt(email)
            if code == 250:
                fake_email = f"no-such-user-{int(time.time())}@{domain}"
                fake_code, _ = server.rcpt(fake_email)
                catchall_cache[domain] = {}
                catchall_cache[domain][email] = (fake_code != 250)
                return fake_code != 250
            return False
    except Exception:
        return False
    finally:
        elapsed = time.time() - start
        with smtp_lock:
            smtp_response_times.append(elapsed)
            if len(smtp_response_times) > 100:
                smtp_response_times.pop(0)
        if len(smtp_response_times) >= 10:
            avg = sum(smtp_response_times[-10:]) / 10
            if avg > 3:
                time.sleep(10)

def check_email(email):
    if not is_valid_syntax(email):
        return None
    domain = email.split('@')[-1]
    if not has_mx_record(domain):
        return None
    if check_via_smtp(email):
        return email
    return None

class ProgressBar:
    def __init__(self, total, length=50):
        self.total = total
        self.length = length
        self.current = 0
        self.start_time = time.time()

    def update(self):
        self.current += 1
        progress = self.current / self.total
        bar = '=' * int(progress * self.length)
        spaces = ' ' * (self.length - len(bar))
        elapsed = time.time() - self.start_time
        eta = (elapsed / self.current) * (self.total - self.current) if self.current else 0
        sys.stdout.write(f"\r[ {bar}{spaces} ] {self.current}/{self.total} "
                         f"({progress:.0%}) | Elapsed: {elapsed:.1f}s | ETA: {eta:.1f}s")
        sys.stdout.flush()

    def complete(self):
        print()
