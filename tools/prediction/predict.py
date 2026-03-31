#!/usr/bin/env python3
"""CLI entry point for the Bayesian Prediction Engine.

Usage:
    python3 predict.py "Will AU regs be up next week?"
    python3 predict.py --market AU --metric regs --horizon 1
    python3 predict.py --calibrate
    python3 predict.py --autonomy
    python3 predict.py --log-task callout_writing --category mixed
"""

import sys
import os
import argparse

# Ensure prediction package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.expanduser('~/shared/tools/data'))


def main():
    parser = argparse.ArgumentParser(
        description='Bayesian Prediction Engine — PS Analytics',
    )
    parser.add_argument(
        'question', nargs='?', default=None,
        help='Natural-language prediction question',
    )
    parser.add_argument('--market', help='Market code (AU, MX, US, etc.)')
    parser.add_argument('--metric', help='Metric name (regs, spend, cpa, cvr, clicks, cpc)')
    parser.add_argument('--horizon', type=int, default=1, help='Horizon in weeks (default: 1)')
    parser.add_argument('--calibrate', action='store_true', help='Run calibration')
    parser.add_argument('--calibrate-week', help='Specific week to calibrate (e.g., "2026 W14")')
    parser.add_argument('--autonomy', action='store_true', help='Show autonomy ratios')
    parser.add_argument('--log-task', metavar='WORKFLOW', help='Log an autonomy task')
    parser.add_argument('--category', help='Task category (fully_agentic, mixed, human_only)')
    parser.add_argument('--agent', help='Agent name for --log-task')
    parser.add_argument('--details', help='Details for --log-task')
    parser.add_argument('--consumer', default='human', choices=['human', 'agent'],
                        help='Output format (default: human)')
    parser.add_argument('--db', default=None, help='Database path override')

    args = parser.parse_args()

    from prediction.engine import PredictionEngine
    from prediction.autonomy import AutonomyTracker

    engine = PredictionEngine(db_path=args.db)

    # --- Calibrate mode ---
    if args.calibrate or args.calibrate_week:
        week = args.calibrate_week
        report = engine.calibrate(week=week)
        print(f"Calibration complete.")
        print(f"  Scored predictions: {report.total_scored}")
        print(f"  Direction accuracy: {report.direction_accuracy:.0%}")
        print(f"  Interval coverage:  {report.interval_coverage:.0%}")
        print(f"  Mean error:         {report.mean_error_pct:.1f}%")
        print(f"  Calibration score:  {report.calibration_score:.2f}")
        print(f"  Confidence adjust:  {report.confidence_adjustment:.2f}")
        if report.tier_breakdown:
            print(f"  Tiers:")
            for tier, data in report.tier_breakdown.items():
                print(f"    {tier}: {data['count']} predictions, "
                      f"hit rate {data.get('hit_rate', 0):.0%}")
        return

    # --- Autonomy mode ---
    if args.autonomy:
        tracker = AutonomyTracker(db_path=args.db)
        ratios = tracker.get_ratios()
        position = tracker.five_levels_position()
        print(f"Autonomy — Level {position['level']}: {position['label']}")
        print(f"  Fully agentic: {ratios['pct_fully_agentic']:.1f}%")
        print(f"  Mixed:         {ratios['pct_mixed']:.1f}%")
        print(f"  Human-only:    {ratios['pct_human_only']:.1f}%")
        print(f"  Total tasks:   {ratios['total_tasks']}")
        if ratios.get('by_workflow'):
            print(f"  By workflow:")
            for wf, data in ratios['by_workflow'].items():
                print(f"    {wf}: {data.get('pct_fully_agentic', 0):.0f}% agentic "
                      f"({data['total']} tasks)")
        return

    # --- Log task mode ---
    if args.log_task:
        if not args.category:
            print("Error: --category required with --log-task", file=sys.stderr)
            sys.exit(1)
        tracker = AutonomyTracker(db_path=args.db)
        task_id = tracker.log_task(
            workflow=args.log_task,
            category=args.category,
            details=args.details,
            agent=args.agent,
        )
        print(f"Logged task {task_id}: {args.log_task} ({args.category})")
        return

    # --- Structured prediction (--market + --metric) ---
    if args.market and args.metric:
        result = engine.predict_metric(
            market=args.market,
            metric=args.metric,
            horizon_weeks=args.horizon,
            consumer=args.consumer,
        )
        _print_result(result, args.consumer)
        return

    # --- Natural language prediction ---
    if args.question:
        context = {}
        if args.market:
            context['market'] = args.market
        if args.metric:
            context['metric'] = args.metric
        if args.horizon != 1:
            context['horizon_weeks'] = args.horizon

        result = engine.predict(
            question=args.question,
            consumer=args.consumer,
            context=context if context else None,
        )
        _print_result(result, args.consumer)
        return

    parser.print_help()


def _print_result(result, consumer):
    """Print prediction result to stdout."""
    if consumer == 'agent':
        import json
        output = result.formatted_output
        if isinstance(output, dict):
            print(json.dumps(output, indent=2, default=str))
        else:
            print(output)
    else:
        print(result.formatted_output or result.reasoning)


if __name__ == '__main__':
    main()
