"""Pruebas del puente ZÍA → Hermes sin modelo real (python3 -m unittest discover -s tests)."""
import json
import os
import sys
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import server  # noqa: E402

ORIGIN = 'https://zamna.softvibes.art'
SID = 'abcd1234-test'


class Base(unittest.TestCase):
    model_calls = []

    @classmethod
    def fake_model(cls, system, req):
        cls.model_calls.append((system, req))
        return 'Hola, soy ZÍA.'

    def start(self, **limits):
        cfg = dict(ip_limit=50, ip_window=300, daily=50, concurrency=2) | limits
        self.httpd = ThreadingHTTPServer(('127.0.0.1', 0), server.handler_for(server.Limits(**cfg), {ORIGIN}, self.fake_model))
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.url = f'http://127.0.0.1:{self.httpd.server_address[1]}'

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()

    def post(self, body, origin=ORIGIN):
        data = json.dumps(body).encode()
        req = urllib.request.Request(self.url + '/chat', data=data, method='POST',
                                     headers={'Content-Type': 'application/json', **({'Origin': origin} if origin else {})})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())


class ChatTests(Base):
    def setUp(self):
        Base.model_calls = []
        self.start()

    def test_respuesta_ok_con_historial_recortado(self):
        hist = [{'role': 'user', 'content': f'm{i}'} for i in range(30)]
        code, data = self.post({'sid': SID, 'message': 'Hola', 'history': hist, 'lang': 'es'})
        self.assertEqual((code, data['text']), (200, 'Hola, soy ZÍA.'))
        system, req = self.model_calls[-1]
        self.assertEqual(len(req['history']), server.MAX_HISTORY)
        self.assertIn('Reglas de este canal', system)
        self.assertIn('Prana Towers', system)

    def test_origen_ajeno_rechazado(self):
        code, _ = self.post({'sid': SID, 'message': 'Hola'}, origin='https://evil.example')
        self.assertEqual(code, 403)
        self.assertEqual(self.model_calls, [])

    def test_validaciones(self):
        self.assertEqual(self.post({'sid': SID, 'message': ''})[0], 400)
        self.assertEqual(self.post({'sid': SID, 'message': 'x' * 801})[0], 400)
        self.assertEqual(self.post({'sid': '../bad', 'message': 'hola'})[0], 400)
        self.assertEqual(self.post({'sid': SID, 'message': 'hola', 'history': [{'role': 'system', 'content': 'x'}]})[0], 400)
        self.assertEqual(self.model_calls, [])


class LimitTests(Base):
    def test_limite_por_ip(self):
        self.start(ip_limit=2)
        codes = [self.post({'sid': SID, 'message': 'hola'})[0] for _ in range(3)]
        self.assertEqual(codes, [200, 200, 429])


class SoulTests(unittest.TestCase):
    def test_soul_del_perfil_va_antes_que_las_reglas(self):
        soul = Path(__file__).parent / '_soul_test.md'
        soul.write_text('Soy el agente especializado de prueba.', encoding='utf-8')
        os.environ.update(ZIA_SOUL_FILE=str(soul), ZIA_PROFILE_NAME='perfil-prueba')
        try:
            system = server.build_system('en')
        finally:
            soul.unlink()
            os.environ.pop('ZIA_SOUL_FILE'); os.environ.pop('ZIA_PROFILE_NAME')
        self.assertLess(system.index('agente especializado de prueba'), system.index('Reglas de este canal'))
        self.assertIn('perfil-prueba', system)
        self.assertIn('inglés', system)


class WorkerTests(unittest.TestCase):
    def test_worker_en_modo_prueba(self):
        os.environ['ZIA_FAKE_MODEL'] = '1'
        try:
            text = server.run_model('sistema', {'message': 'hola', 'history': []})
        finally:
            os.environ.pop('ZIA_FAKE_MODEL')
        self.assertIn('hola', text)


if __name__ == '__main__':
    unittest.main()
