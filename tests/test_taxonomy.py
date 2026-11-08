from agent.taxonomy import (
    DOCUMENT_SPECS,
    DocumentType,
    InfoGrade,
    needs_human_review,
    round_up_grade,
)


def test_every_document_type_has_spec():
    assert set(DOCUMENT_SPECS) == set(DocumentType)


def test_single_confident_class_is_automatic():
    assert not needs_human_review({DocumentType.CAPITAL_CALL})


def test_ambiguous_or_undetermined_goes_to_human():
    assert needs_human_review({DocumentType.CAPITAL_CALL, DocumentType.CONSENT_REQUEST})
    assert needs_human_review(set())
    assert needs_human_review({DocumentType.UNDETERMINED})


def test_grade_rounds_up():
    assert round_up_grade({InfoGrade.INTERNAL, InfoGrade.RESTRICTED}) is InfoGrade.RESTRICTED
    assert round_up_grade(set()) is InfoGrade.RESTRICTED
