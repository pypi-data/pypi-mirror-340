import argparse

from konseki.modules.activity_display import process_events
from konseki.modules.github_api import GitHubAPIError, get_github_activity_events


def main():
    parser = argparse.ArgumentParser(
        description="Display GitHub user activity summary."
    )
    parser.add_argument("username", type=str, help="GitHub username")
    args = parser.parse_args()

    try:
        events = get_github_activity_events(args.username)
        formatted_events = process_events(events)

        if not formatted_events:
            print("No recent activity found.")
            return

        print("\nRecent GitHub Activity")
        print("\n".join(formatted_events))

    except GitHubAPIError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Operation cancelled by user.")


if __name__ == "__main__":
    main()
