from botocore.exceptions import ClientError
import json
from models.SectionContent import SectionContent
from pynamodb.exceptions import DoesNotExist
from typing import Dict, Any


def handler(event: Dict[str, Any], _: Any) -> Dict[str, Any]:
    try:
        # Check that the request is a GET request
        if event["requestContext"]["httpMethod"] != "GET":
            return {"statusCode": 405}

        # Extract body parameters from HTTP request
        query_parameters = event['queryStringParameters']
        user_id = query_parameters['userId']
        section = query_parameters['section']

        if SectionContent.count(user_id) > 0:  # existing entry
            cur_user_info = SectionContent.get(user_id)
            content = getattr(cur_user_info, section)
        else: # no entry for this user yet
            content = ""

        return {
            "statusCode": 200,
            "body": json.dumps({"section": section, "content": content})
        }

    except (KeyError, TypeError, AttributeError):
        return {"statusCode": 400}

    except DoesNotExist:
        return {"statusCode": 404}

    except ClientError:
        return {"statusCode": 500}
