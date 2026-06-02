const cards = [
  {
    title: "沉没成本：为什么越亏越舍不得停",
    theme: "决策偏误",
    tags: ["沉没成本", "止损", "选择"],
    caseText: "你已经为一个项目投入了三周，结果越来越像一个无底洞。继续做，是为了未来收益，还是只是不想承认过去的投入已经无法追回？",
    modelText: "沉没成本是已经发生且无法收回的投入。更好的判断方式，是只看从现在开始继续投入能带来什么，而不是过去已经花掉了什么。",
    mistakeText: "把“我已经付出很多”误当成“我应该继续”。真正需要比较的是继续、暂停、转向三种选择的未来收益和机会成本。",
    questionText: "我现在坚持的一件事，是因为它仍然有未来价值，还是因为我不想承认过去判断错了？",
    actionText: "花 10 分钟写下一个正在消耗你的选择，并列出继续与停止各自的未来收益。"
  },
  {
    title: "二阶思维：先问下一步会发生什么",
    theme: "长期主义",
    tags: ["二阶思维", "复利", "延迟满足"],
    caseText: "一个立刻舒服的选择，常常会在几周后制造更大的麻烦。一个短期费力的选择，也可能在未来帮你省下大量重复劳动。",
    modelText: "二阶思维要求你不要停在第一层结果，而是继续追问：这个结果会带来什么新的行为、关系和限制？",
    mistakeText: "只被即时反馈牵着走。比如只看今天是否轻松，却忽略这个选择会让明天更自由还是更被动。",
    questionText: "我今天最想快速解决的一件事，它的第二层后果是什么？",
    actionText: "用 10 分钟画两列：立刻结果、两周后的结果。只分析一个选择。"
  },
  {
    title: "边界感：善意不等于无限承担",
    theme: "人性与关系",
    tags: ["边界", "互惠", "关系"],
    caseText: "你答应帮一个人收拾烂摊子，第一次是情分，第二次成了默认，第三次你已经开始怨气上来。",
    modelText: "健康关系需要互惠和边界。边界不是冷漠，而是让责任回到该承担的人身上。",
    mistakeText: "把拒绝理解成伤害别人，于是用过度承担换取短暂和平，最后反而损耗关系。",
    questionText: "我最近哪一次答应，其实是在害怕冲突，而不是出于真正愿意？",
    actionText: "花 10 分钟写一句温和但清楚的边界表达，今天只练习这一句。"
  },
  {
    title: "激励错位：指标好看不等于事情变好",
    theme: "商业与产品",
    tags: ["激励", "指标", "产品判断"],
    caseText: "团队开始追一个数字后，所有动作都围着数字转。数字上去了，用户体验却变差了。",
    modelText: "指标会塑造行为。一个好指标应该逼近真实目标，而不是诱导人们优化表面结果。",
    mistakeText: "把可测量的东西当成真正重要的东西。越容易统计的指标，越需要警惕它是否只是替身。",
    questionText: "我现在追的一个数字，真的代表进步吗，还是只是更容易被看见？",
    actionText: "用 10 分钟给一个目标补一句反指标：如果这个数字变好但什么变坏，就说明跑偏了。"
  },
  {
    title: "反馈循环：你得到什么，就会重复什么",
    theme: "职场与管理",
    tags: ["反馈", "协作", "管理"],
    caseText: "一个人每次救火都被表扬，于是系统越来越依赖救火，而不是奖励提前预防的人。",
    modelText: "组织会重复被奖励的行为。想改变结果，先看奖励、惩罚和注意力流向哪里。",
    mistakeText: "只批评个人不够主动，却没有检查环境是不是正在奖励短期表现、忽视长期建设。",
    questionText: "我所在的环境正在奖励哪一种行为，即使嘴上说想要另一种？",
    actionText: "花 10 分钟写下一个你想鼓励的行为，并给它设计一次具体、及时的正反馈。"
  },
  {
    title: "安全边际：别把刚好够用当成安全",
    theme: "风险判断",
    tags: ["安全边际", "周期", "风险"],
    caseText: "计划在正常天气下刚好赶上，预算在正常支出下刚好够用，情绪在正常压力下刚好稳住。问题是，现实很少一直正常。",
    modelText: "安全边际是在不确定世界里给自己留余地。它不是保守，而是承认预测会错。",
    mistakeText: "把理想条件下可行，当成真实条件下可靠。越重要的事情，越不能只按平均情况设计。",
    questionText: "我最近哪件事只在一切顺利时才成立？",
    actionText: "用 10 分钟给这件事加一个缓冲：时间、钱、精力或备用方案任选其一。"
  },
  {
    title: "周复盘：找出本周最常出现的判断模式",
    theme: "本周复盘",
    tags: ["复盘", "模式识别", "下周方向"],
    caseText: "复盘不是给自己打分，而是从一周的选择里找重复模式。重复出现的问题，往往比单次失误更值得处理。",
    modelText: "模式识别能让你从事件层上升到系统层。不要只问这次发生了什么，也要问它为什么总以相似方式发生。",
    mistakeText: "复盘时只记流水账，或者只责怪自己。更有用的是找到一个下周可以改变的小杠杆。",
    questionText: "本周我在哪一种场景下最容易判断失真？",
    actionText: "花 10 分钟选出本周一个重复模式，并给下周设置一个提前提醒。"
  }
];

const storageKey = "daily-cognitive-web-state";
const todayKey = new Date().toISOString().slice(0, 10);
const els = {
  streakDays: document.querySelector("#streakDays"),
  todayDate: document.querySelector("#todayDate"),
  cardTitle: document.querySelector("#cardTitle"),
  themeStrip: document.querySelector("#themeStrip"),
  caseText: document.querySelector("#caseText"),
  modelText: document.querySelector("#modelText"),
  mistakeText: document.querySelector("#mistakeText"),
  questionText: document.querySelector("#questionText"),
  actionText: document.querySelector("#actionText"),
  reflectionInput: document.querySelector("#reflectionInput"),
  saveReflection: document.querySelector("#saveReflection"),
  completeAction: document.querySelector("#completeAction"),
  prevCard: document.querySelector("#prevCard"),
  nextCard: document.querySelector("#nextCard"),
  doneCount: document.querySelector("#doneCount"),
  reviewGrid: document.querySelector("#reviewGrid"),
  historyList: document.querySelector("#historyList"),
  clearHistory: document.querySelector("#clearHistory"),
  toast: document.querySelector("#toast")
};

let state = loadState();
let cardIndex = new Date().getDay();

function loadState() {
  try {
    return JSON.parse(localStorage.getItem(storageKey)) || { records: [] };
  } catch {
    return { records: [] };
  }
}

function saveState() {
  localStorage.setItem(storageKey, JSON.stringify(state));
}

function currentCard() {
  return cards[cardIndex % cards.length];
}

function renderToday() {
  const card = currentCard();
  const record = state.records.find((item) => item.date === todayKey && item.title === card.title);
  els.todayDate.textContent = new Intl.DateTimeFormat("zh-CN", {
    month: "long",
    day: "numeric",
    weekday: "long"
  }).format(new Date());
  els.cardTitle.textContent = card.title;
  els.themeStrip.innerHTML = [card.theme, ...card.tags]
    .map((tag) => `<span class="theme-chip">${tag}</span>`)
    .join("");
  els.caseText.textContent = card.caseText;
  els.modelText.textContent = card.modelText;
  els.mistakeText.textContent = card.mistakeText;
  els.questionText.textContent = card.questionText;
  els.actionText.textContent = card.actionText;
  els.reflectionInput.value = record?.reflection || "";
  renderSummary();
}

function renderSummary() {
  const records = [...state.records].sort((a, b) => b.date.localeCompare(a.date));
  const completed = records.filter((item) => item.completed);
  els.streakDays.textContent = calculateStreak(records);
  els.doneCount.textContent = `${completed.length} 次`;
  els.reviewGrid.innerHTML = buildReviewItems(records);
  els.historyList.innerHTML = records.length ? records.map(buildHistoryItem).join("") : `<div class="empty">还没有记录。今天保存一次，就会在这里出现。</div>`;
}

function calculateStreak(records) {
  const days = new Set(records.filter((item) => item.completed || item.reflection).map((item) => item.date));
  let count = 0;
  const cursor = new Date(todayKey);
  while (days.has(cursor.toISOString().slice(0, 10))) {
    count += 1;
    cursor.setDate(cursor.getDate() - 1);
  }
  return count;
}

function buildReviewItems(records) {
  const latest = records.slice(0, 4);
  if (!latest.length) {
    return `<div class="empty">先完成几张卡片，复盘会自动长出来。</div>`;
  }
  return latest.map((item) => `
    <div class="review-item">
      <span>${escapeHtml(item.date)} · ${escapeHtml(item.theme)}</span>
      <strong>${escapeHtml(item.title)}</strong>
      <p>${escapeHtml(item.reflection || "还没有写回答。")}</p>
    </div>
  `).join("");
}

function buildHistoryItem(item) {
  return `
    <div class="history-item">
      <span>${escapeHtml(item.date)} · ${item.completed ? "已完成行动" : "未标记行动"}</span>
      <strong>${escapeHtml(item.title)}</strong>
      <p>${escapeHtml(item.reflection || "没有回答内容。")}</p>
    </div>
  `;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function upsertToday(patch) {
  const card = currentCard();
  const existing = state.records.findIndex((item) => item.date === todayKey && item.title === card.title);
  const nextRecord = {
    date: todayKey,
    title: card.title,
    theme: card.theme,
    reflection: "",
    completed: false,
    ...patch
  };
  if (existing >= 0) {
    state.records[existing] = { ...state.records[existing], ...nextRecord };
  } else {
    state.records.push(nextRecord);
  }
  saveState();
  renderSummary();
}

function switchView(viewName) {
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.classList.toggle("is-active", tab.dataset.view === viewName);
  });
  document.querySelectorAll(".view").forEach((view) => {
    view.classList.toggle("is-active", view.id === `${viewName}View`);
  });
}

function showToast(text) {
  els.toast.textContent = text;
  els.toast.classList.add("is-visible");
  window.setTimeout(() => els.toast.classList.remove("is-visible"), 1800);
}

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => switchView(tab.dataset.view));
});

els.saveReflection.addEventListener("click", () => {
  upsertToday({ reflection: els.reflectionInput.value.trim() });
  showToast("今日记录已保存");
});

els.completeAction.addEventListener("click", () => {
  upsertToday({ reflection: els.reflectionInput.value.trim(), completed: true });
  showToast("微行动已标记完成");
});

els.prevCard.addEventListener("click", () => {
  cardIndex = (cardIndex - 1 + cards.length) % cards.length;
  renderToday();
});

els.nextCard.addEventListener("click", () => {
  cardIndex = (cardIndex + 1) % cards.length;
  renderToday();
});

els.clearHistory.addEventListener("click", () => {
  state = { records: [] };
  saveState();
  renderToday();
  showToast("历史记录已清空");
});

renderToday();
