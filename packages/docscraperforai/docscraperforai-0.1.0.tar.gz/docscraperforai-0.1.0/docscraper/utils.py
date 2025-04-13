from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse, urljoin

def allowed_by_robots(url, user_agent='*'):
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    robots_url = urljoin(base, '/robots.txt')
    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception as e:
        return True
    return rp.can_fetch(user_agent, url)
