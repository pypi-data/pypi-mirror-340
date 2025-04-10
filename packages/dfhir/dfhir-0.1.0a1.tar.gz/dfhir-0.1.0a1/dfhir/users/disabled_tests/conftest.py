"""Pytest configuration for the nebula app."""

import pytest

from nebula.users.models import User
from nebula.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    """Set the media root to a temporary directory."""
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture()
def user(db) -> User:
    """Return a user instance."""
    return UserFactory()
