import requests

GITHUB_EVENTS_URL = "https://api.github.com/users/{username}/events"


class GitHubAPIError(Exception):
    pass


def get_github_activity_events(username):
    url = GITHUB_EVENTS_URL.format(username=username)
    response = requests.get(url)

    if not response.ok:
        handle_api_errors(response.status_code)

    return response.json()


def handle_api_errors(status_code: int) -> None:
    error_messages = {
        404: "User not found. Please check the username.",
        403: "API rate limit exceeded.",
        500: "GitHub server error.",
    }

    raise GitHubAPIError(error_messages.get(status_code, "Error fetching data."))
