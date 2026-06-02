import boto3
import json
import time
import random

# --- CONFIGURATION ---
STREAM_NAME = 'vimal-kinesis-stream'

REGION = "us-east-1" # Make sure this matches your AWS console

# --- INITIALIZE KINESIS CLIENT ---
client = boto3.client(
    'kinesis',
    region_name=REGION
)

def send_data():
    print(f"Starting to send data to {STREAM_NAME}...")
    
    try:
        # Send 20 test messages
        for i in range(1, 21):
            # 1. Create a data payload (JSON)
            payload = {
                "id": i,
                "user_id": random.randint(100, 999),
                "action": random.choice(["click", "login", "purchase", "logout"]),
                "device": random.choice(["mobile", "desktop", "tablet"]),
                "local_timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 2. Convert to JSON string and then to bytes
            data_bytes = json.dumps(payload).encode('utf-8')
            
            # 3. Put the record into the stream
            # PartitionKey is used to distribute data across shards
            response = client.put_record(
                StreamName=STREAM_NAME,
                Data=data_bytes,
                PartitionKey=str(payload["user_id"]) 
            )
            
            print(f"Sent Message #{i}: {payload}")
            print(f"--> SequenceNumber: {response['SequenceNumber']}\n")
            
            # Wait 1 second between messages so you can watch them arrive
            time.sleep(1)

    except Exception as e:
        print(f"Error sending data: {e}")

if __name__ == "__main__":
    send_data()