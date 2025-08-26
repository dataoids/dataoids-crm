from urllib.parse import urlparse
import re

def normalize_linkedin_url(url: str) -> str:
    if not url:
        return ""
    url = url.strip()
    # ensure scheme
    if url.startswith("//"):
        url = "https:" + url
    if not url.startswith("http"):
        url = "https://" + url
    # lowercase domain & path
    p = urlparse(url)
    host = p.netloc.lower()
    path = re.sub(r"/+$", "", p.path.lower())  # remove trailing slash
    # keep only /in/<slug> pattern
    m = re.match(r"^/in/[^/]+$", path)
    if not m:
        # sometimes links come as /in/<slug>/details/...
        m2 = re.match(r"^/in/([^/]+)/.*$", path)
        if m2:
            path = f"/in/{m2.group(1)}"
        else:
            return ""
    return f"https://www.linkedin.com{path}"