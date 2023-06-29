from botocore.exceptions import ClientError
import json
from models.SectionContent import SectionContent
from pynamodb.exceptions import DoesNotExist
from typing import Dict, Any


def handler(event: Dict[str, Any], _: Any) -> Dict[str, Any]:
    try:
        # Check that the request is a PUT request
        if event["requestContext"]["httpMethod"] != "PUT":
            return {"statusCode": 405}

        # Extract body parameters from HTTP request
        request_body = json.loads(event['body'])
        user_id = request_body['userId']
        section = request_body['section']
        content = request_body['content']

        if SectionContent.count(user_id) > 0: # update existing entry
            cur_user_info = SectionContent.get(user_id)
            status_code = 200
        else: # add new entry
            cur_user_info = SectionContent(user_id)
            status_code = 201

        setattr(cur_user_info, section, content)
        cur_user_info.save()

        return {
            "statusCode": status_code,
            "body": json.dumps({"section": section, "content": content})
        }

    except (KeyError, TypeError, AttributeError):
        return {"statusCode": 400}

    except DoesNotExist:
        return {"statusCode": 404}

    except ClientError:
        return {"statusCode": 500}
