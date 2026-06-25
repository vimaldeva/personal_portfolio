import os
from deepeval import evaluate
from deepeval.test_case import ConversationalTestCase, Turn, ToolCall
from deepeval.metrics import TopicAdherenceMetric, ToolUseMetric

# 1. Set your LLM Judge API Key
os.environ["OPENAI_API_KEY"] = "your_openai_key"

# 2. Define the broad list of tools available to your agent
# (This allows the metric to determine if the agent picked the optimal tool)
global_available_tools = [
    ToolCall(name="check_shipping_status", description="Fetches delivery updates using a tracking ID."),
    ToolCall(name="cancel_order", description="Cancels an order and initiates a refund process."),
    ToolCall(name="check_warehouse_inventory", description="Checks item stock counts in real-time.")
]

# 3. Build a multi-turn conversation test case
convo_test_case = ConversationalTestCase(
    scenario="Customer trying to locate a delayed package",
    turns=[
        Turn(
            role="user", 
            content="Hi, my order #10293 hasn't arrived yet. Can you tell me where it is?"
        ),
        Turn(
            role="assistant", 
            content="Let me look that up for you right away.",
            # The assistant correctly invokes the shipping tracker tool here
            tools_called=[
                ToolCall(
                    name="check_shipping_status", 
                    description="Fetches delivery updates using a tracking ID.",
                    input_parameters={"order_id": 10293},
                    output={"status": "Delayed in transit", "eta": "June 25th"}
                )
            ]
        ),
        Turn(
            role="user", 
            content="Okay thanks. Also, do you know if the blue shoes are still in stock?"
        ),
        Turn(
            role="assistant", 
            content="Yes, we have 5 pairs left in our main warehouse.",
            # The assistant uses the inventory tool for the second query
            tools_called=[
                ToolCall(
                    name="check_warehouse_inventory",
                    description="Checks item stock counts in real-time.",
                    input_parameters={"item": "blue shoes"},
                    output={"stock_count": 5}
                )
            ]
        ),
        Turn(
            role="user", 
            content="Great! By the way, who do you think will win the football match tonight?"
        ),
        Turn(
            role="assistant", 
            content="I can only assist you with store orders, shipping, and inventory queries. Let me know if you need anything else!"
        )
    ]
)

# 4. Initialize DeepEval Metrics
# TopicAdherenceMetric penalizes the bot if it answers questions outside allowed boundaries
topic_metric = TopicAdherenceMetric(
    relevant_topics=["order tracking", "shipping status", "product stock updates"],
    threshold=0.5
)

# ToolUseMetric evaluates both tool selection accuracy and parameter correctness
tool_metric = ToolUseMetric(
    available_tools=global_available_tools,
    threshold=0.5
)

# 5. Run the evaluation
if __name__ == "__main__":
    evaluate(
        test_cases=[convo_test_case], 
        metrics=[topic_metric, tool_metric]
    )
