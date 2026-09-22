import pytest
from unittest.mock import Mock

import m03a03a_agonzalez as github_api


def mock_requests(monkeypatch, *responses):
    """Create and install mock GitHub API responses."""
    mock_get = Mock()

    mock_get.side_effect = [
        Mock(status_code=status, json=lambda data=data: data)
        for status, data in responses
    ]

    monkeypatch.setattr(github_api.requests, "get", mock_get)


def test_get_repositories(monkeypatch):
    mock_requests(
        monkeypatch,
        (200, [{"name": "Repository1"}, {"name": "Repository2"}]),
        (200, [{}, {}, {}]),
        (200, [{}, {}])
    )

    assert github_api.get_repositories("test_user") == [
        ("Repository1", 3),
        ("Repository2", 2)
    ]


def test_invalid_user(monkeypatch):
    mock_requests(monkeypatch, (404, None))

    with pytest.raises(ValueError):
        github_api.get_repositories("invalid_user")


def test_empty_repository(monkeypatch):
    mock_requests(
        monkeypatch,
        (200, [{"name": "EmptyRepository"}]),
        (409, None)
    )

    assert github_api.get_repositories("test_user") == [
        ("EmptyRepository", 0)
    ]


def test_display_repositories(monkeypatch, capsys):
    monkeypatch.setattr(
        github_api,
        "get_repositories",
        lambda user: [("Repository1", 10), ("Repository2", 27)]
    )

    github_api.display_repositories("test_user")

    assert capsys.readouterr().out == (
        "Repo: Repository1 Number of commits: 10\n"
        "Repo: Repository2 Number of commits: 27\n"
    )