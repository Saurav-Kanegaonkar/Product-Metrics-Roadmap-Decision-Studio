# Data Dictionary

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
