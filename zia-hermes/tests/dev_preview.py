"""Vista previa local: sirve ../sitio y conecta /api/zia/chat al puente con modelo falso.
Uso: python3 tests/dev_preview.py  → http://127.0.0.1:8792/zia/?abrir"""
import functools, os, sys, threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['ZIA_FAKE_MODEL'] = '1'
import server
ORIGIN = 'http://127.0.0.1:8792'
Api = server.handler_for(server.Limits(50, 300, 200, 2), {ORIGIN})
class H(SimpleHTTPRequestHandler):
    def do_POST(self):
        Api.do_POST(self)
    reply = Api.reply
    def log_message(self, *a): pass
ThreadingHTTPServer(('127.0.0.1', 8792), functools.partial(H, directory=str(ROOT.parent / 'sitio'))).serve_forever()
