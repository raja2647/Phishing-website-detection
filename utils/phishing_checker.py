import hashlib
import urllib.parse

def check_url(url):
    # Get the length of the URL
    url_length = len(url)

    # Calculate SHA-256 hash of the URL
    sha_hash = hashlib.sha256(url.encode()).hexdigest()

    # Check if the URL uses HTTPS
    is_https = url.lower().startswith("https://")

    # Parse the URL to get its domain
    parsed_url = urllib.parse.urlparse(url)
    domain = parsed_url.netloc

    # Check for suspicious keywords
    suspicious_keywords = ["login", "update", "verify", "secure", "account", "bank", "credentials", "signin", "payment"]
    suspicious_tlds = ['.xyz', '.top', '.club', '.date', '.win']
    contains_keywords = any(keyword in url.lower() for keyword in suspicious_keywords)
    contains_keywords = any(keyword in url.lower() for keyword in suspicious_tlds)


    # Create a report of the URL
    result = {
        'url': url,
        'url_length': url_length,
        'sha_hash': sha_hash,
        'is_https': is_https,
        'domain': domain,
        'contains_keywords': contains_keywords,
    }

    # Determine phishing likelihood
    if "http" not in url or url_length < 10:
        result['phishing_status'] = "Suspicious"
    elif contains_keywords:
        result['phishing_status'] = "Potential Phishing"
    else:
        result['phishing_status'] = "Likely Safe"
    
    return result