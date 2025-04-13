import re

def expand_pattern(pattern, username, domain):
    matches = re.findall(r"\{num(\d+)-(\d+)\}", pattern)
    if not matches:
        return [pattern.replace('{username}', username).replace('{domain}', domain)]
    
    result = []
    for match in matches:
        start, end = int(match[0]), int(match[1])
        for n in range(start, end + 1):
            p = pattern.replace(f"{{num{start}-{end}}}", str(n))
            p = p.replace('{username}', username).replace('{domain}', domain)
            result.append(p)
    return result

def generate_emails(username, domains, patterns):
    emails = []
    for domain in domains:
        for pattern in patterns:
            emails.extend(expand_pattern(pattern, username, domain))
    return emails
