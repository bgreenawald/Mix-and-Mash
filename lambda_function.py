from generate import generate

def lambda_handler(event, context):
    if "message" in event:
        message = event["message"]
    else:
        return "No input message recieved"

    if "project" in event:
        project = event["project"]
    else:
        return "No project specified."

    memory = event["memory"] if "memory" in event else False
    mechanism = event["mechanism"] if "mechanism" in event else "uniform"

    return generate(message, project, memory, mechanism)


if __name__=="__main__":
    # Standard message test case
    print(lambda_handler({
        "message": "I",
        "project": "biblical_trump",
    }, None))

    # No message test case
    print(lambda_handler({
        "msg": "I",
        "project": "biblical_trump",
    }, None))

    # Message with memory, but not enough words
    print(lambda_handler({
        "message": "I",
        "project": "biblical_trump",
        "memory": True
    }, None))

    # Message with memory, but not enough words
    print(lambda_handler({
        "message": "I am",
        "project": "biblical_trump",
        "memory": True
    }, None))

    # Message with memory and mechanism
    print(lambda_handler({
        "message": "I am",
        "project": "biblical_trump",
        "memory": True,
        "mechanism": "random"
    }, None))