response = client.batch_get_item(
    RequestItems={
        'ExamMarks': {
            'Keys': [
                {'roll_no': {'N': '101'}, 'subject_cd': {'S': 'MATH-101'}},
                {'roll_no': {'N': '102'}, 'subject_cd': {'S': 'PHY-102'}},
                {'roll_no': {'N': '103'}, 'subject_cd': {'S': 'CHEM-101'}}
            ]
        }
    }
)
print(response['Responses']['ExamMarks'])

batch_get_item (Bulk Read) :

Similar to batch write, but for reading. You can retrieve up to 100 items at once if you know their Primary Keys.
