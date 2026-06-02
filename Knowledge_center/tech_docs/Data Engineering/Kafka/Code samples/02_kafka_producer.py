import json
import time
from confluent_kafka import Producer

# --- CONFIGURATION ---
conf = {
    # Get this from Aiven Overview (The URI)
    'bootstrap.servers': 'kafka-vimal-vimaldeva10-ebe6.k.aivencloud.com:26267',
    
    # Security Settings (Points to the files in the same folder)
    'security.protocol': 'SSL',
    'ssl.ca.location': 'ca.pem',
    'ssl.certificate.location': 'service.cert',
    'ssl.key.location': 'service.key',
    
    # Reliability settings
    'acks': 'all'
}

# --- CALLBACK FUNCTION ---
# This runs when the message is successfully sent (or fails)
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# --- INITIALIZE PRODUCER ---
producer = Producer(conf)
topic_name = "test-topic"

print(f"Starting producer. Sending messages to {topic_name}...")

try:
    # Send 10 test messages
    for i in range(1, 11):
        # Create a dictionary (JSON)
        data = {
            "id": i,
            "source": "local_python_script",
            "message": f"Hello from my computer! Message #{i}",
            "timestamp": time.time()
        }
        
        # Convert dict to string (JSON)
        payload = json.dumps(data)
        
        # Post the data
        producer.produce(
            topic=topic_name, 
            value=payload.encode('utf-8'), 
            callback=delivery_report
        )
        
        # Serve delivery callbacks (important!)
        producer.poll(0)
        
        print(f"Sent: {payload}")
        time.sleep(2) # Wait 2 seconds between messages

except KeyboardInterrupt:
    print("Stopping producer...")

finally:
    # Wait for all messages to be delivered before closing
    print("Flushing final messages...")
    producer.flush()