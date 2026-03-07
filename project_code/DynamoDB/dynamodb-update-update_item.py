response = client.update_item(
    TableName='ExamMarks',
    Key={
        'roll_no': {'N': '101'},
        'subject_cd': {'S': 'MATH-101'}
    },
    # SET new value for marks, ADD a new tag to a list
    UpdateExpression="SET marks = :m, remarks = :r", 
    ExpressionAttributeValues={
        ':m': {'N': '98'},
        ':r': {'S': 'Improved significantly'}
    },
    ReturnValues="UPDATED_NEW" # Returns only the updated attributes
)
