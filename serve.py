"""Servidor local do RETRODECK — MIME types corretos para PWA.

O `python -m http.server` padrão pode servir .js como text/plain em algumas
máquinas Windows, o que impede o registro do service worker (exige
text/javascript). Uso:  python serve.py [porta]   (padrão 8080)
"""
import http.server
import socketserver
import sys


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **getattr(http.server.SimpleHTTPRequestHandler, 'extensions_map', {}),
        '.js': 'text/javascript',
        '.mjs': 'text/javascript',
        '.webmanifest': 'application/manifest+json',
        '.json': 'application/json',
        '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon',
        '.png': 'image/png',
        '.m3u8': 'application/vnd.apple.mpegurl',
    }


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    with socketserver.TCPServer(('', port), Handler) as httpd:
        print(f'RETRODECK em http://localhost:{port}')
        httpd.serve_forever()
