## MAE - Mean Absolute Error

#### Definition

- MAE measures the average magnitude of the errors in a set of predictions, without considering their direction. 
- It tells you, on average, how far off your predictions are from the actual values. 
- Because it uses absolute values, positive and negative errors don't cancel each other out. 
- The result is expressed in the exact same units as the target variable (e.g., if you are predicting housing prices in dollars, the MAE will be in dollars).

---

#### Mathenatical Formula

```
MAE = ( ∑ | Actual – Guess | ) ÷ Total Guesses

```

Actual: The real-world number you were trying to predict.

Guess: The number your machine learning model predicted.

| | (Absolute Value): This means "ignore negative signs." Just look at the distance between the numbers. (For example, if you guess 5 and the actual is 3, the difference is 2. If you guess 3 and the actual is 5, the difference is still just 2).

∑ (Sigma / Sum): This simply means "Add them all up."

÷ Total Guesses: Divide by the number of times you guessed, which gives you the average.

---


#### Python code

```
from sklearn.metrics import mean_absolute_error

actual_prices = [250, 300, 350, 400, 15000]  # Notice the massive 15,000 outlier!
model_guesses = [245, 310, 350, 380, 10000]  # The model missed the outlier by a lot

#  Calculate the MAE
mae_result = mean_absolute_error(actual_prices, model_guesses)

#  Print the result
print(f"The Mean Absolute Error is: {mae_result}")
```
---

#### Pros

- Highly Intuitive: Because it scales linearly and shares the target's units, it is very easy to explain to non-technical stakeholders (e.g., "Our model's predictions are off by an average of $5,000").

- Robust to Outliers: Unlike Mean Squared Error (MSE), MAE does not square the error terms. This means a single massive outlier won't exponentially blow up your error metric.

- Even Penalty: All errors are weighted equally on a linear scale. An error of 10 is penalized exactly twice as much as an error of 5.

---
#### Cons

- Ignores Error Significance: Because all errors are weighted equally, it doesn't penalize large, potentially catastrophic errors any more than small ones.

- Mathematical Optimization Challenges: The absolute value function $|x|$ is not strictly differentiable at zero. While modern algorithms easily handle this using sub-gradients, it makes analytical optimization slightly more complex than the perfectly smooth, bowl-shaped MSE.

- Scale-Dependent: Because it is expressed in the target's units, you cannot use MAE to compare model performance across different datasets that have different scales.

--- 
#### When to use it 

- Outlier-heavy data: Use MAE when your dataset contains anomalies or outliers that you know exist but shouldn't overly influence your model's evaluation.

- Business reporting: Use it when you need to explain the model's performance to business users who need a straightforward, real-world interpretation of the error.

- When all errors are equal: Use it when a misprediction of $100 is considered exactly twice as bad as a misprediction of $50, no more and no less.

---

#### When to Not use it 

- When large errors are unacceptable: If an error of 100 is much more than twice as bad as an error of 50 (e.g., predicting stock market crashes or medical dosages), you should avoid MAE. Use MSE or RMSE instead, as they disproportionately penalize larger errors.

- When comparing across domains: Do not use MAE if you are trying to compare your model's accuracy across multiple targets with vastly different scales (use MAPE or R-squared instead).
---

#### A Real-World Scenario Where MAE is the Best Choice

Imagine you are building a machine learning model for a real estate website (like Zillow) to predict how much houses will sell for.


The Data: 99% of the houses in this city are normal family homes that cost between $200,000 and $500,000.

The Outliers: There are a handful of massive celebrity mega-mansions in the hills that cost $15,000,000.

Why MAE is better here than MSE or RMSE:
If you use MSE (Mean Squared Error), the formula squares the errors. If your model misprices a $15 million mansion by $2 million, squaring that error creates a mathematically massive penalty.


To minimize that huge penalty, the machine learning model will actually shift its focus to try and get the mega-mansions right. But by trying to fix the mansions, it ruins the predictions for the normal houses.


By using MAE, you don't square the errors. A 2 million dollar  error on a mansion is simply treated as a 2 million dollar error. The model won't panic and ruin the predictions for the 99% of normal houses just to accommodate a few crazy outliers. Furthermore, you can go to your boss and say, "On average, our algorithm predicts a house's price within $12,000 of its actual sale price," which is a perfect, easy-to-understand business metric.