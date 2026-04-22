/**
 * Provenance registry — maps dashboard sections to their producers.
 *
 * Source of truth for "who made this?" metadata used by the leadership demo.
 * Each entry describes which agents/hooks/humans contributed to a given
 * dashboard section. Pulled from body/device.md + hook protocols.
 *
 * When a new agent or hook starts producing content for the dashboard,
 * add it here. The dashboard renders whatever is here.
 */

(function () {
  'use strict';

  const REGISTRY = {
    // Command Center — main index.html
    'sec-blocks': {
      provs: [
        { type: 'agent', producer: 'AM Backend', detail: 'Parallel ingestion of Asana tasks, priorities, and Next-action_RW fields (6 subagents)' },
        { type: 'agent', producer: 'EOD Backend', detail: 'Asana reconciliation, recurring task rollover, completion moves' },
        { type: 'human', producer: 'Richard', detail: 'Sets bucket caps and cadence rules via command-center protocol' },
      ],
      trace: 'https://code.amazon.com/',
    },
    'sec-ledger': {
      provs: [
        { type: 'agent', producer: 'Signal Extractor', detail: 'Hedy + Slack + email signal parsing → commitment detection' },
        { type: 'reviewed', producer: 'Richard-approved', detail: 'Commitments surface here only after appearing in a reviewed source' },
      ],
    },
    'sec-intel': {
      provs: [
        { type: 'agent', producer: 'Karpathy', detail: 'Surfaces differentiated/delegate/communicate items via leverage framework' },
        { type: 'agent', producer: 'aMCC', detail: 'Avoidance detection and hard-thing surfacing' },
      ],
    },

    // Hero — WBR health score
    'wbr-hero': {
      provs: [
        { type: 'agent', producer: 'WBR Pipeline', detail: '3-agent pipeline: market-analyst → callout-writer → callout-reviewer; composite quality score' },
        { type: 'agent', producer: 'Hard-gates', detail: 'Quality gate enforcement — blocks markets failing structural checks' },
      ],
    },

    // Performance tab
    'perf-forecast': {
      provs: [
        { type: 'agent', producer: 'Bayesian Projector', detail: 'Seasonal priors + regime change adjustments + weighted prediction decay (λ=0.2)' },
        { type: 'agent', producer: 'Regime Detector', detail: 'Scans ps.change_log for structural market changes' },
      ],
    },

    // State files
    'state-au': {
      provs: [
        { type: 'agent', producer: 'AU Analyst', detail: 'Daily engine: trailing-week metrics + anomaly flags' },
        { type: 'agent', producer: 'WBR Pipeline', detail: 'Weekly: prediction scoring, forward forecast with CI, vs-OP2 pacing' },
        { type: 'human', producer: 'Richard', detail: 'Active initiatives, open items, stakeholder context' },
      ],
    },
    'state-mx': {
      provs: [
        { type: 'agent', producer: 'MX Analyst', detail: 'Daily engine: trailing-week metrics + anomaly flags' },
        { type: 'agent', producer: 'WBR Pipeline', detail: 'Weekly: prediction scoring, forward forecast with CI, vs-OP2 pacing' },
        { type: 'human', producer: 'Richard', detail: 'Active initiatives, open items, stakeholder context' },
      ],
    },
    'state-ww': {
      provs: [
        { type: 'agent', producer: 'WW Aggregator', detail: 'Synthesizes 10 market callouts into WW narrative' },
        { type: 'agent', producer: 'WBR Pipeline', detail: 'Underlying per-market analysis' },
      ],
    },

    // Body System tab
    'agent-health': {
      provs: [
        { type: 'agent', producer: 'Body System Refresher', detail: 'Queries ops.hook_executions + workflow_executions + agent_invocations' },
        { type: 'human', producer: 'Richard', detail: 'Success metric definitions' },
      ],
    },

    // Wiki search
    'wiki-pipeline': {
      provs: [
        { type: 'agent', producer: 'Wiki Team', detail: '6 agents: editor → researcher → writer → critic → librarian + concierge' },
        { type: 'reviewed', producer: 'Critic-gated', detail: 'No article publishes without 8/10 critic score' },
        { type: 'human', producer: 'Richard', detail: 'Editorial direction, topic priorities' },
      ],
    },
  };

  window.ProvenanceRegistry = {
    get: (key) => REGISTRY[key] || null,
    all: () => REGISTRY,
    /**
     * Apply provenance bars to all registered sections on the current page.
     * Call after the page renders its section labels.
     */
    applyAll: () => {
      if (!window.Provenance) return;
      for (const [sectionId, config] of Object.entries(REGISTRY)) {
        if (document.getElementById(sectionId)) {
          window.Provenance.injectBar(sectionId, config.provs, config.trace);
        }
      }
    },
  };
})();
