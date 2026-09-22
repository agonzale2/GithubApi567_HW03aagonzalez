import requests
import json


def get_repositories(github_user_id):
    """Return repository names and commit counts for a GitHub user."""

    repo_url = f"https://api.github.com/users/{github_user_id}/repos"
    response = requests.get(repo_url, timeout=10)

    if response.status_code != 200:
        raise ValueError(f"Unable to find GitHub user: {github_user_id}")

    repositories = response.json()
    results = []

    for repository in repositories:
        repository_name = repository["name"]

        commits_url = (
            f"https://api.github.com/repos/"
            f"{github_user_id}/{repository_name}/commits"
        )

        commits_response = requests.get(commits_url, timeout=10)

        if commits_response.status_code == 409:
            commit_count = 0
        elif commits_response.status_code != 200:
            raise ValueError(
                f"Unable to retrieve commits for {repository_name}"
            )
        else:
            commits = commits_response.json()
            commit_count = len(commits)

        results.append((repository_name, commit_count))

    return results


def display_repositories(github_user_id):
    """Display each repository name and its number of commits."""

    results = get_repositories(github_user_id)

    for repository_name, commit_count in results:
        print(f"Repo: {repository_name} Number of commits: {commit_count}")


if __name__ == "__main__":
    github_user_id = input("Enter a GitHub user ID: ")

    try:
        display_repositories(github_user_id)
    except (ValueError, requests.RequestException) as error:
        print(f"Error: {error}")
