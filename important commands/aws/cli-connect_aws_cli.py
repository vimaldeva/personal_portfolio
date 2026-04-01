# Connect if local CLI is connected to AWS or not
aws sts get-caller-identity

# Check AWS connectivity
aws s3 ls

# create new AWS connection using access keys
aws configure

# Configure using SSO access keys
$env:AWS_REGION = "us-east-1"
$env:AWS_DEFAULT_REGION = "us-east-1"
$env:AWS_ACCESS_KEY_ID="AAAAAA"
$env:AWS_SECRET_ACCESS_KEY="/AAA/AAAA"
$env:AWS_SESSION_TOKEN= "IAAAAA"

