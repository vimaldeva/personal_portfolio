client.delete_item(
    TableName='ExamMarks',
    Key={
        'roll_no': {'N': '101'},
        'subject_cd': {'S': 'MATH-101'}
    }
)
