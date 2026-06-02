const cards = [
  {
    title: "沉没成本：那家开了三个月还没人来的小店",
    theme: "决策偏误",
    tags: ["沉没成本", "止损", "选择"],
    caseText: "小林和朋友合伙开了一家社区咖啡店。装修时他们选了更贵的木质吧台，又预付了半年房租，还花了很多晚上调菜单。开业三个月后，客流一直很低，附近居民更习惯去便利店买咖啡。朋友提出关店，小林第一反应是反对：钱都花了，时间也搭进去了，现在关掉不就全白费了吗？真正让他卡住的，不是未来还有多大希望，而是过去的投入让他不甘心。",
    modelText: "沉没成本是已经发生且无法收回的投入。做下一步判断时，它不应该成为继续投入的理由。真正该问的是：从今天开始，如果重新选择，我还会把时间、钱和注意力投到这里吗？",
    mistakeText: "最常见的误判，是把“不想浪费过去”误认为“应该继续未来”。过去的钱已经回不来，继续投入只会制造新的成本。一个清醒的判断，要把过去的投入从决策桌上拿走。",
    questionText: "我现在坚持的一件事，是因为它仍然值得，还是因为我不想承认过去那一步可能走错了？",
    actionText: "花 10 分钟写下一个你舍不得停的选择，只比较“从今天继续”和“今天停止”的未来结果。"
  },
  {
    title: "二阶思维：那个看起来很省事的临时方案",
    theme: "长期主义",
    tags: ["二阶思维", "复利", "延迟满足"],
    caseText: "产品经理阿远为了赶周五上线，决定先用一个临时规则绕过复杂校验。第一层结果很好：上线准时，老板满意，群里一片轻松。两周后，客服开始收到奇怪投诉，运营不得不手动修数据，开发也不敢改相关功能，因为没人知道那个临时规则会影响哪里。阿远后来意识到，他当时只看到了“今天省下半天”，没有看到“未来每周多花两小时”。",
    modelText: "二阶思维不是只问这个选择立刻带来什么，而是继续追问：这个结果会制造什么新的行为、限制和连锁反应？短期顺手的选择，可能在长期变成维护成本。",
    mistakeText: "人很容易被第一层结果诱惑：快、爽、省事、避免冲突。但真正决定质量的，常常是第二层后果：它会不会让系统更脆弱，让关系更含糊，让自己更被动。",
    questionText: "我今天想快速解决的一件事，两周后会不会以另一种形式回来找我？",
    actionText: "用 10 分钟写两列：第一列是立刻好处，第二列是两周后的代价或收益。只分析一个选择。"
  },
  {
    title: "边界感：从帮忙一次到默认责任",
    theme: "人性与关系",
    tags: ["边界", "互惠", "关系"],
    caseText: "同事小周第一次请你帮他改汇报材料时，你觉得只是顺手。第二次，他说自己太忙，你又帮了。第三次，他直接把文档发来，还补一句“还是你改得快”。你心里不舒服，但又怕拒绝显得小气。慢慢地，你发现自己不是在帮忙，而是在替他承担他本该练习的能力。关系里的怨气，往往不是从拒绝开始，而是从不清楚的默认开始。",
    modelText: "边界不是冷漠，而是让责任回到正确的位置。健康的关系需要善意，也需要清楚：什么我愿意帮，什么你需要自己承担，什么不能变成长期默认。",
    mistakeText: "很多人把拒绝理解成伤害别人，于是用过度承担换短暂和平。结果是表面没有冲突，心里却积累怨气，最后关系更容易突然崩掉。",
    questionText: "我最近哪一次答应，其实不是愿意，而是害怕对方失望或不高兴？",
    actionText: "花 10 分钟写一句边界表达：这次我可以帮到哪里，下一步需要你自己完成什么。"
  },
  {
    title: "激励错位：当团队开始只追一个数字",
    theme: "商业与产品",
    tags: ["激励", "指标", "产品判断"],
    caseText: "一家内容产品把“日活”定成最重要指标。起初，团队只是优化提醒和入口。后来，为了让用户回来，页面开始塞更多弹窗，消息提醒越来越频繁，推荐内容也变得更刺激。日活确实涨了，但用户停留质量下降，投诉变多，老用户开始说这个产品变吵了。数字赢了，产品输了。",
    modelText: "指标会塑造行为。一个指标如果离真实目标太远，就会诱导团队优化表面结果。好指标应该逼近真实价值，同时配一个反指标防止跑偏。",
    mistakeText: "常见误判是把“容易统计”当成“真正重要”。日活、点击、转化都可能有用，但它们只是替身，不是目标本身。替身一旦被崇拜，行动就会变形。",
    questionText: "我现在追的一个数字，真的代表进步吗，还是只是更容易被看见？",
    actionText: "用 10 分钟给一个目标补一句反指标：如果这个数字变好但什么变坏，就说明我跑偏了。"
  },
  {
    title: "反馈循环：为什么救火的人总是越来越忙",
    theme: "职场与管理",
    tags: ["反馈", "协作", "管理"],
    caseText: "团队里有个同事特别会救火。项目临近上线，他总能熬夜把问题补上，因此每次复盘都被表扬。久而久之，大家开始默认：前期规划粗一点也没关系，反正最后有人兜底。那个救火的人越来越累，系统也越来越依赖临时补救。问题不在于他不该负责，而在于团队把奖励给了最后一刻的英雄，而不是提前把风险消掉的人。",
    modelText: "系统会重复被奖励的行为。你表扬什么、关注什么、容忍什么，都会形成反馈循环。想改变结果，不能只要求人改变，还要改变奖励和注意力的流向。",
    mistakeText: "常见误判是只批评个人不主动，却不看环境正在鼓励什么。如果提前预防没人看见，临时救火却被称赞，系统就会自然长成救火型。",
    questionText: "我所在的环境正在奖励哪一种行为，即使嘴上说想要另一种？",
    actionText: "花 10 分钟写下一个你想鼓励的行为，并设计一次具体、及时的正反馈。"
  },
  {
    title: "安全边际：刚好赶上其实不是计划",
    theme: "风险判断",
    tags: ["安全边际", "周期", "风险"],
    caseText: "你准备下午三点见一个重要客户。地图显示路上需要四十分钟，于是你两点二十出门，看起来刚刚好。结果路上临时堵车，停车场也满了，你到会议室时已经迟到五分钟。你的计划并不是失败在计算错了四十分钟，而是失败在默认一切都会按平均情况发生。现实只要稍微偏离，刚好就会变成不够。",
    modelText: "安全边际是在不确定世界里给自己留余地。它不是保守，而是承认预测会错、环境会变、人会疲惫，重要事情不能只按理想情况设计。",
    mistakeText: "常见误判是把“正常情况下可行”当成“真实情况下可靠”。越重要的事，越需要缓冲。没有缓冲的计划，本质上是在赌世界配合你。",
    questionText: "我最近哪件事只在一切顺利时才成立？",
    actionText: "用 10 分钟给这件事加一个缓冲：时间、钱、精力或备用方案任选其一。"
  },
  {
    title: "周复盘：从一次失误看见一个重复模式",
    theme: "本周复盘",
    tags: ["复盘", "模式识别", "下周方向"],
    caseText: "周日晚上，你回想这一周，发现自己又把一个重要任务拖到了最后一天。表面看，这是一次时间管理失败。但如果继续看，会发现类似场景已经出现过三次：只要任务不够明确、没人马上检查、结果又比较重要，你就会拖到压力足够大才开始。复盘的价值，不是责备这一次，而是看见那个反复出现的启动模式。",
    modelText: "模式识别能让你从事件层上升到系统层。不要只问这次发生了什么，也要问：它为什么总以相似方式发生？触发条件是什么？我能提前改变哪一个小环节？",
    mistakeText: "很多复盘会变成流水账，或者变成自我批评。真正有用的复盘，是找到一个下周能改变的小杠杆，而不是给自己贴一个笼统标签。",
    questionText: "本周我在哪一种场景下最容易判断失真或行动变形？",
    actionText: "花 10 分钟选出本周一个重复模式，并给下周设置一个提前提醒或更小的第一步。"
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
    .map((tag) => `<span class="theme-chip">${escapeHtml(tag)}</span>`)
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
