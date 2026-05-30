# Daily Cognitive WeChat + flomo Design

## Goal

Build a daily cognitive training system that sends one 3-5 minute case-based reflection to the user each day, then saves the same content into flomo for long-term review.

The system should help the user improve judgment through examples, not just receive motivational content. Each message should teach one transferable decision-making pattern and end with a concrete question or small action.

## Recommended Product Shape

Use a lightweight automation that runs every morning, generates one cognitive training card, sends it to a WeChat-facing channel, and archives it in flomo.

Recommended delivery path:

1. A scheduled task runs every day at 08:00.
2. The system selects that day's theme.
3. AI generates a 3-5 minute case card.
4. A quality check verifies structure, usefulness, and non-repetition.
5. The card is sent to WeChat through a stable channel.
6. The same card is saved to flomo through flomo's API or incoming webhook.
7. The selected theme and title are recorded to reduce repetition.

## WeChat And flomo Roles

WeChat should be the reminder and reading surface. It creates the daily trigger to read.

flomo should be the knowledge archive. It stores every daily card with tags so the user can search, review, and build a personal cognitive library over time.

The recommended first implementation is Enterprise WeChat group bot plus flomo API. This is more stable than trying to automate direct personal WeChat messages.

## Daily Content Format

Each daily card should follow this structure:

```text
#每日认知/主题标签

标题：具体、有冲突感

1. 案例
一个商业、职场、关系、历史或个人选择案例。

2. 关键转折
当事人在什么压力、诱惑或信息不完整的情况下做了选择。

3. 认知模型
解释背后的思维模型，比如沉没成本、损失厌恶、二阶思维、机会成本、激励错位。

4. 常见误判
普通人在类似处境中最容易怎么想错。

5. 迁移到你
把案例映射到工作、赚钱、关系、选择、学习等现实场景。

6. 今日一问
一个让用户联系自己现实处境的问题。

7. 微行动
今天可以做的一件小事，最好 10 分钟内能完成。
```

## Weekly Theme Rotation

Use a weekly rhythm so the content stays varied:

```text
Monday: decision bias
Tuesday: long-term thinking and compounding
Wednesday: human nature and relationships
Thursday: business or product case
Friday: workplace and management judgment
Saturday: history, investing, or social case
Sunday: weekly review
```

Sunday should not introduce a new case by default. It should summarize the week:

```text
本周你训练了哪些判断力
出现最多的认知模型是什么
哪一个问题最值得继续想
下周建议关注哪个主题
```

## flomo Tags

Use consistent tags so cards become searchable:

```text
#每日认知
#认知偏差
#人生决策
#长期主义
#商业案例
#本周复盘
```

Each card should include `#每日认知` plus one or two specific tags.

## Content Quality Rules

Each generated card must pass these rules before sending:

1. It contains all seven required sections.
2. It can be read in roughly 3-5 minutes.
3. It explains one main cognitive model, not several unrelated ideas.
4. It avoids generic motivational language.
5. It includes a concrete "今日一问".
6. It includes a micro-action the user can complete in about 10 minutes.
7. It does not repeat a theme or title from the last 30 days.

## Minimal Viable Version

The first version should do only the essential workflow:

1. Run once per day at 08:00.
2. Generate one daily cognitive card.
3. Send the card to Enterprise WeChat.
4. Save the card to flomo.
5. Store the last 30 days of titles and themes.
6. Retry failed sends up to two times.

This version does not need a web dashboard, manual editing queue, analytics, or account system.

## Error Handling

If content generation fails, the system should retry once with the same theme.

If WeChat sending fails, the system should retry up to two times and save the failure status.

If flomo saving fails, the system should still send to WeChat and retry flomo saving later.

If both WeChat and flomo fail, the generated card should be saved locally so it is not lost.

## Future Improvements

After the minimal version is stable, add:

1. Weekly flomo review summaries.
2. A feedback command such as "more like this" or "less like this".
3. Theme weighting based on the user's preferred topics.
4. A small local archive for searching past cards.
5. Optional manual approval before sending.

## Open Decisions

Before implementation, confirm:

1. Whether the first WeChat channel will be Enterprise WeChat bot or another delivery path.
2. The exact daily send time.
3. Whether cards should be generated from general knowledge or from a curated source list.
4. Whether the flomo webhook/API endpoint is already available.
