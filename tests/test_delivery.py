import json
from unittest import TestCase
from unittest.mock import patch

from cognitive_push.delivery import send_flomo, send_pushplus


class _FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class DeliveryTests(TestCase):
    def test_send_pushplus_posts_token_title_and_content_payload(self):
        captured = {}

        def fake_urlopen(request, timeout):
            captured["body"] = json.loads(request.data.decode("utf-8"))
            return _FakeResponse({"code": 200})

        with patch("urllib.request.urlopen", side_effect=fake_urlopen):
            send_pushplus("token", "hello")

        self.assertEqual(captured["body"]["token"], "token")
        self.assertEqual(captured["body"]["title"], "每日认知")
        self.assertEqual(captured["body"]["content"], "hello")
        self.assertEqual(captured["body"]["template"], "markdown")

    def test_send_pushplus_raises_on_business_error(self):
        with patch("urllib.request.urlopen", return_value=_FakeResponse({"code": 500, "msg": "bad"})):
            with self.assertRaises(RuntimeError):
                send_pushplus("token", "hello")

    def test_send_flomo_posts_content_payload(self):
        captured = {}

        def fake_urlopen(request, timeout):
            captured["body"] = json.loads(request.data.decode("utf-8"))
            return _FakeResponse({})

        with patch("urllib.request.urlopen", side_effect=fake_urlopen):
            send_flomo("https://flomo.example", "hello")

        self.assertEqual(captured["body"], {"content": "hello"})

    def test_send_flomo_raises_on_business_error(self):
        with patch("urllib.request.urlopen", return_value=_FakeResponse({"errcode": 1, "errmsg": "bad"})):
            with self.assertRaises(RuntimeError):
                send_flomo("https://flomo.example", "hello")

    def test_send_flomo_raises_on_code_business_error(self):
        with patch("urllib.request.urlopen", return_value=_FakeResponse({"code": 1, "message": "bad"})):
            with self.assertRaises(RuntimeError):
                send_flomo("https://flomo.example", "hello")
