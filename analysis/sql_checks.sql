-- Example quality checks for Product Metrics Roadmap Decision Studio
select source_system, check_type, avg(failure_rate_pct) as avg_failure_rate
from data_quality_checks
group by source_system, check_type
order by avg_failure_rate desc;

select entity_id, avg(priority_score) as avg_priority_score
from daily_metrics
group by entity_id
order by avg_priority_score desc;
