## Cross-Region Snapshot Copy
### What is it?
- Automatically copies snapshots to another AWS region
- Used for disaster recovery — if primary region goes down, restore from another region

```
Primary Cluster (us-east-1)
        ↓ auto snapshot
S3 (us-east-1)
        ↓ cross-region copy
S3 (eu-west-1)  ← restore here if us-east-1 fails
```

### Setup
```
-- Enable cross-region snapshot copy
aws redshift enable-snapshot-copy \
  --cluster-identifier my-cluster \
  --destination-region eu-west-1 \
  --retention-period 7;
```

### Key Things to Remember
- Works for both automated and manual snapshots
- Additional S3 storage cost in destination region
- If cluster uses KMS encryption → must set up snapshot copy grant in destination region first
- Retention period in destination can differ from source
- Snapshot copy is async — slight lag between source and destination


