# Feature: asana-agent-task-management — Shared fixtures and test generators
# ABPS AI Pipeline property-based testing infrastructure

import random
import string
from datetime import date, timedelta

import hypothesis.strategies as st
from hypothesis import settings

# --- Constants ---

RICHARD_GID = "1212732742544167"

ALLOWED_HTML_TAGS = ["body", "strong", "em", "u", "s", "code", "a", "ul", "ol", "li"]

PIPELINE_STATES = [
    "untriaged", "triaged", "research", "draft", "review",
    "approved", "active", "archived",
]

WORK_PRODUCT_TYPES = ["guide", "reference", "decision", "playbook", "analysis"]

CADENCE_OPTIONS = ["weekly", "monthly", "quarterly", "one-time"]

SECTIONS = ["Intake", "In Progress", "Review", "Active", "Archive"]

ROUTINE_OPTIONS = ["Deep Work", "Admin", "Communication", "Research", "Review"]

PRIORITY_RW_OPTIONS = ["Today", "Urgent", "Not urgent"]

CRITIC_DIMENSIONS = ["usefulness", "clarity", "accuracy", "dual_audience", "economy"]

SUBTASK_PREFIXES = {
    "research": "📋 Research: ",
    "draft": "✏️ Draft: ",
    "review": "🔍 Review: ",
    "approve": "✅ Approve: ",
}


# --- Default hypothesis settings ---

settings.register_profile("default", max_examples=100)
settings.load_profile("default")


# --- Generators (hypothesis strategies) ---

# arbTaskName — generates valid Asana task names (1-200 chars, printable)
arbTaskName = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z"), min_codepoint=32, max_codepoint=126),
    min_size=1,
    max_size=200,
).filter(lambda s: s.strip() != "")


# arbHtmlContent — generates HTML content using only allowed Asana tags
def _html_leaf():
    """Generate a leaf HTML text node or inline-tagged content."""
    return st.one_of(
        # Plain text
        st.text(alphabet=string.ascii_letters + string.digits + " .,;:!?-", min_size=1, max_size=50),
        # <strong>text</strong>
        st.text(alphabet=string.ascii_letters + " ", min_size=1, max_size=30).map(
            lambda t: f"<strong>{t}</strong>"
        ),
        # <em>text</em>
        st.text(alphabet=string.ascii_letters + " ", min_size=1, max_size=30).map(
            lambda t: f"<em>{t}</em>"
        ),
        # <u>text</u>
        st.text(alphabet=string.ascii_letters + " ", min_size=1, max_size=30).map(
            lambda t: f"<u>{t}</u>"
        ),
        # <s>text</s>
        st.text(alphabet=string.ascii_letters + " ", min_size=1, max_size=30).map(
            lambda t: f"<s>{t}</s>"
        ),
        # <code>text</code>
        st.text(alphabet=string.ascii_letters + string.digits + "_-.", min_size=1, max_size=20).map(
            lambda t: f"<code>{t}</code>"
        ),
        # <a href="url">text</a>
        st.tuples(
            st.text(alphabet=string.ascii_letters + string.digits + "/-_.", min_size=5, max_size=30),
            st.text(alphabet=string.ascii_letters + " ", min_size=1, max_size=20),
        ).map(lambda pair: f'<a href="https://{pair[0]}">{pair[1]}</a>'),
    )


def _html_list():
    """Generate an HTML list (ul or ol) with li items."""
    return st.tuples(
        st.sampled_from(["ul", "ol"]),
        st.lists(_html_leaf(), min_size=1, max_size=5),
    ).map(lambda pair: f"<{pair[0]}>" + "".join(f"<li>{item}</li>" for item in pair[1]) + f"</{pair[0]}>")


arbHtmlContent = st.lists(
    st.one_of(_html_leaf(), _html_list()),
    min_size=1,
    max_size=8,
).map(lambda parts: "<body>" + "\n".join(parts) + "</body>")


# arbDate — generates valid YYYY-MM-DD date strings within ±365 days of today
arbDate = st.dates(
    min_value=date.today() - timedelta(days=365),
    max_value=date.today() + timedelta(days=365),
).map(lambda d: d.isoformat())


# arbCadence — generates one of: weekly, monthly, quarterly, one-time
arbCadence = st.sampled_from(CADENCE_OPTIONS)


# arbTask — generates a full mock ABPS AI task object with all fields
arbTask = st.fixed_dictionaries({
    "gid": st.text(alphabet=string.digits, min_size=13, max_size=16),
    "name": arbTaskName,
    "html_notes": arbHtmlContent,
    "assignee": st.fixed_dictionaries({
        "gid": st.just(RICHARD_GID),
    }),
    "start_on": st.one_of(st.none(), arbDate),
    "due_on": st.one_of(st.none(), arbDate),
    "completed": st.booleans(),
    "resource_subtype": st.just("default_task"),
    "section": st.sampled_from(SECTIONS),
    "custom_fields": st.fixed_dictionaries({
        "Routine": st.one_of(st.none(), st.sampled_from(ROUTINE_OPTIONS)),
        "Priority_RW": st.one_of(st.none(), st.sampled_from(PRIORITY_RW_OPTIONS)),
        "Frequency": st.one_of(st.none(), st.sampled_from(CADENCE_OPTIONS)),
        "Kiro_RW": st.one_of(st.none(), st.text(min_size=0, max_size=200)),
    }),
    "work_product_type": st.one_of(st.none(), st.sampled_from(WORK_PRODUCT_TYPES)),
    "subtasks": st.lists(
        st.fixed_dictionaries({
            "name": st.text(min_size=1, max_size=100),
            "completed": st.booleans(),
            "resource_subtype": st.sampled_from(["default_task", "approval"]),
        }),
        min_size=0,
        max_size=4,
    ),
})


# arbCriticScore — generates a dict of 5 dimension scores (1-10 each)
arbCriticScore = st.fixed_dictionaries({
    dim: st.integers(min_value=1, max_value=10)
    for dim in CRITIC_DIMENSIONS
})


# arbPipelineState — generates a valid pipeline state string
arbPipelineState = st.sampled_from(PIPELINE_STATES)


# arbAssigneeGid — generates either Richard's GID or a random GID
arbAssigneeGid = st.one_of(
    st.just(RICHARD_GID),
    st.text(alphabet=string.digits, min_size=13, max_size=16).filter(
        lambda g: g != RICHARD_GID
    ),
)
