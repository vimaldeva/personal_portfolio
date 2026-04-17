## R-squared (R²), also known as the Coefficient of Determination.

#### Definition

It tells you how much of the data's pattern your model actually captured. It answers the question: "How much better is our fancy machine learning model compared to a totally stupid model that just guesses the exact same average number every single time?"


A score of 1.0 (100%) means your model perfectly predicts every single data point.

A score of 0.0 (0%) means your model is completely useless and is no better than just guessing the average.

(In rare cases, your score can be negative if your model is so incredibly bad that it's actually worse than just guessing the average!)

---

#### Mathematical Formula

```
R-squared = 1 - ( Your Model's Mistakes ÷ Mistakes if you just guessed the Average )

```
Steps to calculate:


Calculate your model's squared errors (just like calculating MSE).

Find the average of all the actual values. Calculate the squared errors as if your model literally just guessed that average number every single time.

Divide your model's error by the "average guess" error. (This gives you the percentage of error that still exists).

Subtract that number from 1 to get the percentage of error you successfully eliminated.

---

#### Python code 

```
from sklearn.metrics import r2_score

# 2. Create actual values and the model's guesses
actual_sales = [100, 150, 200, 250]
model_guesses = [110, 140, 190, 260]

# 3. Calculate the R-squared score
r2_result = r2_score(actual_sales, model_guesses)

# 4. Print the result
# Multiplying by 100 to show it as a percentage
print(f"The R-squared score is: {r2_result:.4f} (or {r2_result * 100:.2f}%)")
```
---
#### Pros
- Universal "Score": Because it is a ratio between 0 and 1 (or 0% to 100%), it is completely scale-free. You can use it to easily communicate success to business leaders ("Our model captures 85% of the trend").

- Easy to Compare Across Datasets: You can use R-squared to compare how well models are performing on totally different datasets (e.g., comparing a model predicting $500,000 houses with a model predicting $2 cups of coffee).

---
#### Cons
- Doesn't give real-world context: A model might have a great R-squared of 0.95 (95%), but if you are predicting something highly sensitive, that remaining 5% of error could still represent millions of dollars lost. It hides the actual dollar/minute amount of the error.

- Can be manipulated: Every time you add a new piece of information (a new variable) to a machine learning model, the standard R-squared mathematical formula will always stay the same or go up. It will never go down, even if the new information is complete garbage. (This is why "Adjusted R-squared" was invented).
---

#### When to Use It
When you need a quick, universal baseline to see if your model is actually doing anything useful (if your R² is 0.05, your model has failed to learn anything).

When you need to compare model performance across different departments or datasets with vastly different numbers.

---

#### When Not to Use It
When you need to know exactly how much money or time your model is losing per mistake (use MAE or RMSE).

When you are adding dozens of new features to your model to see if they help (use Adjusted R-squared instead, which penalizes you for adding useless data).

---
#### A Real-World Scenario Where R-squared is the Best Choice
Scenario: A Manager Comparing Two Different AI Teams


Imagine you are the VP of Data Science at a retail company, overseeing two teams.


Team A built a model predicting the company's annual revenue in billions of dollars.

Team B built a model predicting the daily sales of a specific candy bar in single dollars.

You ask both teams how well their models are doing.


Team A says: "Our Root Mean Squared Error is $50,000,000."

Team B says: "Our Root Mean Squared Error is $15."

If you only look at RMSE, you cannot compare these teams. Team A's error sounds terrifying ($50 million!), and Team B's error sounds great ($15). But relative to what they are predicting, $50 million might be a remarkably accurate prediction for a multi-billion dollar company, while being off by $15 for a candy bar might mean the model is terrible!


By using R-squared, the playing field is leveled.


Team A reports an R-squared of 0.96. (They are capturing 96% of the revenue variance).

Team B reports an R-squared of 0.40. (They are only capturing 40% of the candy bar variance).

Now you instantly know: Team A's model is doing a fantastic job, and Team B needs to go back to the drawing board to improve their model.