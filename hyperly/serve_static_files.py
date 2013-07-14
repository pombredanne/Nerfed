import os
from http_parser.parser import HttpParser

ROOT = os.path.dirname(os.path.abspath(__file__))


def proxy(data):
    parser = HttpParser(0)
    parser.execute(data, len(data))
    path = parser.get_path()
    if path.startswith('/static'):
        path = os.path.join(ROOT, path[1:])
        if os.path.exists(path):
            fno = os.open(path, os.O_RDONLY)
            return {
                "file": fno,
                "reply": "HTTP/1.1 200 OK\r\n\r\n"
            }
        else:
            return {
                "close": True
            }
    return {
        "close": True
    }
