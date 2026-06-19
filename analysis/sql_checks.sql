-- SQL-style checks mirror the synthetic CSV outputs in this public portfolio artifact.
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
