# GitHub API Repository and Commit Counter — HW 03b Mocking

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/agonzale2/GithubApi567_HW03aagonzalez/tree/HW03b_Mocking.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/agonzale2/GithubApi567_HW03aagonzalez/tree/HW03b_Mocking)

This Python application accepts a GitHub user ID and displays the names of the user's public repositories along with the number of commits in each repository.

## Mock Testing

The automated tests use Python's `unittest.mock` module to replace calls to the GitHub API with controlled mock responses. This ensures that the tests produce consistent results without depending on live GitHub data or exceeding API request limits.

The tests cover:

- Successful repository and commit retrieval
- Invalid GitHub users
- Repositories with no commits
- The required output format

## Requirements

- Python 3.x
- requests
- pytest

## Run the Application

```bash
python m03a03a_agonzalez.py