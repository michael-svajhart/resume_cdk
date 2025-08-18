import json




def handle_bubbleSort(data):
    old_array = data
    for i, ele in enumerate(data):
        print(f"{index} {ele}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "old_data": old_array,
            "new_data": data,
        })
    }

def handle_insertionSort(data):
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "insertionSort called"})
    }

def handle_heapSort(data):
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "heapSort called"})
    }

def handle_mergeSort(data):
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "mergeSort called"})
    }


def handler(event, context):
    print(f"event: {event}")
    print(f"context: {context}")
    if event.get("body"):
        body = json.loads(event["body"])
        
    data = body.get("data")
    if data == None:
        return {"statusCode": 400, "body": "No data to sort."}

    # print(f"foo={foo}, bar={bar} hello={hello}")
    sort_type = body.get("sortType")
    match sort_type:
        case "bubbleSort":
            return handle_bubbleSort(data)
        case "insertionSort":
            return handle_insertionSort(data)
        case "heapSort":
            return handle_heapSort(data)
        case "mergeSort":
            return handle_mergeSort(data)
        case _:
            return {"statusCode": 400, "body": "Unsupported sort method, current available are bubbleSort, insertionSort, heapSort, and mergeSort"}
        

    # response = {
    #     "status": "success",
    #     "message": "Hello from Lambda!",
    #     "body": body
    # }

    return {
        "statusCode": 501,
        "headers": {"Content-Type": "application/json"},
        "body":"whhhooppps"
    }
