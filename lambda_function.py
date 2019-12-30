import json

from generate import generate


def lambda_handler(event, context):

    print("Got event {}".format(event))

    try:
        body = json.loads(event["body"])

        if "message" in body:
            message = body["message"]
        else:
            return {
                "statusCode": 400,
                "body": json.dumps("No input message recieved"),
            }

        if "project" in body:
            project = body["project"]
        else:
            return {
                "statusCode": 400,
                "body": json.dumps("No project specified."),
            }

        memory = body.get("memory", False)
        mechanism = body.get("mechanism", "uniform")

        try:
            message = generate(message, project, memory, mechanism)
            return {
                "statusCode": 200,
                "body": json.dumps(message),
            }
        except (KeyError, ValueError) as e:
            return {
                "statusCode": 400,
                "body": json.dumps(str(e))
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

    # No word test case
    print(lambda_handler({"body": json.dumps({
        "message": "",
        "project": "biblical_trump",
    })}, None))

    # Message with memory, but not enough words
    print(lambda_handler({"body": json.dumps({
        "message": "I",
        "project": "biblical_trump",
        "memory": True
    })}, None))

    # Message with memory
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

    # Message with no memory and multiple words
    print(lambda_handler({"body": json.dumps({
        "message": "I am",
        "project": "biblical_trump",
        "memory": False,
    })}, None))