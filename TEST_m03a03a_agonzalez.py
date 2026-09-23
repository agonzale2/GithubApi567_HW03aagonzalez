import pytest
from unittest.mock import Mock, patch

from m03a03a_agonzalez import get_repositories, display_repositories


def create_response(status_code, json_data=None):
    """Create a mock GitHub API response."""
    response = Mock()
    response.status_code = status_code
    response.json.return_value = json_data
    return response


@patch("m03a03a_agonzalez.requests.get")
def test_get_repositories(mock_get):
    """Test successful repository and commit retrieval."""

    mock_get.side_effect = [
        create_response(
            200,
            [
                {"name": "Repository1"},
                {"name": "Repository2"}
            ]
        ),
        create_response(200, [{}, {}, {}]),
        create_response(200, [{}, {}])
    ]

    result = get_repositories("test_user")

    assert result == [
        ("Repository1", 3),
        ("Repository2", 2)
    ]


@patch("m03a03a_agonzalez.requests.get")
def test_invalid_user(mock_get):
    """Test that an invalid user raises an error."""

    mock_get.return_value = create_response(404)

    with pytest.raises(ValueError):
        get_repositories("invalid_user")


@patch("m03a03a_agonzalez.requests.get")
def test_empty_repository(mock_get):
    """Test that an empty repository has zero commits."""

    mock_get.side_effect = [
        create_response(
            200,
            [{"name": "EmptyRepository"}]
        ),
        create_response(409)
    ]

    result = get_repositories("test_user")

    assert result == [("EmptyRepository", 0)]


@patch("m03a03a_agonzalez.get_repositories")
def test_display_repositories(mock_get_repositories, capsys):
    """Test the required output format."""

    mock_get_repositories.return_value = [
        ("Repository1", 10),
        ("Repository2", 27)
    ]

    display_repositories("test_user")

    assert capsys.readouterr().out == (
        "Repo: Repository1 Number of commits: 10\n"
        "Repo: Repository2 Number of commits: 27\n"
    )