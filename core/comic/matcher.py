import re

def match_comic(comic):
    comic = comic.strip()
    if comic.isdigit(): # id
        return int(comic)
    pattern = r'^(?:https?://)?(?:www\.)?xkcd\.com/(\d+)/?$' # url
    match = re.match(pattern, comic)
    if match:
        return int(match.group(1))
    return None # invalid