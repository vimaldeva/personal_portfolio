client.transact_write_items(
    TransactItems=[
        {
            'Update': {
                'TableName': 'BankAccounts',
                'Key': {'AccountId': {'S': 'A'}},
                'UpdateExpression': 'SET balance = balance - :amount',
                'ExpressionAttributeValues': {':amount': {'N': '100'}}
            }
        },
        {
            'Update': {
                'TableName': 'BankAccounts',
                'Key': {'AccountId': {'S': 'B'}},
                'UpdateExpression': 'SET balance = balance + :amount',
                'ExpressionAttributeValues': {':amount': {'N': '100'}}
            }
        }
    ]
)

transact_write_items (ACID Transactions) :

Used when you need "All or Nothing" operations. For example, "Deduct money from User A AND Add money to User B". If one fails, both fail. This is more expensive than standard writes but ensures data integrity.

