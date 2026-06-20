from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ContextualPrecisionMetric, ContextualRecallMetric, ContextualRelevancyMetric
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv
from deepeval.models import GPTModel
from deepeval.models import OllamaModel

import os

load_dotenv()

local_model = OllamaModel(model = "qwen2.5-coder:7b", base_url = "http://localhost:11434")

# custom_model = GPTModel(model = "gpt-4o-mini")


test_case = LLMTestCase(
    input = "What is the refund policy",
    actual_output = "We have lot of products in our store",
    # actual_output = "You can return the product within 25 days for a full_refund",
    expected_output = "Items can be returned within 30 days",
    # retrieval_context = ["Our return policy allows refunds within 30 days of purchase"]
    # retrieval_context = ["Our return policy allows refunds within 30 days of purchase","Tomorrow is a Holiday"]
    retrieval_context = ["Tomorrow is a Holiday","Our return policy allows refunds within 30 days of purchase. We have summer sales going on where lot of new poducts have arrived"]
)

metrics = [AnswerRelevancyMetric(model = local_model,async_mode=False), FaithfulnessMetric(model=local_model, async_mode=False),
           ContextualPrecisionMetric(model = local_model, include_reason= True),
           ContextualRecallMetric(model= local_model),
           ContextualRelevancyMetric(model= local_model)]

evaluate(test_cases = [test_case], metrics= metrics)
