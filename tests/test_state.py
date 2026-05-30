from unittest import TestCase

from cognitive_push.state import DailyRecord, StateStore


class StateStoreTests(TestCase):
    def test_state_store_starts_empty(self):
        with self.subTest("empty state"):
            import tempfile
            from pathlib import Path

            with tempfile.TemporaryDirectory() as directory:
                store = StateStore(Path(directory) / "state.json")
                self.assertEqual(store.recent_titles(), set())
                self.assertEqual(store.recent_themes(), set())

    def test_state_store_keeps_last_30_records(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / "state.json")
            for index in range(35):
                store.add_record(
                    DailyRecord(
                        date=f"2026-06-{index + 1:02d}",
                        title=f"title-{index}",
                        theme=f"theme-{index}",
                        content=f"content-{index}",
                        wecom_sent=True,
                        flomo_sent=True,
                    )
                )

            data = store.load()
            self.assertEqual(len(data["records"]), 30)
            self.assertEqual(data["records"][0]["title"], "title-5")
            self.assertIn("title-34", store.recent_titles())

    def test_state_store_detects_successful_record_for_date(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / "state.json")
            store.add_record(
                DailyRecord(
                    date="2026-06-01",
                    title="title",
                    theme="#每日认知/认知偏差",
                    content="full card",
                    wecom_sent=True,
                    flomo_sent=True,
                )
            )

            self.assertTrue(store.has_successful_record_for_date("2026-06-01"))
            self.assertFalse(store.has_successful_record_for_date("2026-06-02"))

    def test_state_store_returns_latest_record_for_date(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / "state.json")
            store.add_record(
                DailyRecord(
                    date="2026-06-01",
                    title="old",
                    theme="#每日认知/认知偏差",
                    content="old card",
                    wecom_sent=True,
                    flomo_sent=False,
                )
            )
            store.add_record(
                DailyRecord(
                    date="2026-06-01",
                    title="new",
                    theme="#每日认知/认知偏差",
                    content="new card",
                    wecom_sent=True,
                    flomo_sent=True,
                )
            )

            self.assertEqual(store.latest_record_for_date("2026-06-01")["content"], "new card")
