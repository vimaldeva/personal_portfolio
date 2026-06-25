import sys
import mlflow
from openai import OpenAI
import ollama # Kept ONLY for the get_available_models list function

# 1. Point MLflow to your tracking server dashboard
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Ollama_Chat_Experiment")

# 2. Enable automatic logging for all OpenAI SDK calls
mlflow.openai.autolog()

# 3. Point the OpenAI client to your local Ollama server instance
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama" # Ollama does not validate keys, but a string value is required
)

def chat_with_ollama():
    print("Ollama Chat CLI - Type 'quit' to exit")
    print("Available models:", get_available_models())
    print("-" * 50)
    
    model = input("Enter model name (default: qwen2.5-coder:7b): ").strip()
    if not model:
        model = "qwen2.5-coder:7b"
    
    messages = []
    
    # CRITICAL: Start an active MLflow parent run session to nest the conversation loop turns together
    with mlflow.start_run(run_name=f"Chat_Session_{model}"):
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
                
            if not user_input:
                continue
                
            messages.append({"role": "user", "content": user_input})
            
            try:
                # Call Ollama via the OpenAI client so MLflow autolog triggers natively
                response = client.chat.completions.create(
                    model=model,
                    messages=messages
                )
                
                assistant_response = response.choices[0].message.content
                print(f"Assistant: {assistant_response}")
                
                messages.append({"role": "assistant", "content": assistant_response})
                
            except Exception as e:
                print(f"Error: {e}")
                print("Please check if Ollama is running and the model exists.")

def get_available_models():
    try:
        response = ollama.list()
        return ", ".join([m['name'] for m in response['models']])
    except:
        return "No models found"

if __name__ == "__main__":
    chat_with_ollama()
