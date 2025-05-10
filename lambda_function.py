def lambda_handler(event, context):
    for i in range(20):  # Loop 20 times to simulate both success and failure
        try:
            if i < 10:
                # Simulate successful execution (first 10 times)
                result = 10 / 2  # Just an example of a successful operation
                print(f"Success: Operation {i} completed. Result: {result}")
            else:
                # Simulate an error (next 10 times)
                result = 10 / 0  # This will throw a ZeroDivisionError
                print(f"Success: Operation {i} completed. Result: {result}")
        except Exception as e:
            # Log the error to CloudWatch but continue the loop
            print(f"Error occurred at operation {i}: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda function completed with both success and errors')
    }