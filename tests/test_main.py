import os
import tempfile
from datetime import date, datetime
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from cognitive_push.main import main, run_once, should_send_at
from cognitive_push.state import DailyRecord, StateStore


VALID_CARD = """#每日认知/认知偏差

标题：为什么聪明人也会拖着错误决定不放？

1. 案例
一个人已经在错误项目上投入很多时间，于是继续投入更多资源。表面上看，他是在坚持，是在对过去的努力负责；但更深一层看，他真正不愿意面对的是“之前可能判断错了”。这个压力会让一个理性的人不断寻找继续下去的理由。

2. 关键转折
真正的转折点不是项目突然变好，而是承认损失会带来自尊压力。当他把“停止”理解成“失败”，就会把更多时间放进同一个错误选择里。

3. 认知模型
这背后是沉没成本：已经付出的成本不应该决定下一步选择。真正应该被评估的是，从今天开始继续投入，未来还能不能产生足够回报。

4. 常见误判
很多人会把继续投入理解成负责，其实只是害怕承认之前判断错了。负责不是把错误坚持到底，而是尽快停止扩大损失。

5. 迁移到你
当你迟迟不愿意停止某件事时，可以先问它未来是否仍然值得，而不是问自己过去已经投入了多少。

6. 今日一问
我现在有没有一件事，是因为已经投入太多才继续坚持？

7. 微行动
今天花 10 分钟写下一个正在消耗你的选择，并列出继续和停止的未来收益。
"""


class MainTests(TestCase):
    def test_should_send_at_configured_hour(self):
        self.assertTrue(should_send_at(datetime(2026, 6, 1, 8, 0), 8))
        self.assertFalse(should_send_at(datetime(2026, 6, 1, 7, 59), 8))

    def test_main_force_disables_send_hour_guard(self):
        with patch("cognitive_push.main.run_once") as run_once_mock:
            main(["--force"])

        run_once_mock.assert_called_once_with(enforce_send_hour=False)

    def test_main_serve_api_starts_app_api(self):
        with patch("cognitive_push.main.serve_app_api") as serve_app_api:
            main(["--serve-api"])

        serve_app_api.assert_called_once()

    def test_main_send_ios_notification_runs_scheduler(self):
        with patch("cognitive_push.main.run_ios_notification_once") as run_ios_notification_once:
            main(["--send-ios-notification"])

        run_ios_notification_once.assert_called_once()

    def test_run_once_sends_and_records_card(self):
        with tempfile.TemporaryDirectory() as directory:
            state_path = str(Path(directory) / "state.json")
            env = {
                "DEEPSEEK_API_KEY": "key",
                "DEEPSEEK_MODEL": "model",
                "PUSHPLUS_TOKEN": "https://pushplus-token",
                "FLOMO_WEBHOOK_URL": "https://flomo.example",
                "COGNITIVE_PUSH_STATE": state_path,
            }
            sent = {"pushplus": 0, "flomo": 0}

            with patch.dict(os.environ, env, clear=True):
                with patch("cognitive_push.main.generate_card", return_value=VALID_CARD):
                    with patch("cognitive_push.main.send_pushplus", side_effect=lambda url, content: sent.__setitem__("pushplus", sent["pushplus"] + 1)):
                        with patch("cognitive_push.main.send_flomo", side_effect=lambda url, content: sent.__setitem__("flomo", sent["flomo"] + 1)):
                            run_once(date(2026, 6, 1))

            self.assertEqual(sent, {"pushplus": 1, "flomo": 1})
            self.assertTrue(Path(state_path).exists())

    def test_run_once_skips_when_date_already_succeeded(self):
        with tempfile.TemporaryDirectory() as directory:
            state_path = str(Path(directory) / "state.json")
            store = StateStore(state_path)
            store.add_record(
                DailyRecord(
                    date="2026-06-01",
                    title="existing",
                    theme="#每日认知/认知偏差",
                    content=VALID_CARD,
                    pushplus_sent=True,
                    flomo_sent=True,
                )
            )
            env = {
                "DEEPSEEK_API_KEY": "key",
                "DEEPSEEK_MODEL": "model",
                "PUSHPLUS_TOKEN": "https://pushplus-token",
                "FLOMO_WEBHOOK_URL": "https://flomo.example",
                "COGNITIVE_PUSH_STATE": state_path,
            }

            with patch.dict(os.environ, env, clear=True):
                with patch("cognitive_push.main.generate_card") as generate_card:
                    run_once(date(2026, 6, 1))

            generate_card.assert_not_called()

    def test_run_once_reuses_existing_content_and_only_retries_failed_flomo(self):
        with tempfile.TemporaryDirectory() as directory:
            state_path = str(Path(directory) / "state.json")
            store = StateStore(state_path)
            store.add_record(
                DailyRecord(
                    date="2026-06-01",
                    title="existing",
                    theme="#每日认知/认知偏差",
                    content=VALID_CARD,
                    pushplus_sent=True,
                    flomo_sent=False,
                )
            )
            env = {
                "DEEPSEEK_API_KEY": "key",
                "DEEPSEEK_MODEL": "model",
                "PUSHPLUS_TOKEN": "https://pushplus-token",
                "FLOMO_WEBHOOK_URL": "https://flomo.example",
                "COGNITIVE_PUSH_STATE": state_path,
            }

            with patch.dict(os.environ, env, clear=True):
                with patch("cognitive_push.main.generate_card") as generate_card:
                    with patch("cognitive_push.main.send_pushplus") as send_pushplus:
                        with patch("cognitive_push.main.send_flomo") as send_flomo:
                            run_once(date(2026, 6, 1))

            generate_card.assert_not_called()
            send_pushplus.assert_not_called()
            send_flomo.assert_called_once()
            data = StateStore(state_path).load()
            self.assertTrue(data["records"][-1]["pushplus_sent"])
            self.assertTrue(data["records"][-1]["flomo_sent"])

    def test_run_once_respects_configured_send_hour(self):
        env = {
            "DEEPSEEK_API_KEY": "key",
            "DEEPSEEK_MODEL": "model",
            "PUSHPLUS_TOKEN": "https://pushplus-token",
            "FLOMO_WEBHOOK_URL": "https://flomo.example",
            "COGNITIVE_PUSH_SEND_HOUR": "9",
        }

        with patch.dict(os.environ, env, clear=True):
            with patch("cognitive_push.main.generate_card") as generate_card:
                with patch("builtins.print"):
                    run_once(enforce_send_hour=True, now=datetime(2026, 6, 1, 8, 0))

        generate_card.assert_not_called()

    def test_run_once_records_full_content_when_both_sends_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            state_path = str(Path(directory) / "state.json")
            env = {
                "DEEPSEEK_API_KEY": "key",
                "DEEPSEEK_MODEL": "model",
                "PUSHPLUS_TOKEN": "https://pushplus-token",
                "FLOMO_WEBHOOK_URL": "https://flomo.example",
                "COGNITIVE_PUSH_STATE": state_path,
            }

            with patch.dict(os.environ, env, clear=True):
                with patch("cognitive_push.main.generate_card", return_value=VALID_CARD):
                    with patch("cognitive_push.main.send_pushplus", side_effect=RuntimeError("pushplus failed")):
                        with patch("cognitive_push.main.send_flomo", side_effect=RuntimeError("flomo failed")):
                            with patch("cognitive_push.main.sleep"):
                                with patch("builtins.print"):
                                    with self.assertRaises(RuntimeError):
                                        run_once(date(2026, 6, 1))

            data = StateStore(state_path).load()
            self.assertEqual(data["records"][0]["content"], VALID_CARD)
            self.assertFalse(data["records"][0]["pushplus_sent"])
            self.assertFalse(data["records"][0]["flomo_sent"])
