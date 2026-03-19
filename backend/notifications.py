from exponent_server_sdk import (
    PushClient,
    PushMessage,
)


async def send_daily_notifications(app):
    """Called by the cron job daily at 12 PM. Sends a push notification to all active devices."""
    db = app.db

    devices = await db.devices.find({"is_active": True}).to_list(length=None)

    if not devices:
        print("No active devices found, skipping notifications.")
        return

    messages = []
    for device in devices:
        token = device.get("push_token")
        if not token:
            continue

        messages.append(
            PushMessage(
                to=token,
                title="Attendance Regularization",
                body=f"Hi {device.get('user_name', 'there')}! Should I regularize your attendance today?",
                data={"user_id": device["user_id"], "action": "regularize_prompt"},
                category_id="regularize",  # used by Expo to show Yes/No action buttons
            )
        )

    if not messages:
        print("No valid push tokens found.")
        return

    # Send in batches (Expo handles batching internally)
    push_client = PushClient()
    try:
        responses = push_client.publish_multiple(messages)
        for i, response in enumerate(responses):
            try:
                response.validate_response()
            except Exception as e:
                print(f"Failed to send to {messages[i].to}: {e}")
        print(f"Sent {len(messages)} notifications.")
    except Exception as e:
        print(f"Error sending notifications: {e}")
