## Linear Regression 

Linear regression is a supervised learning algorithm used to model the relationship between a dependent variable (target) and one or more independent variables (features). It assumes a linear relationship between the variables, meaning the dependent variable changes at a constant rate with respect to the independent variable(s). The goal is to find the best-fit line that minimizes the error between predicted and actual values.

---

#### Equation 

For simple linear regression (one independent variable), the equation is:

```
y = mx + b
```
y: Predicted value (dependent variable)

x: Input value (independent variable)

m: Slope of the line

b: Intercept (value of y when x = 0)

For multiple linear regression (multiple independent variables), the equation expands to:

```
y = β₀ + β₁x₁ + β₂x₂ + ... + βₖxₖ
```
β₀: Intercept

β₁, β₂, ..., βₖ: Coefficients for each independent variable.

---

#### Assumptions of Linear Regression

- Linearity: The relationship between inputs and output is linear.

- Independence of Errors: Errors are not correlated.

- Homoscedasticity: Errors have constant variance.

- Normality of Errors: Errors follow a normal distribution.

- No Multicollinearity: Independent variables are not highly correlated.

---

#### Code
```
import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([5, 15, 25, 35, 45, 55]).reshape((-1, 1))
y = np.array([5, 20, 14, 32, 22, 38])

model = LinearRegression().fit(X, y)

# View results 
print("Intercept:", model.intercept_)
print("Slope:", model.coef_)
print("R² Score:", model.score(X, y))

y_pred = model.predict(X)
print("Predictions:", y_pred)

```
---

### Evaluation Metrics

- Mean Squared Error (MSE): Average of squared differences between actual and predicted values.

- Root Mean Squared Error (RMSE): Square root of MSE.

- Mean Absolute Error (MAE): Average of absolute differences between actual and predicted values.

- R-squared (R²): Proportion of variance in the dependent variable explained by the independent variables.

---

#### Applications

- Predictive Modeling: Forecasting house prices, stock values, etc.
- Financial Forecasting: Predicting economic indicators.
- Risk Management: Assessing relationships between risk factors and outcomes.

---

#### Advantages

- Simple and interpretable.
- Computationally efficient.
- Serves as a baseline for more complex models.

---

#### Limitations

- Assumes linearity, which may not hold for all datasets.
- Sensitive to outliers and multicollinearity.
- Limited in capturing complex relationships.

---

#### Others

Linear regression remains a foundational algorithm in machine learning, widely used for its simplicity and effectiveness in modeling linear relationships.