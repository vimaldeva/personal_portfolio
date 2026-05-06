## Lambda UDFs (User Defined Functions)

## What is it?
- Custom functions written in Lambda that Redshift calls during query execution
- Extends Redshift SQL with logic that can't be done in standard SQL
- Lambda function processes input → returns result → - - Redshift uses it in query

Analogy:

SQL can't call an external API → Lambda UDF acts as a bridge
Redshift calls Lambda mid-query → Lambda does the work → returns result back


```
-- Create Lambda UDF pointing to a Lambda function
CREATE OR REPLACE EXTERNAL FUNCTION get_sentiment(input_text VARCHAR)
RETURNS VARCHAR
VOLATILE
LAMBDA 'my-sentiment-lambda'
IAM_ROLE 'arn:aws:iam::123:role/RedshiftRole';

-- Use it in a query like a normal function
SELECT review_text, get_sentiment(review_text) as sentiment
FROM product_reviews;
```

Lambda function (Python):

```
def handler(event, context):
    results = []
    for record in event['arguments']:
        text = record[0]
        # call Comprehend or any logic
        results.append("positive" if "good" in text else "negative")
    return {"results": results}

```

### Key Things to Remember
- Lambda UDF adds network latency — avoid on billions of rows
- Best for small lookups, API calls, complex transformations not possible in SQL
- Lambda must be in same region as Redshift cluster
- IAM Role needs lambda:InvokeFunction permission
- Scalar UDFs (Python/SQL) also exist for simpler cases — no Lambda needed

