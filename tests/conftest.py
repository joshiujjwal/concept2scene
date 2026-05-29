"""Shared pytest fixtures for concept2scene tests."""
from __future__ import annotations

import pytest


@pytest.fixture
def sample_concept() -> str:
    """A valid concept string for testing."""
    return "The silence after a lighthouse keeper realizes the ships have stopped coming"


@pytest.fixture
def sample_concept_short() -> str:
    """A minimal valid concept."""
    return "loneliness"
