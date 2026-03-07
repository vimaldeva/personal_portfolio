# Select all marks > 90 for a specific student
response = client.execute_statement(
    Statement="SELECT * FROM ExamMarks WHERE roll_no = 101 AND marks > 90"
)

print(response['Items'])

execute_statement (PartiQL - SQL for DynamoDB) :

If you prefer SQL syntax over the JSON format, DynamoDB supports PartiQL. This is very popular for developers coming from relational databases.

