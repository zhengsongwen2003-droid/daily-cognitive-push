import json
from unittest import TestCase
from unittest.mock import patch

from cognitive_push.config import Config
from cognitive_push.generator import build_prompt, generate_card
from cognitive_push.themes import Theme


class _FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return json.dumps({"choices": [{"message": {"content": "#每日认知/测试\n\n标题：测试标题"}}]}).encode("utf-8")


class GeneratorTests(TestCase):
    def test_build_prompt_includes_theme_and_recent_titles(self):
        theme = Theme("决策偏误", "训练误判。", ("沉没成本",))
        prompt = build_prompt(theme, {"旧标题"})
        self.assertIn("当天主题：决策偏误", prompt)
        self.assertIn("旧标题", prompt)
        self.assertIn("必须严格使用以下结构", prompt)

    def test_generate_card_returns_output_text(self):
        config = Config(
            deepseek_api_key="key",
            deepseek_model="deepseek-chat",
            pushplus_token="https://pushplus-token",
            flomo_webhook_url="https://flomo.example",
            state_path="state.json",
            send_hour=8,
        )
        theme = Theme("决策偏误", "训练误判。", ("沉没成本",))

        with patch("urllib.request.urlopen", return_value=_FakeResponse()):
            card = generate_card(config, theme, set())

        self.assertEqual(card, "#每日认知/测试\n\n标题：测试标题")

    def test_generate_card_calls_deepseek_chat_completions(self):
        captured = {}
        config = Config(
            deepseek_api_key="key",
            deepseek_model="deepseek-chat",
            pushplus_token="pushplus-token",
            flomo_webhook_url="https://flomo.example",
            state_path="state.json",
            send_hour=8,
        )
        theme = Theme("决策偏误", "训练误判。", ("沉没成本",))

        def fake_urlopen(request, timeout):
            captured["url"] = request.full_url
            captured["body"] = json.loads(request.data.decode("utf-8"))
            captured["auth"] = request.headers["Authorization"]
            return _FakeResponse()

        with patch("urllib.request.urlopen", side_effect=fake_urlopen):
            generate_card(config, theme, set())

        self.assertEqual(captured["url"], "https://api.deepseek.com/chat/completions")
        self.assertEqual(captured["body"]["model"], "deepseek-chat")
        self.assertEqual(captured["body"]["messages"][0]["role"], "user")
        self.assertEqual(captured["auth"], "Bearer key")
