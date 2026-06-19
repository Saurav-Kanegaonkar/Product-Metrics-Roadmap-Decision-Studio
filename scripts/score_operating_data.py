import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "analysis" / "outputs"
ANALYSIS = ROOT / "analysis"
DOC_IMAGES = ROOT / "docs" / "images"

for path in (DATA, OUTPUTS, ANALYSIS, DOC_IMAGES):
    path.mkdir(parents=True, exist_ok=True)

SERVICE_LINES = {
    "placement": {
        "product_area": "Talent placement portal",
        "segment": "job seekers and recruiting coordinators",
        "persona": "placement operations lead",
        "metric": "qualified placement conversion",
    },
    "academy": {
        "product_area": "Academy learning platform",
        "segment": "learners, mentors, and course advisors",
        "persona": "academy program manager",
        "metric": "course completion to interview-ready rate",
    },
    "client_delivery": {
        "product_area": "Client delivery workspace",
        "segment": "client sponsors and delivery squads",
        "persona": "client success director",
        "metric": "on-time milestone acceptance",
    },
    "cloud_saas": {
        "product_area": "Cloud SaaS support console",
        "segment": "managed service clients and support engineers",
        "persona": "support operations manager",
        "metric": "first-contact resolution",
    },
    "mobile": {
        "product_area": "Candidate mobile experience",
        "segment": "mobile-first candidates and account managers",
        "persona": "mobile product owner",
        "metric": "profile completion rate",
    },
    "analytics": {
        "product_area": "Executive analytics layer",
        "segment": "executives, sales, and product leaders",
        "persona": "revenue operations leader",
        "metric": "weekly decision adoption",
    },
}

INITIATIVES = [
    {
        "initiative_id": "INIT-001",
        "service_line": "placement",
        "initiative": "Smart candidate-job matching engine",
        "problem": "Recruiters need faster shortlists that still preserve role fit, interview readiness, and candidate preference signals.",
        "customer_pain": 88,
        "strategic_fit": 91,
        "revenue_reach": 84,
        "market_pressure": 86,
        "effort_points": 34,
        "dependency_risk": 58,
        "analytics_readiness": 79,
        "gtm_readiness": 75,
        "owner": "Product and placement operations",
        "recommendation": "Build now",
    },
    {
        "initiative_id": "INIT-002",
        "service_line": "academy",
        "initiative": "Learner progress and mentor intervention hub",
        "problem": "Course teams need earlier signals when a learner is likely to stall before interview preparation begins.",
        "customer_pain": 82,
        "strategic_fit": 86,
        "revenue_reach": 72,
        "market_pressure": 74,
        "effort_points": 29,
        "dependency_risk": 42,
        "analytics_readiness": 83,
        "gtm_readiness": 81,
        "owner": "Academy product and mentoring",
        "recommendation": "Build now",
    },
    {
        "initiative_id": "INIT-003",
        "service_line": "client_delivery",
        "initiative": "Client project health and acceptance workspace",
        "problem": "Client sponsors need one place to review requirements, delivery risk, acceptance criteria, and milestone decisions.",
        "customer_pain": 90,
        "strategic_fit": 88,
        "revenue_reach": 89,
        "market_pressure": 72,
        "effort_points": 38,
        "dependency_risk": 61,
        "analytics_readiness": 76,
        "gtm_readiness": 68,
        "owner": "Product, engineering, and client success",
        "recommendation": "Pilot with two clients",
    },
    {
        "initiative_id": "INIT-004",
        "service_line": "cloud_saas",
        "initiative": "SaaS support triage and SLA risk console",
        "problem": "Support leads need to see SLA risk, product defects, client tier, and engineering ownership before issues breach.",
        "customer_pain": 85,
        "strategic_fit": 84,
        "revenue_reach": 78,
        "market_pressure": 69,
        "effort_points": 31,
        "dependency_risk": 47,
        "analytics_readiness": 81,
        "gtm_readiness": 73,
        "owner": "Support operations and engineering",
        "recommendation": "Build now",
    },
    {
        "initiative_id": "INIT-005",
        "service_line": "mobile",
        "initiative": "Mobile profile completion and interview prep flow",
        "problem": "Candidates abandon profile setup when resume, skills, availability, and interview prep are split across too many steps.",
        "customer_pain": 78,
        "strategic_fit": 80,
        "revenue_reach": 69,
        "market_pressure": 82,
        "effort_points": 24,
        "dependency_risk": 36,
        "analytics_readiness": 74,
        "gtm_readiness": 84,
        "owner": "Mobile product and UX",
        "recommendation": "Build after instrumentation",
    },
    {
        "initiative_id": "INIT-006",
        "service_line": "analytics",
        "initiative": "Cross-service executive KPI and roadmap review",
        "problem": "Leaders need a common metric contract that connects funnel health, delivery outcomes, support risk, and roadmap tradeoffs.",
        "customer_pain": 74,
        "strategic_fit": 87,
        "revenue_reach": 82,
        "market_pressure": 64,
        "effort_points": 21,
        "dependency_risk": 52,
        "analytics_readiness": 68,
        "gtm_readiness": 70,
        "owner": "Product analytics and executives",
        "recommendation": "Instrument first",
    },
]

THEMES = [
    "workflow visibility",
    "faster decision handoff",
    "mobile completion friction",
    "metric definition gap",
    "client status transparency",
    "learning intervention timing",
    "support SLA risk",
    "competitive feature parity",
]


def roadmap_score(row):
    value = (
        row["customer_pain"] * 0.24
        + row["strategic_fit"] * 0.2
        + row["revenue_reach"] * 0.18
        + row["market_pressure"] * 0.14
        + row["analytics_readiness"] * 0.12
        + row["gtm_readiness"] * 0.08
    )
    drag = row["effort_points"] * 0.34 + row["dependency_risk"] * 0.13
    return round(value - drag + 26, 1)


def risk_band(score):
    if score >= 78:
        return "Ready"
    if score >= 66:
        return "Watch"
    return "Blocked"


def write_csv(path, rows, fields):
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def build_initiatives():
    rows = []
    for item in INITIATIVES:
        service = SERVICE_LINES[item["service_line"]]
        score = roadmap_score(item)
        rows.append(
            {
                "initiative_id": item["initiative_id"],
                "product_area": service["product_area"],
                "initiative": item["initiative"],
                "customer_segment": service["segment"],
                "primary_persona": service["persona"],
                "problem_statement": item["problem"],
                "target_metric": service["metric"],
                "customer_pain_score": item["customer_pain"],
                "strategic_fit_score": item["strategic_fit"],
                "revenue_reach_score": item["revenue_reach"],
                "competitor_pressure_score": item["market_pressure"],
                "effort_points": item["effort_points"],
                "dependency_risk_score": item["dependency_risk"],
                "analytics_readiness_score": item["analytics_readiness"],
                "gtm_readiness_score": item["gtm_readiness"],
                "roadmap_score": score,
                "recommendation": item["recommendation"],
                "owner": item["owner"],
            }
        )
    return sorted(rows, key=lambda row: row["roadmap_score"], reverse=True)


def build_feedback(initiatives):
    rows = []
    channels = ["sales call", "support ticket", "user interview", "product analytics", "CSM note", "training cohort review"]
    for idx, initiative in enumerate(initiatives):
        for week in range(1, 9):
            theme = THEMES[(idx + week) % len(THEMES)]
            volume = 18 + (idx * 7 + week * 5) % 47
            urgency = min(99, int(initiative["customer_pain_score"]) - 12 + (week * 3) % 20)
            revenue = min(99, int(initiative["revenue_reach_score"]) - 10 + (week * 4) % 18)
            rows.append(
                {
                    "signal_id": f"SIG-{idx + 1:02d}-{week:02d}",
                    "initiative_id": initiative["initiative_id"],
                    "week": f"2026-W{week + 10:02d}",
                    "channel": channels[(idx + week) % len(channels)],
                    "theme": theme,
                    "signal_volume": volume,
                    "urgency_score": urgency,
                    "revenue_exposure_score": revenue,
                    "evidence_summary": f"{theme.title()} signal tied to {initiative['product_area'].lower()}",
                }
            )
    return rows


def build_competitors(initiatives):
    competitors = ["Integrated ATS suite", "Learning platform suite", "Client delivery PMO tool", "SaaS support desk", "Mobile career app"]
    rows = []
    for idx, initiative in enumerate(initiatives):
        for comp_idx, competitor in enumerate(competitors[:4]):
            parity = 52 + ((idx + 2) * (comp_idx + 3) * 7) % 38
            gap = max(5, int(initiative["competitor_pressure_score"]) - parity + 18)
            rows.append(
                {
                    "benchmark_id": f"BENCH-{idx + 1:02d}-{comp_idx + 1:02d}",
                    "initiative_id": initiative["initiative_id"],
                    "competitor_archetype": competitor,
                    "capability": initiative["initiative"],
                    "observed_parity_score": parity,
                    "differentiation_gap_score": gap,
                    "recommended_response": "Differentiate" if gap >= 35 else "Match core expectation",
                }
            )
    return rows


def build_backlog(initiatives):
    story_templates = [
        ("Decision context", "As a {persona}, I need the decision context in one place so I can prioritize work without chasing disconnected updates.", "Context includes customer signal, metric, owner, dependency, and decision date."),
        ("Metric contract", "As a product manager, I need a launch metric contract so I can evaluate success before release work starts.", "Primary metric, guardrail metric, data source, event owner, and baseline are documented."),
        ("Acceptance criteria", "As an engineering lead, I need clear acceptance criteria so sprint delivery matches the product intent.", "Acceptance criteria cover happy path, edge cases, instrumentation, QA evidence, and rollback notes."),
    ]
    rows = []
    for idx, initiative in enumerate(initiatives):
        for story_idx, (theme, story, criteria) in enumerate(story_templates):
            sprint = "Sprint 1" if story_idx == 0 and initiative["roadmap_score"] >= 78 else "Sprint 2" if initiative["roadmap_score"] >= 70 else "Discovery"
            priority = "P0" if initiative["roadmap_score"] >= 80 and story_idx < 2 else "P1" if initiative["roadmap_score"] >= 70 else "P2"
            rows.append(
                {
                    "story_id": f"STORY-{idx + 1:02d}-{story_idx + 1:02d}",
                    "initiative_id": initiative["initiative_id"],
                    "theme": theme,
                    "user_story": story.format(persona=initiative["primary_persona"]),
                    "acceptance_criteria": criteria,
                    "priority": priority,
                    "story_points": [5, 3, 8][story_idx] + idx % 3,
                    "sprint_plan": sprint,
                    "owner": ["Product", "Analytics", "Engineering"][story_idx],
                    "dependency": "event tracking" if story_idx == 1 else "UX review" if story_idx == 0 else "QA test plan",
                    "status": "Ready for grooming" if initiative["roadmap_score"] >= 74 else "Needs discovery",
                }
            )
    return rows


def build_release_readiness(initiatives):
    rows = []
    for row in initiatives:
        requirements = min(100, int(row["strategic_fit_score"]) + 4)
        design = min(100, int(row["customer_pain_score"]) - 4)
        engineering = max(35, 100 - int(row["effort_points"]) - int(row["dependency_risk_score"]) // 3)
        qa = min(100, int(row["analytics_readiness_score"]) + 2)
        analytics = int(row["analytics_readiness_score"])
        enablement = int(row["gtm_readiness_score"])
        readiness = round((requirements + design + engineering + qa + analytics + enablement) / 6, 1)
        rows.append(
            {
                "initiative_id": row["initiative_id"],
                "requirements_score": requirements,
                "design_score": design,
                "engineering_score": engineering,
                "qa_score": qa,
                "analytics_score": analytics,
                "sales_enablement_score": enablement,
                "release_readiness_score": readiness,
                "launch_risk": risk_band(readiness),
                "next_gate": "Launch review" if readiness >= 78 else "Resolve analytics and dependency gaps" if readiness >= 66 else "Re-scope MVP",
            }
        )
    return rows


def build_metric_contracts(initiatives):
    rows = []
    guardrails = {
        "placement": "candidate opt-out rate",
        "academy": "mentor intervention backlog",
        "client_delivery": "scope-change cycle time",
        "cloud_saas": "ticket reopen rate",
        "mobile": "support contact rate",
        "analytics": "definition dispute count",
    }
    for item in INITIATIVES:
        initiative = next(row for row in initiatives if row["initiative_id"] == item["initiative_id"])
        service = SERVICE_LINES[item["service_line"]]
        rows.append(
            {
                "metric_contract_id": f"MET-{item['initiative_id'][-3:]}",
                "initiative_id": item["initiative_id"],
                "primary_metric": service["metric"],
                "baseline": f"{58 + int(item['analytics_readiness']) % 19}%",
                "target": f"{66 + int(item['strategic_fit']) % 22}%",
                "guardrail_metric": guardrails[item["service_line"]],
                "source_system": f"{service['product_area']} event stream",
                "sql_check": f"Validate weekly {service['metric']} by initiative and segment",
                "instrumentation_status": "Ready" if initiative["analytics_readiness_score"] >= 78 else "Needs event QA",
            }
        )
    return rows


def build_quality_checks(initiatives):
    checks = ["event completeness", "duplicate account mapping", "owner assignment", "metric definition", "release gate evidence"]
    rows = []
    for idx, initiative in enumerate(initiatives):
        for check_idx, check in enumerate(checks):
            failure_rate = round(max(0.01, (100 - int(initiative["analytics_readiness_score"]) + check_idx * 3 + idx) / 1000), 3)
            rows.append(
                {
                    "check_id": f"QC-{idx + 1:02d}-{check_idx + 1:02d}",
                    "initiative_id": initiative["initiative_id"],
                    "check_name": check,
                    "source_system": initiative["product_area"],
                    "failure_rate": failure_rate,
                    "severity": "High" if failure_rate >= 0.035 and check in ("event completeness", "metric definition") else "Medium" if failure_rate >= 0.025 else "Low",
                    "owner": "Analytics" if check in ("event completeness", "metric definition") else "Product operations",
                }
            )
    return rows


def build_stakeholders(initiatives):
    rows = []
    functions = ["Engineering", "UX", "QA", "Marketing", "Sales", "Executive sponsor"]
    for idx, initiative in enumerate(initiatives):
        for function_idx, function in enumerate(functions):
            alignment = 62 + ((idx + 3) * (function_idx + 2)) % 31
            ask = {
                "Engineering": "Confirm sprint capacity and dependency owner",
                "UX": "Validate workflow with two personas",
                "QA": "Attach regression and acceptance evidence",
                "Marketing": "Prepare launch positioning and FAQ",
                "Sales": "Map enablement to top objection",
                "Executive sponsor": "Approve tradeoff and success metric",
            }[function]
            rows.append(
                {
                    "update_id": f"UPD-{idx + 1:02d}-{function_idx + 1:02d}",
                    "initiative_id": initiative["initiative_id"],
                    "function": function,
                    "alignment_score": alignment,
                    "decision_needed": ask,
                    "cadence": "weekly launch review" if function in ("Engineering", "QA") else "biweekly roadmap review",
                }
            )
    return rows


def write_app_payload(initiatives, feedback, competitors, backlog, readiness, metrics, quality, stakeholders):
    top = initiatives[:3]
    avg_score = round(sum(float(row["roadmap_score"]) for row in initiatives) / len(initiatives), 1)
    ready_count = sum(1 for row in readiness if row["launch_risk"] == "Ready")
    metric_ready = sum(1 for row in metrics if row["instrumentation_status"] == "Ready")
    high_quality = sum(1 for row in quality if row["severity"] == "High")
    payload = {
        "summary": {
            "avgRoadmapScore": avg_score,
            "buildNow": sum(1 for row in initiatives if row["recommendation"] == "Build now"),
            "readyReleases": ready_count,
            "metricReady": metric_ready,
            "highQualityFlags": high_quality,
            "topInitiative": top[0]["initiative"],
            "topInsight": "The best roadmap candidates combine customer pain, strategic fit, metric readiness, and realistic delivery scope.",
        },
        "initiatives": initiatives,
        "feedback": feedback,
        "competitors": competitors,
        "backlog": backlog,
        "readiness": readiness,
        "metrics": metrics,
        "quality": quality,
        "stakeholders": stakeholders,
        "surfaces": [
            "Roadmap command center",
            "Discovery and competitive signals",
            "PRD and Agile delivery",
            "Launch and measurement readiness",
        ],
    }
    (OUTPUTS / "app_payload.json").write_text(json.dumps(payload, indent=2))
    return payload


def write_docs(payload, initiatives):
    readme = """# Product Metrics Roadmap Decision Studio

An interactive Product Manager portfolio artifact for a technology services, training, and SaaS delivery organization. The studio turns customer feedback, market signals, Agile backlog work, release gates, GTM readiness, and product metrics into a roadmap decision packet that a cross-functional team can use before sprint planning or launch review.

## Screenshots

![Roadmap command center](docs/images/roadmap-command-center.png)

**Roadmap command center:** ranks initiatives by customer pain, strategic fit, revenue reach, competitor pressure, delivery effort, dependency risk, analytics readiness, and GTM readiness.

![Discovery and competitive signals](docs/images/discovery-signals.png)

**Discovery and competitive signals:** connects feedback themes, signal volume, revenue exposure, and competitor gaps so roadmap priority is based on evidence instead of volume alone.

![Launch and measurement readiness](docs/images/prd-launch-readiness.png)

**Launch and measurement readiness:** checks release gates, metric contracts, quality issues, and post-launch learning loops before expanding a product release.

## Why This Artifact Exists

Product teams in technology services organizations often support several product surfaces at once: placement workflows, academy learning tools, client delivery portals, SaaS support experiences, mobile candidate journeys, and executive analytics. A PM needs to make roadmap decisions that balance customer value, delivery capacity, SDLC risk, market pressure, and measurable outcomes.

This artifact demonstrates how to turn that ambiguity into a defensible product operating system:

- Define a product strategy and roadmap from mixed qualitative and quantitative evidence.
- Translate feedback and market research into PRD-ready stories and acceptance criteria.
- Prioritize backlog work with Agile delivery constraints and dependency risk.
- Prepare launch, GTM, analytics, QA, and stakeholder communication plans.
- Use SQL-style validation thinking to protect product metrics before launch.

## What Is In The Project

- `index.html`: interactive browser app with four PM surfaces.
- `src/app.js`: app rendering, tab switching, score visualizations, and tables.
- `src/styles.css`: responsive product workspace styling.
- `data/`: deterministic synthetic source datasets.
- `analysis/outputs/app_payload.json`: scored payload used by the app.
- `scripts/score_operating_data.py`: reproducible data generation, scoring, and documentation script.
- `analysis/sql_checks.sql`: SQL-style checks for roadmap, release, metric, and data-quality review.
- `analysis/executive_findings.md`: concise stakeholder readout.
- `data_dictionary.md`: field definitions.

## Data

All data is deterministic synthetic data generated for this public portfolio artifact. It does not represent real company performance, real users, real candidates, real clients, real courses, real tickets, or production systems.

The synthetic structure is modeled on a technology services business with placement services, training programs, bespoke software delivery, cloud/SaaS support, mobile candidate workflows, and executive reporting needs. The generator creates:

- 6 product initiatives across placement, academy, client delivery, cloud SaaS support, mobile, and analytics surfaces.
- 48 feedback signals from sales calls, support tickets, interviews, product analytics, CSM notes, and training cohort reviews.
- 24 competitor benchmark records using competitor archetypes rather than named vendors.
- 18 backlog stories with user stories, acceptance criteria, sprint plans, owners, and dependencies.
- 6 release-readiness records with requirements, design, engineering, QA, analytics, and sales enablement gates.
- 6 metric contracts with baselines, targets, guardrails, source systems, and instrumentation status.
- 30 data-quality checks and 36 stakeholder update records.

The scoring model uses a transparent weighted formula:

`customer pain 24% + strategic fit 20% + revenue reach 18% + competitor pressure 14% + analytics readiness 12% + GTM readiness 8% - effort drag - dependency drag`

The model is intentionally simple because the role is Product Management, not data science. The point is explainable tradeoff judgment, not predictive modeling.

## Run Locally

```bash
python3 scripts/score_operating_data.py
python3 -m http.server 4173
```

Then open `http://localhost:4173`.

## Scope

This is a static public portfolio artifact. It does not connect to live Jira, Confluence, Aha!, Productboard, Trello, Google Analytics, Tableau, Power BI, Looker, cloud services, mobile telemetry, ATS systems, learning platforms, client delivery portals, support desks, or production databases. It shows how a PM can structure the product strategy, backlog, Agile planning, launch readiness, GTM handoff, and measurement logic for a technology services product portfolio.
"""
    (ROOT / "README.md").write_text(readme)

    data_readme = """# Data README

All datasets in this folder are deterministic synthetic data generated for a public portfolio artifact. They do not represent real company performance, users, clients, candidates, learners, support tickets, courses, employees, or production systems.

The data models a technology services and training platform portfolio with placement workflows, academy learning tools, client delivery portals, cloud SaaS support, mobile candidate flows, and executive analytics.

Run `python3 scripts/score_operating_data.py` from the repository root to regenerate every CSV and analysis output.
"""
    (DATA / "README.md").write_text(data_readme)

    findings = f"""# Executive Findings

The synthetic roadmap review identifies {payload['summary']['buildNow']} initiatives ready for near-term build consideration and {payload['summary']['readyReleases']} initiatives with release gates strong enough for launch review.

## Findings

- The top ranked initiative is `{payload['summary']['topInitiative']}`, driven by strong customer pain, strategic fit, revenue reach, and competitive pressure.
- Metric readiness is the main release constraint. {payload['summary']['metricReady']} of {len(initiatives)} metric contracts are ready without additional event QA.
- Data quality risk is manageable but visible. {payload['summary']['highQualityFlags']} high-severity quality checks need owner follow-up before launch decisions.
- The highest value PM behavior is to connect roadmap priority, PRD detail, sprint planning, launch gates, and post-launch measurement in one decision packet.

## Recommended Decision

Move the top build-now initiatives into sprint planning only after each has a confirmed metric contract, QA evidence, stakeholder owner, and launch communication plan.
"""
    (ANALYSIS / "executive_findings.md").write_text(findings)

    methodology = """# Methodology

This artifact uses deterministic synthetic data and transparent scoring. It is designed for portfolio demonstration and interview discussion.

## Scoring

The roadmap score favors customer pain, strategic fit, revenue reach, competitor pressure, analytics readiness, and GTM readiness. It subtracts drag for effort points and dependency risk. The model is intentionally explainable so a PM can defend the tradeoffs with Engineering, UX, QA, Marketing, Sales, and executives.

## Data Assumptions

- Customer pain is higher when feedback volume, urgency, and workflow friction are concentrated.
- Revenue reach is higher when the initiative touches client delivery, placement conversion, support retention, or executive decision adoption.
- Competitor pressure is modeled with competitor archetypes rather than named vendors.
- Release readiness requires requirements, design, engineering, QA, analytics, and sales enablement evidence.
- Metric contracts require a primary metric, baseline, target, guardrail, source system, SQL check, and instrumentation status.
"""
    (ANALYSIS / "methodology.md").write_text(methodology)

    plan = """# Analysis Plan

1. Build the product initiative inventory across placement, academy, client delivery, cloud SaaS support, mobile, and analytics surfaces.
2. Score initiatives using customer pain, strategic fit, revenue reach, competitor pressure, effort, dependency risk, analytics readiness, and GTM readiness.
3. Convert top opportunities into PRD-ready user stories with acceptance criteria, sprint fit, owner, and dependency.
4. Review release gates across requirements, design, engineering, QA, analytics, and sales enablement.
5. Validate metric contracts and SQL-style quality checks before moving work into sprint planning or launch review.
"""
    (ANALYSIS / "analysis_plan.md").write_text(plan)

    recommendations = """# Recommendations

- Prioritize the highest scoring initiatives only when metric contracts and launch gates are ready enough to support post-launch learning.
- Treat customer signal volume as one input, not the decision itself. Combine it with revenue reach, strategic fit, competitor pressure, and delivery risk.
- Require acceptance criteria, analytics instrumentation, and QA evidence before sprint commitment.
- Use stakeholder updates to keep Engineering, UX, QA, Marketing, Sales, and executive sponsors aligned on the decision needed from each function.
"""
    (ANALYSIS / "recommendations.md").write_text(recommendations)

    profile = """# Data Profile

The data profile checks whether the artifact has enough depth for a Product Manager portfolio discussion.

- Product initiatives: 6
- Feedback signals: 48
- Competitor benchmark records: 24
- Backlog stories: 18
- Release readiness records: 6
- Metric contracts: 6
- Data quality checks: 30
- Stakeholder updates: 36

The synthetic data is broad enough to show roadmap strategy, discovery evidence, PRD detail, Agile execution, release readiness, GTM planning, and product metric governance.
"""
    (ANALYSIS / "data_profile.md").write_text(profile)

    sql = """-- SQL-style checks mirror the synthetic CSV outputs in this public portfolio artifact.
-- Table names map to CSV filenames.

-- 1. Roadmap priority review
SELECT
  initiative_id,
  initiative,
  product_area,
  roadmap_score,
  recommendation
FROM product_initiatives
ORDER BY roadmap_score DESC;

-- 2. Feedback concentration by initiative and theme
SELECT
  initiative_id,
  theme,
  SUM(signal_volume) AS total_signals,
  AVG(urgency_score) AS avg_urgency,
  AVG(revenue_exposure_score) AS avg_revenue_exposure
FROM feedback_signals
GROUP BY initiative_id, theme
ORDER BY total_signals DESC;

-- 3. Sprint grooming readiness
SELECT
  initiative_id,
  priority,
  sprint_plan,
  COUNT(*) AS story_count,
  SUM(story_points) AS story_points
FROM backlog_stories
GROUP BY initiative_id, priority, sprint_plan
ORDER BY initiative_id, priority;

-- 4. Launch gate review
SELECT
  initiative_id,
  release_readiness_score,
  launch_risk,
  next_gate
FROM release_readiness
WHERE launch_risk <> 'Ready'
ORDER BY release_readiness_score ASC;

-- 5. Metric contract instrumentation check
SELECT
  initiative_id,
  primary_metric,
  guardrail_metric,
  instrumentation_status
FROM metric_contracts
WHERE instrumentation_status <> 'Ready';

-- 6. High severity quality issues
SELECT
  initiative_id,
  check_name,
  source_system,
  failure_rate,
  owner
FROM data_quality_checks
WHERE severity = 'High'
ORDER BY failure_rate DESC;
"""
    (ANALYSIS / "sql_checks.sql").write_text(sql)

    status = """# Status

- Status: upgraded through the Portfolio Artifact Upgrade Workflow.
- Safe to link as a Product Manager portfolio artifact after changes are pushed.
- Public README uses company-domain language rather than target-company naming.
- Surfaces: roadmap command center, discovery signals, PRD and Agile delivery, launch and measurement readiness.
"""
    (ROOT / "STATUS.md").write_text(status)

    dictionary = """# Data Dictionary

## product_initiatives.csv

- `initiative_id`: stable product initiative identifier.
- `product_area`: product surface or workflow area.
- `initiative`: roadmap candidate name.
- `customer_segment`: user or stakeholder segment affected.
- `primary_persona`: primary decision-maker or workflow owner.
- `problem_statement`: customer or operating problem.
- `target_metric`: primary metric the initiative should move.
- `customer_pain_score`: 0 to 100 pain and urgency score.
- `strategic_fit_score`: 0 to 100 alignment with product strategy.
- `revenue_reach_score`: 0 to 100 reach across revenue, retention, or conversion.
- `competitor_pressure_score`: 0 to 100 market pressure score.
- `effort_points`: Agile effort estimate.
- `dependency_risk_score`: 0 to 100 delivery dependency risk.
- `analytics_readiness_score`: 0 to 100 instrumentation and metric readiness.
- `gtm_readiness_score`: 0 to 100 launch and enablement readiness.
- `roadmap_score`: weighted prioritization score.
- `recommendation`: recommended roadmap action.
- `owner`: accountable function group.

## feedback_signals.csv

Customer, sales, support, interview, analytics, CSM, and cohort review signals used for discovery.

## competitor_benchmarks.csv

Competitor archetype comparison records. These are synthetic archetypes, not named vendor claims.

## backlog_stories.csv

PRD-ready story map with user story, acceptance criteria, priority, story points, sprint plan, owner, dependency, and status.

## release_readiness.csv

Release gate scores across requirements, design, engineering, QA, analytics, and sales enablement.

## metric_contracts.csv

Metric definitions with baseline, target, guardrail, source system, SQL check, and instrumentation status.

## data_quality_checks.csv

Synthetic quality checks for event completeness, ownership, metric definitions, and release evidence.

## stakeholder_updates.csv

Cross-functional stakeholder alignment, decision asks, and review cadence.
"""
    (ROOT / "data_dictionary.md").write_text(dictionary)


def main():
    initiatives = build_initiatives()
    feedback = build_feedback(initiatives)
    competitors = build_competitors(initiatives)
    backlog = build_backlog(initiatives)
    readiness = build_release_readiness(initiatives)
    metrics = build_metric_contracts(initiatives)
    quality = build_quality_checks(initiatives)
    stakeholders = build_stakeholders(initiatives)

    write_csv(DATA / "product_initiatives.csv", initiatives, list(initiatives[0].keys()))
    write_csv(DATA / "feedback_signals.csv", feedback, list(feedback[0].keys()))
    write_csv(DATA / "competitor_benchmarks.csv", competitors, list(competitors[0].keys()))
    write_csv(DATA / "backlog_stories.csv", backlog, list(backlog[0].keys()))
    write_csv(DATA / "release_readiness.csv", readiness, list(readiness[0].keys()))
    write_csv(DATA / "metric_contracts.csv", metrics, list(metrics[0].keys()))
    write_csv(DATA / "data_quality_checks.csv", quality, list(quality[0].keys()))
    write_csv(DATA / "stakeholder_updates.csv", stakeholders, list(stakeholders[0].keys()))

    payload = write_app_payload(initiatives, feedback, competitors, backlog, readiness, metrics, quality, stakeholders)
    write_docs(payload, initiatives)

    print(f"Generated {len(initiatives)} initiatives, {len(feedback)} feedback signals, {len(backlog)} stories.")
    print(f"Top initiative: {payload['summary']['topInitiative']}")
    print(f"Average roadmap score: {payload['summary']['avgRoadmapScore']}")


if __name__ == "__main__":
    main()
