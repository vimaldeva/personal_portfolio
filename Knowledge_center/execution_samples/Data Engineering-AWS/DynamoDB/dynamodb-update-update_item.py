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


update_item (Modify specific fields) :

Unlike put_item (which replaces the whole item), update_item allows you to change just one attribute (e.g., update marks) while leaving the rest (e.g., student name) alone. It also supports atomic counters (incrementing values).

Key Concept: You use an UpdateExpression string.
