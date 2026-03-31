"""AutonomyTracker — Level 5 measurement system.

Categorizes tasks/workflows as fully_agentic, mixed, or human_only.
Tracks ratios over time. Predicts when workflows will shift categories.
Maps to Richard's Five Levels framework.
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.expanduser('~/shared/tools/data'))

from .types import PredictionResult
from .core import BayesianCore

# Lazy DB imports
_db = None
_db_write = None
_db_upsert = None


def _load_db():
    global _db, _db_write, _db_upsert
    if _db is None:
        from query import db, db_write, db_upsert
        _db = db
        _db_write = db_write
        _db_upsert = db_upsert


VALID_CATEGORIES = ('fully_agentic', 'mixed', 'human_only')


class AutonomyTracker:

    def __init__(self, db_path: str = None):
        self.db_path = db_path
        self._core = BayesianCore()

    def log_task(self, workflow: str, category: str, details: str = None,
                 agent: str = None) -> int:
        """Log a task execution. Returns task ID.

        Args:
            workflow: e.g., 'callout_writing', 'morning_brief', 'bid_management'
            category: 'fully_agentic', 'mixed', or 'human_only'
            details: Optional description
            agent: Optional agent name that performed the task
        """
        if category not in VALID_CATEGORIES:
            raise ValueError(
                f"Invalid category '{category}'. Must be one of: {VALID_CATEGORIES}"
            )

        _load_db()
        kw = {'db_path': self.db_path} if self.db_path else {}

        rows = _db("SELECT nextval('autonomy_tasks_seq') AS id", **kw)
        task_id = rows[0]['id']

        _db_write(
            "INSERT INTO autonomy_tasks (id, workflow, category, details, agent) "
            "VALUES (?, ?, ?, ?, ?)",
            params=[task_id, workflow, category, details, agent],
            **kw,
        )
        return task_id

    def get_ratios(self, period: str = 'week') -> dict:
        """Current autonomy ratios for the given period.

        Returns dict with pct_fully_agentic, pct_mixed, pct_human_only,
        total_tasks, and per-workflow breakdown.
        """
        _load_db()
        kw = {'db_path': self.db_path} if self.db_path else {}

        if period == 'month':
            interval = "30"
        elif period == 'quarter':
            interval = "90"
        else:
            interval = "7"

        tasks = _db(
            f"SELECT workflow, category, COUNT(*) as cnt "
            f"FROM autonomy_tasks "
            f"WHERE logged_at >= current_timestamp - INTERVAL '{interval}' DAY "
            f"GROUP BY workflow, category",
            **kw,
        )

        if not tasks:
            return {
                'pct_fully_agentic': 0.0,
                'pct_mixed': 0.0,
                'pct_human_only': 0.0,
                'total_tasks': 0,
                'by_workflow': {},
            }

        total = sum(t['cnt'] for t in tasks)
        counts = {'fully_agentic': 0, 'mixed': 0, 'human_only': 0}
        by_workflow = {}

        for t in tasks:
            cat = t['category']
            counts[cat] = counts.get(cat, 0) + t['cnt']
            wf = t['workflow']
            if wf not in by_workflow:
                by_workflow[wf] = {'fully_agentic': 0, 'mixed': 0, 'human_only': 0, 'total': 0}
            by_workflow[wf][cat] += t['cnt']
            by_workflow[wf]['total'] += t['cnt']

        # Compute percentages per workflow
        for wf, data in by_workflow.items():
            wf_total = data['total']
            if wf_total > 0:
                data['pct_fully_agentic'] = data['fully_agentic'] / wf_total * 100
                data['pct_mixed'] = data['mixed'] / wf_total * 100
                data['pct_human_only'] = data['human_only'] / wf_total * 100

        return {
            'pct_fully_agentic': counts['fully_agentic'] / total * 100 if total else 0.0,
            'pct_mixed': counts['mixed'] / total * 100 if total else 0.0,
            'pct_human_only': counts['human_only'] / total * 100 if total else 0.0,
            'total_tasks': total,
            'by_workflow': by_workflow,
        }

    def get_workflow_trajectory(self, workflow: str) -> list:
        """Historical category distribution from autonomy_history."""
        _load_db()
        kw = {'db_path': self.db_path} if self.db_path else {}

        rows = _db(
            f"SELECT * FROM autonomy_history "
            f"WHERE workflow = '{workflow}' ORDER BY week",
            **kw,
        )
        return rows

    def predict_transition(self, workflow: str,
                           target_category: str = 'fully_agentic') -> PredictionResult:
        """Predict when a workflow will reach target category.

        Uses BayesianCore on the historical pct_fully_agentic trajectory
        to estimate weeks until the target percentage is reached.
        """
        trajectory = self.get_workflow_trajectory(workflow)

        if len(trajectory) < 3:
            return PredictionResult(
                question=f"When will {workflow} become {target_category}?",
                market=None, metric=None,
                prediction_type='time_to_target',
                point_estimate=None,
                lower_bound=None, upper_bound=None,
                confidence_level='uncertain',
                confidence_probability=0.3,
                direction=None,
                horizon_weeks=26,
                reasoning=f"Only {len(trajectory)} weeks of data for {workflow}. "
                          f"Need at least 3 for a trajectory prediction.",
            )

        # Build prior from pct_fully_agentic history
        metric_key = f'pct_{target_category}'
        historical = [{metric_key: row.get(metric_key, 0)} for row in trajectory]
        prior = self._core.build_prior(historical, metric_key)
        posterior = self._core.update_posterior(prior, historical[-4:])

        target_pct = 80.0  # consider "reached" at 80%+
        weeks_est, confidence = self._core.time_to_target(posterior, target_pct)

        from .calibrator import Calibrator
        conf_label = Calibrator.confidence_to_language(confidence)

        return PredictionResult(
            question=f"When will {workflow} become {target_category}?",
            market=None, metric=workflow,
            prediction_type='time_to_target',
            point_estimate=target_pct,
            lower_bound=None, upper_bound=None,
            confidence_level=conf_label,
            confidence_probability=confidence,
            direction='up' if prior.trend_slope > 0 else 'flat',
            horizon_weeks=weeks_est,
            reasoning=f"Current {target_category} rate: {posterior.mean:.0f}%. "
                      f"Weekly trend: {prior.trend_slope:+.1f}pp. "
                      f"Estimated ~{weeks_est} weeks to reach {target_pct:.0f}%.",
        )

    def five_levels_position(self) -> dict:
        """Map current autonomy state to Richard's Five Levels framework.

        Level 1: <10% agentic — human does everything
        Level 2: 10-30% agentic — tools assist
        Level 3: 30-60% agentic — mixed execution
        Level 4: 60-85% agentic — mostly autonomous
        Level 5: >85% agentic — fully autonomous
        """
        ratios = self.get_ratios(period='week')
        pct = ratios['pct_fully_agentic']

        if pct < 10:
            level, label = 1, 'Human-driven'
        elif pct < 30:
            level, label = 2, 'Tool-assisted'
        elif pct < 60:
            level, label = 3, 'Mixed execution'
        elif pct < 85:
            level, label = 4, 'Mostly autonomous'
        else:
            level, label = 5, 'Fully autonomous'

        return {
            'level': level,
            'label': label,
            'pct_fully_agentic': pct,
            'pct_mixed': ratios['pct_mixed'],
            'pct_human_only': ratios['pct_human_only'],
            'total_tasks': ratios['total_tasks'],
        }

    def compute_autonomy_snapshot(self, week: str) -> int:
        """Compute and insert weekly snapshot into autonomy_history.

        Returns number of workflow rows inserted/updated.
        """
        _load_db()
        kw = {'db_path': self.db_path} if self.db_path else {}

        # Get per-workflow stats for this week
        tasks = _db(
            f"SELECT workflow, category, COUNT(*) as cnt, "
            f"AVG(quality_score) as avg_quality "
            f"FROM autonomy_tasks "
            f"WHERE strftime(logged_at, '%Y W%W') = '{week}' "
            f"GROUP BY workflow, category",
            **kw,
        )

        if not tasks:
            return 0

        # Aggregate by workflow
        workflows = {}
        for t in tasks:
            wf = t['workflow']
            if wf not in workflows:
                workflows[wf] = {
                    'total': 0, 'fully_agentic': 0, 'mixed': 0, 'human_only': 0,
                    'quality_scores': [],
                }
            workflows[wf][t['category']] += t['cnt']
            workflows[wf]['total'] += t['cnt']
            if t.get('avg_quality') is not None:
                workflows[wf]['quality_scores'].append(t['avg_quality'])

        count = 0
        for wf, data in workflows.items():
            total = data['total']
            avg_q = (sum(data['quality_scores']) / len(data['quality_scores'])
                     if data['quality_scores'] else None)

            pct_a = data['fully_agentic'] / total * 100
            pct_m = data['mixed'] / total * 100
            pct_h = data['human_only'] / total * 100

            # Five levels position for this workflow
            if pct_a < 10:
                fl = 1
            elif pct_a < 30:
                fl = 2
            elif pct_a < 60:
                fl = 3
            elif pct_a < 85:
                fl = 4
            else:
                fl = 5

            _db_upsert('autonomy_history', {
                'week': week,
                'workflow': wf,
                'total_tasks': total,
                'pct_fully_agentic': pct_a,
                'pct_mixed': pct_m,
                'pct_human_only': pct_h,
                'avg_quality_score': avg_q,
                'five_levels_position': fl,
            }, key_cols=['week', 'workflow'], **kw)
            count += 1

        return count
