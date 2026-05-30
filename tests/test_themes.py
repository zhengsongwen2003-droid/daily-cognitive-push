from datetime import date
from unittest import TestCase

from cognitive_push.themes import theme_for_date


class ThemeTests(TestCase):
    def test_theme_for_monday(self):
        theme = theme_for_date(date(2026, 6, 1))
        self.assertEqual(theme.name, "决策偏误")
        self.assertIn("确认偏误", theme.examples)

    def test_theme_for_sunday_is_review(self):
        theme = theme_for_date(date(2026, 6, 7))
        self.assertEqual(theme.name, "本周复盘")
        self.assertIs(theme.is_review, True)
