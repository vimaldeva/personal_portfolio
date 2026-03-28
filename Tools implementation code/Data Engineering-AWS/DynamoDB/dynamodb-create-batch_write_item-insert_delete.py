client.batch_write_item(
    RequestItems={
        'ExamMarks': [
            # Request 1: Put Item
            {
                'PutRequest': {
                    'Item': {
                        'roll_no': {'N': '201'},
                        'subject_cd': {'S': 'ENG-101'},
                        'marks': {'N': '88'}
                    }
                }
            },
            # Request 2: Put Another Item
            {
                'PutRequest': {
                    'Item': {
                        'roll_no': {'N': '202'},
                        'subject_cd': {'S': 'ENG-101'},
                        'marks': {'N': '91'}
                    }
                }
            },
            # Request 3: Delete an Item (in the same batch!)
            {
                'DeleteRequest': {
                    'Key': {
                        'roll_no': {'N': '105'},
                        'subject_cd': {'S': 'HIST-101'}
                    }
                }
            }
        ]
    }
)


batch_write_item (Bulk Insert/Delete) :

Extremely Important for Performance. If you need to upload 100 items, calling put_item 100 times is slow because of network latency. batch_write_item allows you to send up to 25 items in a single network request.

