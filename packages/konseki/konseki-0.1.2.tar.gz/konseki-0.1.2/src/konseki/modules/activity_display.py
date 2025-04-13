from typing import Dict, List


def format_event_action(event: dict) -> str:
    event_type = event.get("type", "UnknownEvent")
    repo_name = event.get("repo", {}).get("name", "unknown repository")

    try:
        handlers = {
            "PushEvent": handle_push_event,
            "IssuesEvent": handle_issues_event,
            "WatchEvent": lambda e: "Starred {repo_name}",
            "ForkEvent": lambda e: "Forked {repo_name}",
            "CreateEvent": handle_create_event,
        }

        if event_type in handlers:
            return handlers[event_type](event)
        return default_event_handler(event_type, repo_name)

    except (KeyError, AttributeError):
        return f"Unknown action in {repo_name}"


def handle_push_event(event: dict) -> str:
    repo_name = event["repo"]["name"]
    commit_count = len(event["payload"]["commits"])
    return f"Pushed {commit_count} commit(s) to {repo_name}"


def handle_issues_event(event: dict) -> str:
    action = event["payload"]["action"].capitalize()
    repo_name = event["repo"]["name"]
    return f"{action} an issue in {repo_name}"


def handle_create_event(event: dict) -> str:
    ref_type = event["payload"]["ref_type"]
    repo_name = event["repo"]["name"]
    return f"Created {ref_type} in {repo_name}"


def default_event_handler(event_type: str, repo_name: str) -> str:
    action_type = event_type.replace("Event", "")
    return f"{action_type} in {repo_name}"


def process_events(events: List[Dict]) -> List[str]:
    return [f"- {format_event_action(event)}" for event in events]
