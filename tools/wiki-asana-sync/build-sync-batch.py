#!/usr/bin/env python3
"""
Build the batch of Asana task creation commands for wiki sync.
Reads wiki-index.md, extracts article metadata, and outputs
the task creation parameters for each article.

This script generates a JSON file that can be consumed by
the sync executor.
"""

import json
import re
import os
import sys

# Section GIDs
SECTIONS = {
    "Intake": "1213917352480612",
    "In Progress": "1213917923741223",
    "Review": "1213917923779848",
    "Active": "1213917968512184",
    "Archive": "1213917833240629"
}

# Custom field GIDs
FIELDS = {
    "Routine_RW": "1213608836755502",
    "Priority_RW": "1212905889837829",
    "Kiro_RW": "1213915851848087",
    "Next-action_RW": "1213921400039514",
    "File_Path": "1213917488341150",
    "Frequency": "1213921303350613",
    "Category": "1213917488341137",
    "Five_Levels": "1213917488341130",
    "Audience": "1213917488341145",
}

# Enum option GIDs
ROUTINE_WIKI = "1213924412583429"
PRIORITY_NOT_URGENT = "1212905889837833"
PRIORITY_URGENT = "1212905889837831"

FREQ_ONE_TIME = "1213921303350614"
FREQ_WEEKLY = "1213921303350615"
FREQ_MONTHLY = "1213921303350616"
FREQ_QUARTERLY = "1213921303350617"

CAT_TESTING = "1213917488341138"
CAT_STRATEGY = "1213917488341139"
CAT_PROGRAM = "1213917488341140"
CAT_TOOLS = "1213917488341141"
CAT_COMMUNICATION = "1213917488341142"
CAT_BEST_PRACTICES = "1213917488341143"

AUDIENCE_INTERNAL = "1213917488341146"
AUDIENCE_PERSONAL = "1213917488341147"

LEVEL_L1 = "1213917488341131"
LEVEL_L2 = "1213917488341132"
LEVEL_L3 = "1213917488341133"
LEVEL_L4 = "1213917488341134"
LEVEL_L5 = "1213917488341135"

# Articles that need revision (critic scored <8)
NEEDS_REVISION = {
    "au-market-wiki", "enhanced-match-liveramp",
    "f90-lifecycle-strategy", "ad-copy-testing-framework",
    "email-overlay-ww-rollout", "ai-max-test-design",
    "campaign-link-generator-spec", "budget-forecast-helper-spec",
    "q2-initiative-status", "team-workload-distribution",
    "polaris-rollout-status", "project-baloo-overview",
    "mx-market-wiki"
}

# Map category folder to Category enum GID
FOLDER_TO_CAT = {
    "testing": CAT_TESTING,
    "strategy": CAT_STRATEGY,
    "program-details": CAT_PROGRAM,
    "tools": CAT_TOOLS,
    "communication": CAT_COMMUNICATION,
    "best-practices": CAT_BEST_PRACTICES,
    "reporting": CAT_TESTING,  # no reporting enum, use testing
}

# Map level string to Five Levels enum GID
LEVEL_MAP = {
    "1": LEVEL_L1, "L1": LEVEL_L1,
    "2": LEVEL_L2, "L2": LEVEL_L2,
    "3": LEVEL_L3, "L3": LEVEL_L3,
    "4": LEVEL_L4, "L4": LEVEL_L4,
    "5": LEVEL_L5, "L5": LEVEL_L5,
}


def parse_frontmatter(filepath):
    """Extract YAML frontmatter from a markdown file."""
    meta = {}
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return meta, ""
    
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            fm = content[3:end]
            for line in fm.strip().split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    meta[key.strip()] = val.strip().strip('"').strip("'")
            body = content[end+3:]
        else:
            body = content
    else:
        body = content
    
    return meta, body


def determine_section(slug, meta):
    """Determine which Asana section based on article state."""
    if slug in NEEDS_REVISION:
        return SECTIONS["Review"]
    return SECTIONS["Active"]


def determine_frequency(meta):
    """Determine update frequency from frontmatter."""
    trigger = meta.get('update-trigger', '').lower()
    if 'weekly' in trigger:
        return FREQ_WEEKLY
    elif 'monthly' in trigger or 'mbr' in trigger:
        return FREQ_MONTHLY
    elif 'quarterly' in trigger or 'qbr' in trigger:
        return FREQ_QUARTERLY
    return FREQ_ONE_TIME


def determine_audience(meta):
    """Determine audience from frontmatter."""
    audience = meta.get('audience', 'amazon-internal').lower()
    if 'personal' in audience:
        return AUDIENCE_PERSONAL
    return AUDIENCE_INTERNAL


def determine_level(meta):
    """Determine Five Levels from frontmatter."""
    level = meta.get('level', 'N/A')
    if level in LEVEL_MAP:
        return [LEVEL_MAP[level]]
    # Try extracting number
    match = re.search(r'(\d)', str(level))
    if match and match.group(1) in LEVEL_MAP:
        return [LEVEL_MAP[match.group(1)]]
    return []


def build_article_list():
    """Scan artifacts directory and build article metadata."""
    artifacts_dir = os.path.expanduser("~/shared/artifacts")
    articles = []
    
    for category in os.listdir(artifacts_dir):
        cat_path = os.path.join(artifacts_dir, category)
        if not os.path.isdir(cat_path):
            continue
        if category in ('grok-swarm', 'weekly-ships', 'frameworks'):
            continue
            
        for filename in sorted(os.listdir(cat_path)):
            if not filename.endswith('.md'):
                continue
            if filename in ('README.md', 'SITEMAP.md', '.gitkeep'):
                continue
                
            filepath = os.path.join(cat_path, filename)
            meta, body = parse_frontmatter(filepath)
            
            # Skip archived files
            if body.strip().startswith('> **') and 'ARCHIVED' in body[:200]:
                continue
            
            title = meta.get('title', filename.replace('.md', '').replace('-', ' ').title())
            slug = meta.get('slug', filename.replace('.md', ''))
            doc_type = meta.get('doc-type', 'strategy')
            
            articles.append({
                'title': title,
                'slug': slug,
                'filename': filename,
                'category': category,
                'filepath': f"~/shared/artifacts/{category}/{filename}",
                'doc_type': doc_type,
                'level': meta.get('level', 'N/A'),
                'audience': meta.get('audience', 'amazon-internal'),
                'frequency': determine_frequency(meta),
                'section': determine_section(slug, meta),
                'category_gid': FOLDER_TO_CAT.get(category, CAT_STRATEGY),
                'audience_gid': determine_audience(meta),
                'level_gids': determine_level(meta),
                'meta': meta,
            })
    
    return articles


if __name__ == '__main__':
    articles = build_article_list()
    
    print(f"Found {len(articles)} articles to sync:")
    for a in articles:
        section_name = [k for k, v in SECTIONS.items() if v == a['section']][0]
        print(f"  [{section_name:12s}] {a['title'][:60]:60s} ({a['category']})")
    
    # Write to JSON for the sync executor
    output_path = os.path.expanduser("~/shared/tools/wiki-asana-sync/sync-batch.json")
    with open(output_path, 'w') as f:
        json.dump(articles, f, indent=2)
    
    print(f"\nWrote {len(articles)} articles to {output_path}")
