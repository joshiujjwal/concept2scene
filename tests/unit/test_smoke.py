"""Smoke test — confirms pytest is wired up correctly."""


def test_smoke() -> None:
    """The test suite runs."""
    assert 1 == 1


def test_imports() -> None:
    """Core Python stdlib imports work."""
    import uuid
    from datetime import UTC, datetime

    uid = uuid.uuid4()
    now = datetime.now(UTC)

    assert uid is not None
    assert now is not None
