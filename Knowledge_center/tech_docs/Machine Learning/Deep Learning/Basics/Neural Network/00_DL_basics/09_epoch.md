## What is an Epoch?
An Epoch represents one full pass of the entire training dataset through the neural network.

When you train a model, you don't just show it the data once. Because the weights are initialized randomly and the optimizer takes very small steps, the network needs to see the same data many times to gradually learn the underlying patterns.

1 Epoch = Every single sample in your training set has had an opportunity to update the model's internal parameters once.

---
### The Analogy: Studying for an Exam
Imagine you are a student preparing for a difficult final exam using a 500-page textbook.

The Dataset: The 500-page textbook.
- An Epoch: Reading the entire textbook from cover to cover exactly once.
- Training: You don't just read the book once and expect to be an expert. You read it, take notes, and realize you missed some things. So, you read it again. And again.
- Multiple Epochs: Each time you finish the book (one epoch), your understanding (the model's weights) gets a little better. You might study for 20 epochs (read the book 20 times) before you feel ready for the exam.

---
### Epochs vs. Batches vs. Iterations
These three terms are often confused. Here is how they relate to each other:

Let's say you have a dataset of 1,000 images and you set a Batch Size of 10.

- Batch Size: The number of samples processed at one time before the weights are updated. (In our case, 10).
- Iteration: One single update of the weights. To see all 1,000 images using batches of 10, the computer must perform 100 iterations ($1000 / 10 = 100$).
- Epoch: Once those 100 iterations are complete and the model has seen all 1,000 images, 1 Epoch has passed.
The Formula: 
Number of Iterations = Total Training Samples/Batch Size

---
### How Many Epochs Do You Need?
There is no "magic number" for epochs. It depends entirely on the complexity of your data and your model.

- Too Few Epochs (Underfitting): The model hasn't seen the data enough times to learn the patterns. It's like a student who only skimmed the first chapter of the textbook; they will perform poorly on the exam.
- Too Many Epochs (Overfitting): The model has seen the data so many times that it has started to memorize the specific noise and details of the training set, rather than learning the general patterns. It's like a student who memorized the exact wording of the practice questions but doesn't actually understand the concepts. They will get 100% on the practice test but fail the real exam.

---
### How Do We Stop? (Early Stopping)
Since we don't know the perfect number of epochs, data scientists use a technique called Early Stopping.

- We set a very high number of epochs (e.g., 1,000).
- We monitor the model's performance on a separate Validation Set (data the model isn't learning from).
- As long as the validation error is going down, we keep training.
- If the validation error stops improving or starts to go back up (a sign of overfitting), we stop the training automatically, even if we haven't reached 1,000 epochs.

---
### Summary
- Forward Pass: Data goes through the network.
- Backward Pass: Error goes back to calculate gradients.
- Iteration: One batch of data goes through the forward and backward pass.
- Epoch: All batches have gone through; the model has seen the whole dataset once.