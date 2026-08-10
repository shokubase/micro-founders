const LABELS = {
  team_size_bucket: { solo: "1인", "2-3": "2-3인", "4+": "4인 이상", unknown: "미상" },
  revenue_bucket: { "<100K": "$100K 미만", "100K-1M": "$100K~1M", "1M-10M": "$1M~10M", "10M+": "$10M+", unknown: "미상" },
  founder_background: { developer: "개발자 출신", "non-developer": "비개발자", mixed: "혼합/일부기술", unknown: "미상" },
  founder_experience: { "first-time": "첫 창업", serial: "연쇄창업", mixed: "혼합", unknown: "미상" },
  confidence: { high: "높음", medium: "중간", low: "낮음" },
};

const state = {
  data: [],
  filters: { domain_category: new Set(), team_size_bucket: new Set(), revenue_bucket: new Set(), founder_background: new Set() },
  search: "",
  sort: "revenue-desc",
};

const REVENUE_ORDER = ["unknown", "<100K", "100K-1M", "1M-10M", "10M+"];

function fmtUsd(v) {
  if (v === null || v === undefined) return "비공개";
  if (v >= 1_000_000) return "$" + (v / 1_000_000).toFixed(1).replace(/\.0$/, "") + "M/yr(추정)";
  if (v >= 1_000) return "$" + Math.round(v / 1000) + "K/yr(추정)";
  return "$" + v + "/yr(추정)";
}

async function init() {
  const res = await fetch("data/cases.json");
  state.data = await res.json();
  buildFilterChips();
  bindControls();
  checkNewBadge();
  render();
}

function uniqueValues(key) {
  return [...new Set(state.data.map((d) => d[key]).filter(Boolean))].sort();
}

function buildFilterChips() {
  buildChipGroup("filter-domain", uniqueValues("domain_category"), "domain_category", (v) => v);
  buildChipGroup("filter-team", ["solo", "2-3", "4+", "unknown"], "team_size_bucket", (v) => LABELS.team_size_bucket[v]);
  buildChipGroup("filter-revenue", REVENUE_ORDER, "revenue_bucket", (v) => LABELS.revenue_bucket[v]);
  buildChipGroup("filter-background", ["developer", "non-developer", "mixed", "unknown"], "founder_background", (v) => LABELS.founder_background[v]);
}

function buildChipGroup(containerId, values, filterKey, labelFn) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";
  values.forEach((v) => {
    const btn = document.createElement("button");
    btn.className = "chip";
    btn.textContent = labelFn(v);
    btn.dataset.value = v;
    btn.addEventListener("click", () => {
      const set = state.filters[filterKey];
      if (set.has(v)) set.delete(v);
      else set.add(v);
      btn.classList.toggle("active");
      render();
    });
    container.appendChild(btn);
  });
}

function bindControls() {
  document.getElementById("search-box").addEventListener("input", (e) => {
    state.search = e.target.value.trim().toLowerCase();
    render();
  });
  document.getElementById("sort-select").addEventListener("change", (e) => {
    state.sort = e.target.value;
    render();
  });
  document.getElementById("reset-filters").addEventListener("click", () => {
    Object.values(state.filters).forEach((s) => s.clear());
    state.search = "";
    document.getElementById("search-box").value = "";
    document.querySelectorAll(".chip.active").forEach((c) => c.classList.remove("active"));
    render();
  });
  document.getElementById("modal-close").addEventListener("click", closeModal);
  document.getElementById("modal-backdrop").addEventListener("click", (e) => {
    if (e.target.id === "modal-backdrop") closeModal();
  });
}

function matchesFilters(item) {
  for (const [key, set] of Object.entries(state.filters)) {
    if (set.size > 0 && !set.has(item[key])) return false;
  }
  if (state.search) {
    const hay = [item.product, ...(item.founders || []), item.one_liner, item.domain, item.region]
      .join(" ")
      .toLowerCase();
    if (!hay.includes(state.search)) return false;
  }
  return true;
}

function sortData(list) {
  const conf = { high: 3, medium: 2, low: 1 };
  const copy = [...list];
  switch (state.sort) {
    case "revenue-desc":
      copy.sort((a, b) => (b.revenue_annual_usd_est ?? -1) - (a.revenue_annual_usd_est ?? -1));
      break;
    case "revenue-asc":
      copy.sort((a, b) => (a.revenue_annual_usd_est ?? Infinity) - (b.revenue_annual_usd_est ?? Infinity));
      break;
    case "recent":
      copy.sort((a, b) => (b.ingested_at || "").localeCompare(a.ingested_at || ""));
      break;
    case "confidence":
      copy.sort((a, b) => (conf[b.confidence] || 0) - (conf[a.confidence] || 0));
      break;
  }
  return copy;
}

function render() {
  const list = sortData(state.data.filter(matchesFilters));
  document.getElementById("case-count").textContent = `${list.length} / ${state.data.length}개 사례`;
  const container = document.getElementById("results");
  container.innerHTML = "";
  if (list.length === 0) {
    container.innerHTML = '<div class="no-results">조건에 맞는 사례가 없습니다.</div>';
    return;
  }
  list.forEach((item) => container.appendChild(renderCard(item)));
}

function renderCard(item) {
  const card = document.createElement("div");
  card.className = "card";
  card.innerHTML = `
    <h3>${escapeHtml(item.product)}</h3>
    <div class="product-founders">${escapeHtml((item.founders || []).join(", "))} · ${escapeHtml(item.region || "미상")}</div>
    <div class="one-liner">${escapeHtml(item.one_liner || "")}</div>
    <div class="tags">
      <span class="tag">${escapeHtml(item.domain_category || "미분류")}</span>
      <span class="tag">${escapeHtml(LABELS.team_size_bucket[item.team_size_bucket] || "미상")}</span>
      <span class="tag">${escapeHtml(LABELS.founder_background[item.founder_background] || "미상")}</span>
    </div>
    <div class="card-footer">
      <span class="revenue-badge">${fmtUsd(item.revenue_annual_usd_est)}</span>
      <span><span class="confidence-dot confidence-${item.confidence}"></span>${LABELS.confidence[item.confidence] || "미상"}</span>
    </div>
  `;
  card.addEventListener("click", () => openModal(item));
  return card;
}

function openModal(item) {
  const body = document.getElementById("modal-body");
  body.innerHTML = `
    <h2>${escapeHtml(item.product)}</h2>
    <p class="product-founders">${escapeHtml((item.founders || []).join(", "))} · ${escapeHtml(item.region || "미상")}</p>
    <p>${escapeHtml(item.one_liner || "")}</p>
    <dl>
      <dt>도메인</dt><dd>${escapeHtml(item.domain_category || "미상")}</dd>
      <dt>팀 규모</dt><dd>${escapeHtml(item.team_size || "미상")}</dd>
      <dt>매출(원문)</dt><dd>${escapeHtml(item.revenue || "미상")}</dd>
      <dt>매출(추정 연환산)</dt><dd>${fmtUsd(item.revenue_annual_usd_est)}</dd>
      <dt>Exit/펀딩</dt><dd>${escapeHtml(formatMoneyFields(item))}</dd>
      <dt>스택</dt><dd>${escapeHtml((item.stack || []).join(", ") || "미상")}</dd>
      <dt>AI 툴</dt><dd>${escapeHtml((item.ai_tools || []).join(", ") || "미상")}</dd>
      <dt>창업자 배경</dt><dd>${escapeHtml(item.founder_background_raw || item.founder_background || "미상")}</dd>
      <dt>비즈니스 모델</dt><dd>${escapeHtml(item.business_model || "미상")}</dd>
      <dt>상태</dt><dd>${escapeHtml(item.exit_status || "미상")}</dd>
      <dt>신뢰도</dt><dd>${LABELS.confidence[item.confidence] || "미상"}</dd>
    </dl>
    <div class="sources">
      <strong>출처</strong>
      ${(item.sources || []).map((s) => `<a href="${s}" target="_blank" rel="noopener">${s}</a>`).join("")}
    </div>
    ${item.normalize_note ? `<div class="note">매출 추정 방식: ${escapeHtml(item.normalize_note)}</div>` : ""}
  `;
  document.getElementById("modal-backdrop").hidden = false;
}

function formatMoneyFields(item) {
  const parts = [];
  if (item.exit_value_usd) parts.push(`인수가 $${(item.exit_value_usd / 1_000_000).toFixed(0)}M`);
  if (item.funding_usd) parts.push(`누적투자 $${(item.funding_usd / 1_000_000).toFixed(1)}M`);
  if (item.valuation_usd) parts.push(`밸류에이션 $${(item.valuation_usd / 1_000_000_000).toFixed(1)}B`);
  return parts.length ? parts.join(" / ") : "해당없음";
}

function closeModal() {
  document.getElementById("modal-backdrop").hidden = true;
}

function escapeHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function checkNewBadge() {
  const lastVisit = localStorage.getItem("vibedb_last_visit");
  const badge = document.getElementById("new-badge");
  if (lastVisit) {
    const newCount = state.data.filter((d) => d.ingested_at > lastVisit).length;
    if (newCount > 0) {
      badge.hidden = false;
      badge.textContent = `새 사례 ${newCount}건`;
    }
  }
  const today = new Date().toISOString().slice(0, 10);
  localStorage.setItem("vibedb_last_visit", today);
}

init();
