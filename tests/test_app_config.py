import os
from unittest import TestCase
from unittest.mock import patch

from cognitive_push.config import load_app_config, load_generation_config


class AppConfigTests(TestCase):
    def test_load_app_config_uses_safe_defaults(self):
        with patch.dict(os.environ, {}, clear=True):
            config = load_app_config()

        self.assertEqual(config.database_path, "data/app.sqlite3")
        self.assertEqual(config.api_host, "127.0.0.1")
        self.assertEqual(config.api_port, 8080)
        self.assertEqual(config.apns_environment, "sandbox")
        self.assertEqual(config.apns_private_key_path, "")

    def test_load_generation_config_does_not_require_pushplus(self):
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "key", "DEEPSEEK_MODEL": "deepseek-chat"}, clear=True):
            config = load_generation_config()

        self.assertEqual(config.deepseek_api_key, "key")
        self.assertEqual(config.deepseek_model, "deepseek-chat")
        self.assertEqual(config.pushplus_token, "")
