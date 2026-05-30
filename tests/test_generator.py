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
        return json.dumps({"output_text": "#每日认知/测试\n\n标题：测试标题"}).encode("utf-8")


class GeneratorTests(TestCase):
    def test_build_prompt_includes_theme_and_recent_titles(self):
        theme = Theme("决策偏误", "训练误判。", ("沉没成本",))
        prompt = build_prompt(theme, {"旧标题"})
        self.assertIn("当天主题：决策偏误", prompt)
        self.assertIn("旧标题", prompt)
        self.assertIn("必须严格使用以下结构", prompt)

    def test_generate_card_returns_output_text(self):
        config = Config(
            openai_api_key="key",
            openai_model="model",
            wecom_webhook_url="https://wecom.example",
            flomo_webhook_url="https://flomo.example",
            state_path="state.json",
            send_hour=8,
        )
        theme = Theme("决策偏误", "训练误判。", ("沉没成本",))

        with patch("urllib.request.urlopen", return_value=_FakeResponse()):
            card = generate_card(config, theme, set())

        self.assertEqual(card, "#每日认知/测试\n\n标题：测试标题")
