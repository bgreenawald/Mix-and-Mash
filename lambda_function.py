import json

from generate import generate


def lambda_handler(event, context):

    print("Got event {}".format(event))

    try:
        body = json.loads(event["body"])

        if "message" in body:
            message = body["message"]
        else:
            return "No input message recieved"

        if "project" in body:
            project = body["project"]
        else:
            return "No project specified."

        memory = body["memory"] if "memory" in body else False
        mechanism = body["mechanism"] if "mechanism" in body else "uniform"

        return {
            "statusCode": 200,
            "body": json.dumps(generate(message, project, memory, mechanism)),
        }
    except (KeyError, TypeError) as e:
        print("Got error " + str(e))
        return {
            "statusCode": 400,
            "body": json.dumps(str(e)),
        }


if __name__ == "__main__":

    # Standard message test case
    print(lambda_handler({"body": json.dumps({
        "message": "I",
        "project": "biblical_trump",
    })}, None))

    # No message test case
    print(lambda_handler({"body": json.dumps({
        "msg": "I",
        "project": "biblical_trump",
    })}, None))

    # Message with memory, but not enough words
    print(lambda_handler({"body": json.dumps({
        "message": "I",
        "project": "biblical_trump",
        "memory": True
    })}, None))

    # Message with memory, but not enough words
    print(lambda_handler({"body": json.dumps({
        "message": "I am",
        "project": "biblical_trump",
        "memory": True
    })}, None))

    # Message with memory and mechanism
    print(lambda_handler({"body": json.dumps({
        "message": "I am",
        "project": "biblical_trump",
        "memory": True,
        "mechanism": "random"
    })}, None))
