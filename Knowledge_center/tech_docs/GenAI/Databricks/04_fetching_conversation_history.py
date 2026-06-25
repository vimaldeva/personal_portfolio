traces_df = mlflow.search_traces(
    filter_string="tag.session_id = 'session-abc-123'"
)

display(traces_df)


#####################

import mlflow
from mlflow import MlflowClient

EXPERIMENT_NAME = "/Workspace/Users/vimaldeva10@gmail.com/strands-tax-agent"
session_id = "session-abc-123"

client = MlflowClient()

# 1. Get experiment by name and extract its ID
exp = client.get_experiment_by_name(EXPERIMENT_NAME)
if exp is None:
    raise RuntimeError(f"Experiment not found: {EXPERIMENT_NAME}")

experiment_id = exp.experiment_id

# 2. CORRECTED SEARCH: Use experiment_ids and match the tag schema from your working code
traces = client.search_traces(
    experiment_ids=[experiment_id],
    filter_string=f"tag.session_id = '{session_id}'"
)

print("Number of turns:", len(traces))

for i, trace in enumerate(traces, 1):
    print(f"\nTurn {i}:")
    
    # 3. FIX DATA EXTRACTION: Extract attributes directly from the TraceInfo object wrapper
    print("Trace ID:", trace.info.trace_id)
    print("Status:", trace.info.status)

    # 4. FIX SPANS PARSING: Access spans array correctly using standard entity dictionary mapping
    spans = trace.data.spans if hasattr(trace, "data") and hasattr(trace.data, "spans") else []
    
    for span in spans:
        # Spans objects inside the MlflowClient results are typically Span Entity instances
        # We handle both object properties and generic dictionary fallbacks safely
        name = getattr(span, "name", span.get("name") if isinstance(span, dict) else "Unknown")
        inputs = getattr(span, "inputs", span.get("inputs") if isinstance(span, dict) else "None")
        outputs = getattr(span, "outputs", span.get("outputs") if isinstance(span, dict) else "None")
        
        print(f"  Span name: {name}")
        print(f"  Inputs: {inputs}")
        print(f"  Outputs: {outputs}")

############################################################


import mlflow
from mlflow import MlflowClient

EXPERIMENT_NAME = "/Workspace/Users/vimaldeva10@gmail.com/strands-tax-agent"
session_id = "session-abc-123"

client = MlflowClient()

# 1. Fetch the experiment metadata
exp = client.get_experiment_by_name(EXPERIMENT_NAME)
if exp is None:
    raise RuntimeError(f"Experiment not found: {EXPERIMENT_NAME}")

# 2. Retrieve all traces for this specific session
traces = client.search_traces(
    experiment_ids=[exp.experiment_id],
    filter_string=f"tag.session_id = '{session_id}'"
)

conversation_turns = []

# 3. Process and extract root inputs/outputs from each trace
for trace in traces:
    # Get all spans inside this trace turn
    spans = trace.data.spans if hasattr(trace, "data") and hasattr(trace.data, "spans") else []
    
    # Locate the root span (the one representing the top-level Agent execution)
    # The root span has no parent (parent_id is None)
    root_span = next((s for s in spans if getattr(s, "parent_id", None) is None), None)
    
    if root_span:
        # Pull the accurate start timestamp to guarantee chronological order
        start_time = getattr(trace.info, "timestamp_ms", getattr(root_span, "start_time_ms", 0))
        
        # Pull inputs/outputs safely, falling back gracefully if empty
        user_input = getattr(root_span, "inputs", "No input recorded")
        agent_response = getattr(root_span, "outputs", "No response recorded")
        
        conversation_turns.append({
            "timestamp": start_time,
            "user": user_input,
            "agent": agent_response
        })

# 4. CRITICAL: Sort chronologically by timestamp (oldest first)
conversation_turns.sort(key=lambda x: x["timestamp"])

# 5. Display the conversation history beautifully
print(f"=== Conversation History for Session: {session_id} ===\n")
for index, turn in enumerate(conversation_turns, 1):
    print(f"--- Turn {index} ---")
    print(f"👤 User: {turn['user']}")
    print(f"🤖 Agent: {turn['agent']}\n")
