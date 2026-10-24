# AWS Serverless Event Announcement System

## Project Overview
This project implements a serverless event announcement system using AWS services. An organizer sends event details through an API, AWS Lambda processes the request, and Amazon SNS distributes the announcement to subscribed email addresses.

The project demonstrates how AWS services can work together to build a simple, event-driven notification application without managing servers.

## AWS Services Used

| Service            | Purpose                                             |

| ------------------ | --------------------------------------------------- |

| Amazon API Gateway | Receives HTTP POST requests                         |

| AWS Lambda         | Validates event details and publishes announcements |

| Amazon SNS         | Distributes announcements to email subscribers      |

| AWS IAM            | Controls permissions for Lambda                     |

| Amazon CloudWatch  | Stores Lambda execution logs                        |


## Features
- Accepts event details through a REST API.
- Validates required event fields.
- Publishes announcements through Amazon SNS.
- Sends notifications to confirmed email subscribers.
- Returns a JSON response with the SNS message ID.
- Uses IAM permissions to control access to SNS.
- Uses CloudWatch logs for troubleshooting.

## Sample Event Request

```json
{

&#x20; "event\_name": "AWS and DevOps Workshop",

&#x20; "event\_date": "2026-11-15",

&#x20; "event\_location": "Bengaluru",

&#x20; "event\_description": "A beginner-friendly AWS and DevOps workshop."

}

```

## Testing
The application was tested using Postman.
- HTTP method: `POST`
- Resource path: `/announce`
- Result: `200 OK`
- Notification delivery: Verified through the subscribed email inbox.

Screenshots of the AWS configuration and successful test are available in the `screenshots/` directory.

## Security Notes
- Do not commit AWS access keys, secret keys, credentials, or private configuration files.
- The API should be protected with suitable authentication before being used beyond controlled testing.
- Lambda should have only the permissions required for its tasks.
- Avoid sharing screenshots that expose personal information or sensitive account details.

## Cleanup
AWS resources may incur charges depending on usage and pricing. Refer to `cleanup.md` for instructions to remove resources created for this project when they are no longer needed.

## Learning Outcomes
- Understanding serverless architecture on AWS.
- Integrating API Gateway with Lambda.
- Publishing messages using Amazon SNS.
- Configuring IAM permissions.
- Testing APIs with Postman.
- Troubleshooting AWS errors using CloudWatch logs.

## Project Status
Completed and tested as a learning and portfolio project.



