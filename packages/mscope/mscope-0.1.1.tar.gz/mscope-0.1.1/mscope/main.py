import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from mscope.mailgen import generate_emails
from mscope.mailscan import check_email, ProgressBar
from mscope.utils01 import filter_reachable_domains
from mscope.cfgloader import load_config
from mscope.logg import print_banner

def process_username(username, domains, patterns, results):
    emails = generate_emails(username, domains, patterns)
    bar = ProgressBar(len(emails))
    valid = []

    with ThreadPoolExecutor(max_workers=10) as exec:
        futures = {exec.submit(check_email, email): email for email in emails}
        for f in as_completed(futures):
            res = f.result()
            if res:
                valid.append(res)
            bar.update()
    bar.complete()
    results[username] = valid

def main():
    print_banner()

    domains = load_config('domains.txt')
    patterns = load_config('patterns.txt')
    if not domains or not patterns:
        print("Missing domains.txt or patterns.txt")
        return

    reachable = filter_reachable_domains(domains)
    if not reachable:
        print("No reachable domains found.")
        return

    while True:
        try:
            usernames_input = input("\nEnter usernames (comma-separated, or 'exit'): ").strip().lower()
            if usernames_input in ("exit", "quit", "q"):
                break
            usernames = [u.strip() for u in usernames_input.split(',') if u.strip()]
            if not usernames:
                print("No valid usernames entered.")
                continue

            results = defaultdict(list)
            start = time.time()
            with ThreadPoolExecutor(max_workers=len(usernames)) as exec:
                futures = [exec.submit(process_username, u, reachable, patterns, results) for u in usernames]
                for f in futures: f.result()

            print("\n=== Valid Emails Found ===")
            for user in usernames:
                found = results[user]
                if found:
                    print(f"\n[{user}]")
                    for mail in sorted(found):
                        print(mail)
                else:
                    print(f"\n[{user}] No valid emails found.")

            print(f"\nScan completed in {time.time() - start:.1f} seconds.")

        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
