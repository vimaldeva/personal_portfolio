## Adjusted R-squared

#### Definition 
Adjusted R-squared provides the exact same core information as regular R-squared (how well your model explains the data), but with one massive improvement: it penalizes you for adding useless information.


With standard R-squared, every time you add a new variable (feature) to your machine learning model, the score will either stay the same or go up. It mathematically cannot go down. Because of this, a model with 100 useless variables might look better on paper than a model with 3 highly predictive variables.


Adjusted R-squared fixes this by adding a mathematical penalty for every new variable you introduce. If a new variable doesn't improve the model's accuracy enough to offset the penalty, your Adjusted R-squared score will actually drop.

---

#### Mathematical formula 
```
Adjusted R-squared = 1 - [ ( (1 - Regular R-squared) * (Total Rows - 1) ) ÷ (Total Rows - Number of Variables - 1) ]
```

Steps to calculate:


Calculate your regular R-squared score.

Subtract that score from 1.

Multiply that by the number of data rows you have, minus 1.

Divide that result by (Total Rows minus Total Variables minus 1).

Subtract that final number from 1.

---

#### Pros
Prevents "Overfitting": It stops you from thinking your model is improving just because you threw a massive amount of random data at it.

Identifies the Best Model: It helps you find the simplest, most efficient model by rewarding you for using fewer, high-quality variables.
---
#### Cons
Harder to Interpret: Unlike regular R-squared, Adjusted R-squared is no longer a perfect "percentage of variance explained." It is just a comparative score.

Can Be Negative: If your model is terrible and has way too many useless variables, the harsh mathematical penalty can push the score below zero.

Requires Extra Math in Python: Unlike most metrics, Scikit-Learn does not have a built-in function specifically for Adjusted R-squared, so you have to calculate it manually using the regular R-squared output.

---

#### When to Use It
When you are comparing two models that predict the exact same thing, but one model uses more variables than the other.

During "feature selection" (the process of deciding which columns of data to keep and which to delete before training your model).

---
#### When Not to Use It
When you only have one single variable predicting your target (Simple Linear Regression). Regular R-squared is perfectly fine here.

When you need to report the actual dollar, minute, or temperature error to stakeholders (use MAE or RMSE).

---
#### A Real-World Scenario Where Adjusted R-squared is the Best Choice
Scenario: Predicting House Prices using Good vs. Garbage Data


Imagine you are building an AI to predict house prices, and you test two different models.


Model A uses just 3 variables: Square Footage, Number of Bedrooms, and Zip Code.

Model B uses 50 variables: The same 3 good ones, plus 47 totally useless ones (like the color of the neighbor's car, the number of clouds in the sky that day, the phase of the moon, etc.).

If you check the regular R-squared:


Model A scores: 0.85

Model B scores: 0.86

Looking only at regular R-squared, your boss might tell you to put Model B into production because the score is technically higher. But Model B is a bloated, terrible model full of random noise!


By using Adjusted R-squared, the mathematical penalty for adding useless variables kicks in:


Model A scores: 0.84 (barely punished, because it only used 3 variables).

Model B scores: 0.65 (heavily punished for having 47 useless variables that didn't genuinely help the model).

Now the truth is revealed. Adjusted R-squared proves that Model A is vastly superior and more efficient, saving you from deploying a garbage model into the real world.

---

#### Python Code Example (using Scikit-Learn)
Because Scikit-Learn doesn't have a direct adjusted_r2_score function, we first calculate the regular r2_score, and then apply the plain English formula shown above.



```
from sklearn.metrics import r2_score

# 1. Actual values and Model Guesses
actual_prices = [300, 350, 400, 450, 500]
model_guesses = [310, 340, 390, 460, 490]

# 2. Define the shape of your data
total_rows = len(actual_prices)  # We have 5 rows of data (5 houses)
number_of_variables = 3          # Let's say our model used 3 variables (sqft, beds, zip)

# 3. Get the regular R-squared first
regular_r2 = r2_score(actual_prices, model_guesses)

# 4. Calculate Adjusted R-squared using the formula
# Adjusted R2 = 1 - [ ( (1 - R2) * (Rows - 1) ) / (Rows - Variables - 1) ]
numerator = (1 - regular_r2) * (total_rows - 1)
denominator = (total_rows - number_of_variables - 1)

adjusted_r2 = 1 - (numerator / denominator)

# 5. Print the results to compare them
print(f"Regular R-squared:  {regular_r2:.4f}")
print(f"Adjusted R-squared: {adjusted_r2:.4f}")
```