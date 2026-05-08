## Cloud Platform Support (AWS, Azure, GCP)

### What is it?
- Snowflake runs on top of major cloud providers — not its own infrastructure
- You choose a cloud + region when creating your Snowflake account
- Snowflake uses that cloud's object storage and networking underneath

### How Snowflake Uses Each Cloud

| Layer | AWS | Azure | GCP |
| :-- | :-- | :-- | :-- |
| Storage | S3 | Azure Blob Storage | Google Cloud Storage |
| Compute | EC2 (virtual machines) | Azure VMs | GCP VMs |
| Network | AWS VPC | Azure VNet | GCP VPC |
| Private Connectivity | AWS PrivateLink | Azure Private Link | GCP Private Service Connect |

### Cross-Cloud Capabilities

```
Company A (Snowflake on AWS us-east-1)
        │
        │ Cross-cloud replication / Data Sharing
        │
Company B (Snowflake on Azure eastus)
```

- Data Sharing across clouds — share live data between Snowflake accounts on different clouds
- Cross-cloud replication — replicate databases across AWS ↔ Azure ↔ GCP
- Cross-region within same cloud also supported

### Choosing Cloud + Region — Key Considerations

| Factor | Consideration |
| :-- | :-- |
| Where your data lives | Pick same cloud to avoid egress costs |
| Where your team works | Pick closest region for low latency |
| Compliance | Some regions have specific certifications |
| Cross-cloud sharing | Possible but adds network cost |

### Key Things to Remember
- Snowflake account is tied to one cloud + region at creation — cannot change later
- Data transfer within same cloud/region = no egress cost
- Data transfer across regions or clouds = egress cost applies
- Snowflake's behavior is identical across all clouds — no feature differences for most features
- Business Critical edition needed for AWS GovCloud or Azure Government regions





