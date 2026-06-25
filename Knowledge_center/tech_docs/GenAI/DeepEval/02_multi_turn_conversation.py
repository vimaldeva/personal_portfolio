from deepeval import evaluate , assert_test
from deepeval.test_case import ConversationalTestCase, Turn
from deepeval.metrics import TurnRelevancyMetric, KnowledgeRetentionMetric, RoleAdherenceMetric, ConversationCompletenessMetric
from deepeval.models import OllamaModel

local_model = OllamaModel(model = "qwen2.5-coder:7b", base_url = "http://localhost:11434")
# local_model = OllamaModel(model = "gpt-oss:20b", base_url = "http://localhost:11434")

conversations_dataset = [
    ConversationalTestCase(
        scenario="Financial Q&A",  
        chatbot_role = "Bank customer support Assistant",
        turns=[
            Turn(role="user", content="Hi, how can I check my account balance?"),
            Turn(role="assistant", content="You can log into our online banking platform or call customer service."),
            Turn(role="user", content="Thank you for the details.What are the fees associated with transferring money overseas?"),
            Turn(role="assistant", content="The fee depends on the amount and the destination. Please check our website for details."),
            Turn(role="user", content="Thank you for the details.How do I report fraudulent activity on my card with card number 1234?"),
            Turn(role="assistant", content="Contact customer service immediately and provide them with all details of the fraud."),
            Turn(role="user", content="Thank you for the details.What is your return policy for online purchases?"),
            Turn(role="assistant", content="We offer a 30-day return policy. Please visit our website for detailed terms and conditions."),
            # Turn(role="user", content="Give me the list of questions that I asked yo before "),
            # Turn(role="assistant", content="I dont have the conversation history with me, but I can help you with any new questions you have."),
            Turn(role="user", content="what is my credit card balance?"),
            Turn(role="assistant", content="Can you please provide me your credit card number"),
            Turn(role="user", content="tell me a joke about football "),
            Turn(role="assistant", content="Why do football players always have a snack before the game? To make sure they have the energy to avoid interceptions!"),

        ]
    ),
    ConversationalTestCase(
    chatbot_role = "Bank customer support Assistant",
    turns=[
        Turn(role="user", content="What if these shoes don't fit?"),
        Turn(role="assistant", content="We offer a 30-day full refund at no extra cost.", retrieval_context=["All customers are eligible for a 30 day full refund at no extra cost."])
    ],
    expected_outcome="The chatbot must explain the store policies like refunds, discounts, ..etc.",
)
    # ... (Conversations 2-10 defined similarly in the full script)
]

turn_relevancy = TurnRelevancyMetric(threshold=0.8, model= local_model)
knowledge_retention = KnowledgeRetentionMetric(threshold=0.8, model= local_model)
role_adherence = RoleAdherenceMetric(threshold=0.8, model= local_model)
conversation_completeness = ConversationCompletenessMetric(threshold=0.5,model= local_model)

evaluate(
        test_cases=conversations_dataset,
        metrics=[turn_relevancy, knowledge_retention, role_adherence, conversation_completeness]
    )

