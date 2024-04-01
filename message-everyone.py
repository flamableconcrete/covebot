from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

load_dotenv()

# Initialize Slack WebClient with your API token
slack_token = os.getenv(key="SLACK_API_TOKEN")
client = WebClient(token=slack_token)


def get_channel_id(channel_name):
    try:
        # Fetch the list of channels in the workspace
        response = client.conversations_list(types="private_channel")
        channels = response["channels"]

        # Search for the channel ID by its name
        for channel in channels:
            if channel["name"] == channel_name:
                return channel["id"]

        # If the channel with the given name is not found
        print(f"Channel '{channel_name}' not found.")
        return None

    except SlackApiError as e:
        print(f"Error: {e.response['error']}")
        return None


def post_message_to_channel(channel_id, message):
    try:
        client.chat_postMessage(channel=channel_id, text=message)
        print("Message posted to the channel successfully.")
    except SlackApiError as e:
        print(f"Error posting message to channel: {e.response['error']}")


def send_message_to_user(user, message):
    try:
        user_id = user["id"]

        # Send direct message
        client.chat_postMessage(channel=user_id, text=message)
        print("Message sent to:", user.get("real_name"))
    except SlackApiError as e:
        print(f"Failed to send message to {user['real_name']}: {e.response['error']}")


def get_users():
    users = []
    try:
        response = client.users_list()
        users = response["members"]
    except SlackApiError as e:
        print(f"Failed to get users: {e.response['error']}")
    return users


def filter_active_users(users):
    active_users = []
    for user in users:
        if not user.get("deleted") and not user["is_bot"]:
            active_users.append(user)
    return active_users


def send_message_to_username(users, username, message):
    try:
        for user in users:
            if user["name"] == username:
                client.chat_postMessage(channel=user["id"], text=message)
                print("Message sent to:", user["real_name"])
                return

        print(f"User '{username}' not found.")
    except SlackApiError as e:
        print(f"Failed to send message to user '{username}': {e.response['error']}")


def main():
    all_users = get_users()
    active_users = filter_active_users(users=all_users)

    for user in active_users:
        message = ""
        # print("ID:", user["id"])
        # print("Name:", user.get("real_name"))
        # print("Name:", user["real_name"])
        # print("-------------------------------------")
        send_message_to_user(user=user, message=message)


if __name__ == "__main__":
    main()
