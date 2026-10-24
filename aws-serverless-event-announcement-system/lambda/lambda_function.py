
import json
import os
import boto3

sns = boto3.client("sns")
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")

        event_name = body.get("event_name")
        event_date = body.get("event_date")
        event_location = body.get("event_location")
        event_description = body.get("event_description", "")

        if not all([event_name, event_date, event_location]):
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": "event_name, event_date and event_location are required"
                })
            }

        message = (
            f"New Event Announcement!\n\n"
            f"Event: {event_name}\n"
            f"Date: {event_date}\n"
            f"Location: {event_location}\n"
            f"Description: {event_description}"
        )

        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"New Event: {event_name}"[:100],
            Message=message
        )

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Announcement published successfully",
                "message_id": response["MessageId"],
                "event_name": event_name
            })
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON request body"})
        }

    except Exception as e:
        print(f"Failed to publish announcement {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "Unable to publish announcement"
            })
        }
