from copy import deepcopy

from crawl4ai.utils import attach_extraction_provenance


def test_attaches_normalized_provenance_to_nested_records():
    records = [{"title": "outer", "details": {"value": 3}}]

    annotated = attach_extraction_provenance(
        records,
        "  HTTPS://Example.COM/article?utm_source=test&b=2&a=1#section  ",
        "2026-01-02T03:04:05+00:00",
    )

    expected_url = "https://example.com/article?a=1&b=2"
    assert annotated[0]["source_url"] == expected_url
    assert annotated[0]["extracted_at"] == "2026-01-02T03:04:05+00:00"
    assert annotated[0]["details"]["source_url"] == expected_url
    assert annotated[0]["details"]["extracted_at"] == "2026-01-02T03:04:05+00:00"


def test_missing_source_url_is_recorded_as_none():
    annotated = attach_extraction_provenance({"title": "unattributed"}, None, "2026-01-02T03:04:05Z")

    assert annotated["source_url"] is None
    assert annotated["extracted_at"] == "2026-01-02T03:04:05+00:00"


def test_does_not_mutate_caller_input():
    records = [{"title": "original", "nested": {"value": 1}}]
    original = deepcopy(records)

    annotated = attach_extraction_provenance(records, "https://example.com/page", "2026-01-02T03:04:05+00:00")

    assert records == original
    assert "source_url" not in records[0]
    assert "extracted_at" not in records[0]["nested"]
    assert annotated is not records
    assert annotated[0] is not records[0]
