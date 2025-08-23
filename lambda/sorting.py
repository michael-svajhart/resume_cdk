import json




def handle_bubbleSort(data):
    n = len(data)
    
    # Traverse through all array elements
    for i in range(n):
        swapped = False

        # Last i elements are already in place
        for j in range(0, n-i-1):

            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                swapped = True
        if (swapped == False):
            break


    return {
        "statusCode": 200, 
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Or specific origin like "https://www.example.com"
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token",
        },
        "body": json.dumps({
            "data": data,
        })
    }

def handle_insertionSort(data):
    return {
        "statusCode": 200, 
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Or specific origin like "https://www.example.com"
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token",
        },
        "body": json.dumps({
            "data": data,
        })
    }

def handle_heapSort(data):
    return {
        "statusCode": 200, 
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Or specific origin like "https://www.example.com"
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token",
        },
        "body": json.dumps({
            "data": data,
        })
    }


def handle_mergeSort(data):
    return {
        "statusCode": 200, 
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Or specific origin like "https://www.example.com"
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token",
        },
        "body": json.dumps({
            "data": data,
        })
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
