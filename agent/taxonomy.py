"""Closed classification taxonomy for the agent.

Every incoming document, information grade, obligation and alert must fall into
one of these predefined classes. Anything the agent cannot place confidently goes
to UNDETERMINED and is routed to a human reviewer.

The TypeScript mirror lives in web/src/types/taxonomy.ts. Keep both in sync.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DocumentType(str, Enum):
    CAPITAL_CALL = "capital_call"
    DISTRIBUTION_NOTICE = "distribution_notice"
    QUARTERLY_REPORT = "quarterly_report"
    CAPITAL_ACCOUNT_STATEMENT = "capital_account_statement"
    CONSENT_REQUEST = "consent_request"
    OTHER = "other"
    UNDETERMINED = "undetermined"


class InfoGrade(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONTRACTUAL_CONFIDENTIAL = "contractual_confidential"
    RESTRICTED = "restricted"


class ObligationType(str, Enum):
    FUNDING = "funding"
    RESPONSE_CONSENT = "response_consent"
    RIGHT_ELECTION = "right_election"
    TAX_RECLAIM = "tax_reclaim"
    PROXY_VOTE = "proxy_vote"
    UNDETERMINED = "undetermined"


class AlertType(str, Enum):
    DATA_ERROR = "data_error"
    EXPLAINED_MOVE = "explained_move"
    UNEXPLAINED_MOVE = "unexplained_move"


# Grades ordered from least to most sensitive. When uncertain, round up.
GRADE_ORDER: tuple[InfoGrade, ...] = (
    InfoGrade.PUBLIC,
    InfoGrade.INTERNAL,
    InfoGrade.CONTRACTUAL_CONFIDENTIAL,
    InfoGrade.RESTRICTED,
)


@dataclass(frozen=True)
class DocumentSpec:
    definition: str
    required_fields: tuple[str, ...]
    high_risk: bool  # high-risk classes favor recall over precision


DOCUMENT_SPECS: dict[DocumentType, DocumentSpec] = {
    DocumentType.CAPITAL_CALL: DocumentSpec(
        definition="GP request for the LP to fund part of its commitment by a due date.",
        required_fields=("fund_name", "amount", "currency", "due_date", "wire_account", "purpose"),
        high_risk=True,
    ),
    DocumentType.DISTRIBUTION_NOTICE: DocumentSpec(
        definition="GP notice that proceeds are being returned to the LP.",
        required_fields=("fund_name", "amount", "currency", "payment_date", "source"),
        high_risk=False,
    ),
    DocumentType.QUARTERLY_REPORT: DocumentSpec(
        definition="Periodic fund report on portfolio companies and valuations.",
        required_fields=("fund_name", "period_end", "nav", "portfolio_companies"),
        high_risk=False,
    ),
    DocumentType.CAPITAL_ACCOUNT_STATEMENT: DocumentSpec(
        definition="LP-specific ledger: commitment, contributions, distributions, NAV, fees.",
        required_fields=(
            "fund_name", "period_end", "commitment", "contributed_to_date",
            "distributed_to_date", "nav", "management_fee",
        ),
        high_risk=False,
    ),
    DocumentType.CONSENT_REQUEST: DocumentSpec(
        definition="GP request for LP consent or election (extension, amendment, MFN).",
        required_fields=("fund_name", "request_subject", "response_deadline", "default_if_no_response"),
        high_risk=True,
    ),
    DocumentType.OTHER: DocumentSpec(
        definition="Recognized document outside the classes above.",
        required_fields=("fund_name",),
        high_risk=False,
    ),
    DocumentType.UNDETERMINED: DocumentSpec(
        definition="Agent could not classify with sufficient confidence.",
        required_fields=(),
        high_risk=True,
    ),
}


def needs_human_review(prediction_set: set[DocumentType]) -> bool:
    """Route to a human when the conformal prediction set is ambiguous.

    A set with more than one class, an empty set, or any set containing
    UNDETERMINED means the agent must not act on its own.
    """
    return len(prediction_set) != 1 or DocumentType.UNDETERMINED in prediction_set


def round_up_grade(candidates: set[InfoGrade]) -> InfoGrade:
    """When several grades are plausible, apply the most sensitive one."""
    if not candidates:
        return InfoGrade.RESTRICTED
    return max(candidates, key=GRADE_ORDER.index)
