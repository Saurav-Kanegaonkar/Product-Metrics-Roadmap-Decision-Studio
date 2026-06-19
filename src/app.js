const state = {
  data: null,
  view: new URLSearchParams(window.location.search).get("view") || "roadmap",
  selectedId: null,
};

const app = document.querySelector("#app");
const summaryCards = document.querySelector("#summaryCards");

const fmt = new Intl.NumberFormat("en-US", { maximumFractionDigits: 1 });

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function tagClass(value) {
  if (["Build now", "Ready", "P0", "Launch review"].includes(value)) return "green";
  if (["Watch", "P1", "Pilot with two clients", "Build after instrumentation"].includes(value)) return "amber";
  if (["Blocked", "P2", "Instrument first", "Re-scope MVP"].includes(value)) return "rose";
  return "";
}

function tag(value) {
  return `<span class="tag ${tagClass(value)}">${escapeHtml(value)}</span>`;
}

function bar(label, value) {
  const width = Math.max(4, Math.min(100, Number(value)));
  return `
    <div class="bar-row">
      <div class="bar-label"><span>${escapeHtml(label)}</span><span>${fmt.format(value)}</span></div>
      <div class="bar-track"><div class="bar-fill" style="width:${width}%"></div></div>
    </div>
  `;
}

function selectedInitiative() {
  return state.data.initiatives.find((row) => row.initiative_id === state.selectedId) || state.data.initiatives[0];
}

function rowsToTable(columns, rows) {
  return `
    <div class="table-wrap">
      <table>
        <thead>
          <tr>${columns.map((col) => `<th>${escapeHtml(col.label)}</th>`).join("")}</tr>
        </thead>
        <tbody>
          ${rows.map((row) => `
            <tr>
              ${columns.map((col) => `<td>${col.render ? col.render(row) : escapeHtml(row[col.key])}</td>`).join("")}
            </tr>
          `).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function renderSummary() {
  const { summary } = state.data;
  const cards = [
    ["Avg roadmap score", summary.avgRoadmapScore, "Weighted PM decision model"],
    ["Build-now bets", summary.buildNow, "Near-term candidates"],
    ["Metric-ready", summary.metricReady, "Contracts ready for launch"],
    ["Quality flags", summary.highQualityFlags, "High severity checks"],
  ];

  summaryCards.innerHTML = `
    <div class="summary-grid">
      ${cards.map(([label, value, note]) => `
        <div class="metric-card">
          <span>${escapeHtml(label)}</span>
          <strong>${escapeHtml(value)}</strong>
          <small>${escapeHtml(note)}</small>
        </div>
      `).join("")}
    </div>
  `;
}

function renderRoadmap() {
  const initiatives = state.data.initiatives;
  const top = selectedInitiative();
  const scoreBars = [
    ["Customer pain", top.customer_pain_score],
    ["Strategic fit", top.strategic_fit_score],
    ["Revenue reach", top.revenue_reach_score],
    ["Competitor pressure", top.competitor_pressure_score],
    ["Analytics readiness", top.analytics_readiness_score],
    ["GTM readiness", top.gtm_readiness_score],
  ];

  app.innerHTML = `
    <section class="split">
      <div class="section">
        <h2>Roadmap Command Center</h2>
        <div class="initiative-list">
          ${initiatives.map((item) => `
            <article class="decision-card">
              <div class="decision-head">
                <div>
                  <h3>${escapeHtml(item.initiative)}</h3>
                  <p>${escapeHtml(item.problem_statement)}</p>
                </div>
                <button class="score" data-select="${escapeHtml(item.initiative_id)}" aria-label="Select ${escapeHtml(item.initiative)}">${escapeHtml(item.roadmap_score)}</button>
              </div>
              <div class="tag-row">
                ${tag(item.product_area)}
                ${tag(item.recommendation)}
                ${tag(item.target_metric)}
              </div>
            </article>
          `).join("")}
        </div>
      </div>

      <aside class="section">
        <h2>Selected Tradeoff</h2>
        <h3>${escapeHtml(top.initiative)}</h3>
        <p>${escapeHtml(top.customer_segment)}</p>
        <div class="bar-stack">${scoreBars.map(([label, value]) => bar(label, value)).join("")}</div>
        <div class="callout" style="margin-top:16px">
          <strong>PM read:</strong>
          ${escapeHtml(top.recommendation)} because the initiative scores ${escapeHtml(top.roadmap_score)} after effort and dependency drag.
        </div>
      </aside>
    </section>

    <section class="section">
      <h2>Decision Queue</h2>
      ${rowsToTable(
        [
          { label: "Initiative", key: "initiative" },
          { label: "Persona", key: "primary_persona" },
          { label: "Score", key: "roadmap_score" },
          { label: "Effort", key: "effort_points" },
          { label: "Risk", key: "dependency_risk_score" },
          { label: "Recommendation", key: "recommendation", render: (row) => tag(row.recommendation) },
        ],
        initiatives
      )}
    </section>
  `;
}

function renderDiscovery() {
  const top = selectedInitiative();
  const signals = state.data.feedback
    .filter((row) => row.initiative_id === top.initiative_id)
    .sort((a, b) => Number(b.signal_volume) - Number(a.signal_volume));
  const competitors = state.data.competitors
    .filter((row) => row.initiative_id === top.initiative_id)
    .sort((a, b) => Number(b.differentiation_gap_score) - Number(a.differentiation_gap_score));
  const totalSignals = signals.reduce((sum, row) => sum + Number(row.signal_volume), 0);
  const avgUrgency = signals.reduce((sum, row) => sum + Number(row.urgency_score), 0) / signals.length;
  const avgRevenue = signals.reduce((sum, row) => sum + Number(row.revenue_exposure_score), 0) / signals.length;

  app.innerHTML = `
    <section class="split">
      <div class="section">
        <h2>Discovery Evidence</h2>
        <h3>${escapeHtml(top.initiative)}</h3>
        <div class="mini-kpis">
          <div class="mini-kpi"><strong>${totalSignals}</strong><span>Signals reviewed</span></div>
          <div class="mini-kpi"><strong>${fmt.format(avgUrgency)}</strong><span>Avg urgency</span></div>
          <div class="mini-kpi"><strong>${fmt.format(avgRevenue)}</strong><span>Avg revenue exposure</span></div>
        </div>
        <ul class="insight-list" style="margin-top:16px">
          ${signals.slice(0, 4).map((row) => `
            <li><strong>${escapeHtml(row.theme)}:</strong> ${escapeHtml(row.evidence_summary)} from ${escapeHtml(row.channel)} with ${escapeHtml(row.signal_volume)} signals.</li>
          `).join("")}
        </ul>
      </div>

      <aside class="section">
        <h2>Competitive Response</h2>
        <div class="bar-stack">
          ${competitors.map((row) => bar(row.competitor_archetype, row.differentiation_gap_score)).join("")}
        </div>
        <div class="tag-row" style="margin-top:16px">
          ${competitors.map((row) => tag(row.recommended_response)).join("")}
        </div>
      </aside>
    </section>

    <section class="section">
      <h2>Feedback Signal Table</h2>
      ${rowsToTable(
        [
          { label: "Week", key: "week" },
          { label: "Channel", key: "channel" },
          { label: "Theme", key: "theme" },
          { label: "Volume", key: "signal_volume" },
          { label: "Urgency", key: "urgency_score" },
          { label: "Revenue", key: "revenue_exposure_score" },
        ],
        signals
      )}
    </section>
  `;
}

function renderDelivery() {
  const top = selectedInitiative();
  const stories = state.data.backlog.filter((row) => row.initiative_id === top.initiative_id);
  const stakeholderRows = state.data.stakeholders
    .filter((row) => row.initiative_id === top.initiative_id)
    .sort((a, b) => Number(b.alignment_score) - Number(a.alignment_score));
  const points = stories.reduce((sum, row) => sum + Number(row.story_points), 0);

  app.innerHTML = `
    <section class="three">
      <article class="section">
        <h2>PRD Focus</h2>
        <h3>${escapeHtml(top.initiative)}</h3>
        <p>${escapeHtml(top.problem_statement)}</p>
        <div class="tag-row">
          ${tag(top.primary_persona)}
          ${tag(top.target_metric)}
        </div>
      </article>
      <article class="section">
        <h2>Sprint Shape</h2>
        <div class="mini-kpis">
          <div class="mini-kpi"><strong>${stories.length}</strong><span>Stories</span></div>
          <div class="mini-kpi"><strong>${points}</strong><span>Story points</span></div>
          <div class="mini-kpi"><strong>${stories.filter((row) => row.priority === "P0").length}</strong><span>P0 stories</span></div>
        </div>
      </article>
      <article class="section">
        <h2>Scrum Input</h2>
        <ul class="insight-list">
          <li>Bring decision context and acceptance criteria into grooming.</li>
          <li>Confirm event tracking and QA evidence before sprint commitment.</li>
          <li>Use stakeholder asks to keep ceremonies decision-oriented.</li>
        </ul>
      </article>
    </section>

    <section class="section">
      <h2>Story Map</h2>
      ${rowsToTable(
        [
          { label: "Theme", key: "theme" },
          { label: "User Story", key: "user_story" },
          { label: "Acceptance Criteria", key: "acceptance_criteria" },
          { label: "Priority", key: "priority", render: (row) => tag(row.priority) },
          { label: "Sprint", key: "sprint_plan" },
          { label: "Owner", key: "owner" },
        ],
        stories
      )}
    </section>

    <section class="section">
      <h2>Stakeholder Decision Asks</h2>
      ${rowsToTable(
        [
          { label: "Function", key: "function" },
          { label: "Alignment", key: "alignment_score" },
          { label: "Decision Needed", key: "decision_needed" },
          { label: "Cadence", key: "cadence" },
        ],
        stakeholderRows
      )}
    </section>
  `;
}

function renderLaunch() {
  const top = selectedInitiative();
  const readiness = state.data.readiness.find((row) => row.initiative_id === top.initiative_id);
  const metric = state.data.metrics.find((row) => row.initiative_id === top.initiative_id);
  const quality = state.data.quality
    .filter((row) => row.initiative_id === top.initiative_id)
    .sort((a, b) => Number(b.failure_rate) - Number(a.failure_rate));
  const readinessBars = [
    ["Requirements", readiness.requirements_score],
    ["Design", readiness.design_score],
    ["Engineering", readiness.engineering_score],
    ["QA", readiness.qa_score],
    ["Analytics", readiness.analytics_score],
    ["Sales enablement", readiness.sales_enablement_score],
  ];

  app.innerHTML = `
    <section class="split">
      <div class="section">
        <h2>Launch Readiness</h2>
        <h3>${escapeHtml(top.initiative)}</h3>
        <div class="mini-kpis">
          <div class="mini-kpi"><strong>${escapeHtml(readiness.release_readiness_score)}</strong><span>Readiness score</span></div>
          <div class="mini-kpi"><strong>${escapeHtml(readiness.launch_risk)}</strong><span>Launch risk</span></div>
          <div class="mini-kpi"><strong>${escapeHtml(metric.instrumentation_status)}</strong><span>Instrumentation</span></div>
        </div>
        <div class="bar-stack" style="margin-top:18px">
          ${readinessBars.map(([label, value]) => bar(label, value)).join("")}
        </div>
      </div>

      <aside class="section">
        <h2>Metric Contract</h2>
        <ul class="insight-list">
          <li><strong>Primary:</strong> ${escapeHtml(metric.primary_metric)} from ${escapeHtml(metric.source_system)}.</li>
          <li><strong>Baseline to target:</strong> ${escapeHtml(metric.baseline)} to ${escapeHtml(metric.target)}.</li>
          <li><strong>Guardrail:</strong> ${escapeHtml(metric.guardrail_metric)}.</li>
          <li><strong>SQL check:</strong> ${escapeHtml(metric.sql_check)}.</li>
        </ul>
        <div class="callout" style="margin-top:16px">
          <strong>Next gate:</strong> ${escapeHtml(readiness.next_gate)}
        </div>
      </aside>
    </section>

    <section class="two">
      <div class="section">
        <h2>Quality Checks</h2>
        ${rowsToTable(
          [
            { label: "Check", key: "check_name" },
            { label: "Failure Rate", key: "failure_rate" },
            { label: "Severity", key: "severity", render: (row) => tag(row.severity) },
            { label: "Owner", key: "owner" },
          ],
          quality
        )}
      </div>
      <div class="section">
        <h2>Post-Launch Learning Plan</h2>
        <ul class="insight-list">
          <li>Review primary metric weekly for the first three sprint review cycles after launch.</li>
          <li>Watch guardrail movement before expanding the release to the next product segment.</li>
          <li>Compare support, sales, and product analytics feedback against the PRD success criteria.</li>
          <li>Send one stakeholder status note with decision, metric movement, quality risk, and next action.</li>
        </ul>
      </div>
    </section>
  `;
}

function render() {
  renderSummary();
  const renderers = {
    roadmap: renderRoadmap,
    discovery: renderDiscovery,
    delivery: renderDelivery,
    launch: renderLaunch,
  };
  renderers[state.view]();

  document.querySelectorAll("[data-select]").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedId = button.dataset.select;
      render();
    });
  });
}

document.querySelectorAll(".tab").forEach((button) => {
  button.classList.toggle("is-active", button.dataset.view === state.view);
  button.addEventListener("click", () => {
    state.view = button.dataset.view;
    document.querySelectorAll(".tab").forEach((tab) => tab.classList.toggle("is-active", tab === button));
    render();
  });
});

fetch("analysis/outputs/app_payload.json")
  .then((response) => {
    if (!response.ok) throw new Error("Could not load app payload");
    return response.json();
  })
  .then((payload) => {
    state.data = payload;
    state.selectedId = payload.initiatives[0].initiative_id;
    render();
  })
  .catch((error) => {
    app.innerHTML = `
      <section class="section">
        <h2>Unable To Load Data</h2>
        <p>${escapeHtml(error.message)}. Run <code>python3 scripts/score_operating_data.py</code> and start a local web server.</p>
      </section>
    `;
  });
