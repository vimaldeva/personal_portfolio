## 1. Data Preparation & Engineering
Before you can train, you must prepare and store your data.

**SageMaker Ground Truth** : A managed data labeling service (using human workers or AI) to create high-quality training datasets.

**SageMaker Data Wrangler**: A low-code interface to import, transform, and analyze data from over 40 sources without writing code.

**SageMaker Feature Store**: A centralized repository to store, update, and retrieve features for both training (offline) and real-time inference (online). This is critical for feature consistency in MLOps.

**SageMaker Processing**: Managed Python/Spark jobs used for data preprocessing, post-processing, and model evaluation.


---
## 2. Model Development & Experimentation
Where data scientists build and test their hypotheses.

**SageMaker Studio**: A unified web-based IDE for the entire ML workflow.

**SageMaker Notebooks**: Managed Jupyter notebooks with elastic compute.

**SageMaker JumpStart**: A hub for pre-trained models (including Foundation Models/LLMs) and one-click solutions for common ML use cases.

**SageMaker Canvas**: A no-code interface for business analysts to build models without writing a single line of code.

**SageMaker Experiments**: Automatically tracks and compares different training iterations (trials), parameters, and results.


---
## 3. Model Training & Optimization
Scaling the compute needed to create the model.

**SageMaker Training Jobs**: Fully managed infrastructure that spins up, trains, and shuts down clusters automatically.

**SageMaker Automatic Model Tuning (HPO)**: Uses Bayesian optimization to find the best hyperparameters for your model.

**SageMaker Distributed Training Libraries**: Optimized libraries to split large datasets or large models across multiple GPUs/nodes (Data Parallelism and Model Parallelism).

**SageMaker Autopilot**: An AutoML tool that automatically explores different algorithms and preprocessing steps to find the best model for your data.


---
## 4. Model Deployment (Inference)
Getting the model into production.

- Real-time Endpoints: For low-latency, persistent inference.

- Serverless Inference: For intermittent traffic; you only pay for the compute time used (no idle costs).
- Asynchronous Inference: For large payloads (up to 1GB) or long processing times (up to 1 hour).
- Batch Transform: For offline predictions on large datasets.
- Inference Recommender: Automatically runs load tests to help you choose the best instance type and configuration for your model.
- Multi-Model Endpoints (MME): Allows hosting multiple models on a single endpoint to save costs.

---
## 5. MLOps & Governance (The "Ops" Part)
The glue that automates, monitors, and secures the lifecycle.

**SageMaker Pipelines**: A CI/CD service specifically for ML. It allows you to create automated workflows (DAGs) for data prep, training, and deployment.

**SageMaker Model Registry**: A central catalog to version models, manage their lifecycle (e.g., "Pending Manual Approval" to "Production"), and track lineage.

**SageMaker Model Monitor**: Automatically detects Data Drift (changes in input data) and Concept Drift (changes in model accuracy) in production.

**SageMaker Clarify**: Detects bias in datasets and provides "Explainability" (SHAP values) to understand why a model made a specific prediction.

**SageMaker Model Cards**: Standardized documentation for models (purpose, risk, performance) to satisfy compliance and governance.

**SageMaker Model Dashboard**: A unified view to monitor the health and performance of all your deployed models across the account.

**SageMaker Lineage Tracking**: Automatically tracks the history of data, code, and models to ensure reproducibility and auditability.

---
## 6. Specialized & Edge Features
**SageMaker Edge Manager**: For managing and monitoring models deployed on IoT devices (edge).
**SageMaker Neo**: A compiler that optimizes models to run faster on specific hardware (ARM, Intel, Nvidia, etc.) with a smaller footprint.

---

Summary: The "Must-Haves" for MLOps
If you are specifically setting up an MLOps pipeline, focus on these five:


- Pipelines (Orchestration)
- Model Registry (Versioning)
- Feature Store (Data Consistency)
- Model Monitor (Production Health)
- Experiments (Tracking)