from unittest import TestCase

from cognitive_push.quality import validate_card


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


class QualityTests(TestCase):
    def test_valid_card_passes_quality_check(self):
        result = validate_card(VALID_CARD, recent_titles=set(), recent_themes=set())
        self.assertIs(result.ok, True)
        self.assertEqual(result.errors, [])

    def test_missing_section_fails_quality_check(self):
        result = validate_card("标题：太短", recent_titles=set(), recent_themes=set())
        self.assertIs(result.ok, False)
        self.assertTrue(any("缺少章节" in error for error in result.errors))

    def test_repeated_title_fails_quality_check(self):
        result = validate_card(VALID_CARD, recent_titles={"为什么聪明人也会拖着错误决定不放？"}, recent_themes=set())
        self.assertIs(result.ok, False)
        self.assertIn("标题最近 30 天内已出现", result.errors)

    def test_incomplete_daily_tag_fails_quality_check(self):
        card = VALID_CARD.replace("#每日认知/认知偏差", "#每日认知/")
        result = validate_card(card, recent_titles=set(), recent_themes=set())
        self.assertIs(result.ok, False)
        self.assertIn("主题标签不完整", result.errors)

    def test_question_must_be_in_today_question_section(self):
        card = VALID_CARD.replace(
            "我现在有没有一件事，是因为已经投入太多才继续坚持？",
            "我会找一个真实场景来检查这个模式。",
        )
        result = validate_card(card, recent_titles=set(), recent_themes=set())
        self.assertIs(result.ok, False)
        self.assertIn("今日一问必须包含问题", result.errors)

    def test_micro_action_must_include_10_minutes_in_own_section(self):
        card = VALID_CARD.replace(
            "今天花 10 分钟写下一个正在消耗你的选择，并列出继续和停止的未来收益。",
            "今天写下一个正在消耗你的选择，并列出继续和停止的未来收益。",
        )
        result = validate_card(card, recent_titles=set(), recent_themes=set())
        self.assertIs(result.ok, False)
        self.assertIn("微行动需要明确 10 分钟左右可完成", result.errors)

    def test_sections_must_be_in_order(self):
        card = VALID_CARD.replace("2. 关键转折", "4. 常见误判", 1)
        result = validate_card(card, recent_titles=set(), recent_themes=set())
        self.assertIs(result.ok, False)
        self.assertTrue(any("章节顺序或数量不正确" in error for error in result.errors))

    def test_bold_markdown_section_headers_are_accepted(self):
        card = VALID_CARD
        for section in ("1. 案例", "2. 关键转折", "3. 认知模型", "4. 常见误判", "5. 迁移到你", "6. 今日一问", "7. 微行动"):
            card = card.replace(section, f"**{section}**")

        result = validate_card(card, recent_titles=set(), recent_themes=set())

        self.assertIs(result.ok, True)

    def test_bold_section_names_after_number_are_accepted(self):
        card = VALID_CARD.replace("标题：为什么聪明人也会拖着错误决定不放？", "**标题：为什么聪明人也会拖着错误决定不放？**")
        for section in ("1. 案例", "2. 关键转折", "3. 认知模型", "4. 常见误判", "5. 迁移到你", "6. 今日一问", "7. 微行动"):
            number, name = section.split(". ", 1)
            card = card.replace(section, f"{number}. **{name}**")
        card = card.replace("10 分钟", "10分钟")

        result = validate_card(card, recent_titles=set(), recent_themes=set())

        self.assertIs(result.ok, True)
