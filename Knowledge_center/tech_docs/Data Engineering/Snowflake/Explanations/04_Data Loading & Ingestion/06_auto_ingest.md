## Auto-Ingest with SQS (S3 Events)

### What is it?
Snowpipe watches an SQS queue that S3 publishes events to
When new file lands in S3 → S3 sends event to SQS → Snowpipe picks it up → loads file
Setup Flow

```
Step 1: Create Snowpipe with AUTO_INGEST = TRUE
        ↓
Step 2: Get SQS ARN from Snowpipe
        DESC PIPE orders_pipe;
        → shows notification_channel (SQS ARN)
        ↓
Step 3: Go to S3 bucket → Properties → Event Notifications
        → Create notification for "All object create events"
        → Destination: SQS → paste the ARN from Step 2
        ↓
Step 4: Files land in S3 → S3 notifies SQS → Snowpipe loads automatically
```

```
Step 1: Create Snowpipe with AUTO_INGEST = TRUE
        ↓
Step 2: Get SQS ARN from Snowpipe
        DESC PIPE orders_pipe;
        → shows notification_channel (SQS ARN)
        ↓
Step 3: Go to S3 bucket → Properties → Event Notifications
        → Create notification for "All object create events"
        → Destination: SQS → paste the ARN from Step 2
        ↓
Step 4: Files land in S3 → S3 notifies SQS → Snowpipe loads automatically
```

### End-to-End Flow

```
New file → S3 bucket
               ↓ S3 event notification
           SQS Queue (Snowflake-managed)
               ↓ Snowpipe polling SQS
           Snowpipe detects new file
               ↓ auto-triggers COPY
           Data loaded into table
           (within 1-2 minutes of file arrival)
```

### Key Things to Remember
One pipe = one S3 prefix + one target table
SQS queue is Snowflake-managed — you just point S3 at it
Azure equivalent: Azure Event Grid instead of SQS
GCS equivalent: GCS Pub/Sub notifications
Snowpipe does NOT guarantee ordering — files loaded as they arrive


