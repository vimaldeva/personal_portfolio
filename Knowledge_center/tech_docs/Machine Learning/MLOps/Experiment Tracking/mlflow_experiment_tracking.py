import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, root_mean_squared_error
import mlflow
from mlflow.models import infer_signature

input_file_path = "../data/source_data.csv"
columns_to_drop = ["date","yr_built","yr_renovated","street","statezip","country"]

source_df = pd.read_csv(input_file_path)

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("house_price_prediction")
with mlflow.start_run(run_name="Linear Regression -1", description="Basic Linear Regression model for house price prediction") as run:

    mlflow.log_artifact(input_file_path, artifact_path="input_data")

    mlflow.log_params({"Algorithm used": "Linear Regression",
                       "Shape__input_shape": source_df.shape, "input_columns": source_df.columns.tolist(),
                       "Training Conf__train_test_split": "0.2", 
                       "Training Conf__Scaling": "StandardScaler",
                       "Training Conf__OneHotEncoding": "city column",
                        "Training Conf__input_columns_dropped": columns_to_drop,

                       })

    source_df["yr_built"]
    current_year = pd.Timestamp.now().year
    source_df["yr_since_built"] = current_year - 10 - source_df["yr_built"]

    # For the above column I need to create multiple columns like built less than 5 years before, 10 years before, 20 years before, etc...help me with code for it
    source_df["built_less_than_5_years"] = source_df["yr_since_built"].apply(lambda x: 1 if x < 5 else 0)
    source_df["built_less_than_10_years"] = source_df["yr_since_built"].apply(lambda x: 1 if (x < 10) & (x >=5) else 0)
    source_df["built_less_than_20_years"] = source_df["yr_since_built"].apply(lambda x: 1 if (x < 20) & (x >=10) else 0) 
    source_df["built_less_than_30_years"] = source_df["yr_since_built"].apply(lambda x: 1 if ( x < 30) & ( x >=20) else 0) 
    source_df["built_less_than_40_years"] = source_df["yr_since_built"].apply(lambda x: 1 if ( x < 40) & ( x >=30) else 0) 
    source_df["built_less_than_50_years"] = source_df["yr_since_built"].apply(lambda x: 1 if ( x < 50) & ( x >=40) else 0) 
    source_df["built_less_than_100_years"] = source_df["yr_since_built"].apply(lambda x: 1 if ( x < 100) &  ( x >=50) else 0) 

    source_df["is_recently_renovated"] = source_df.apply(lambda x: 1 if (x["yr_renovated"] != 0) & (current_year -10 - x["yr_renovated"] < 20) else 0, axis=1)
    source_df["years_since_renovation"] = source_df.apply(lambda x: current_year -10 - x["yr_renovated"] if x["yr_renovated"] != 0 else x["yr_since_built"], axis=1)
    source_df[["yr_built","yr_since_built", "yr_renovated", "is_recently_renovated", "years_since_renovation"   ]].head(100)

    source_df["date"] = pd.to_datetime(source_df["date"])

    source_df["bedrooms"] = source_df["bedrooms"].astype(int)
    source_df["bathrooms"] = source_df["bathrooms"].astype(int)
    # convert float column to int column


    source_df.drop(columns=columns_to_drop, inplace=True)


    Q1 = source_df["price"].quantile(0.25)
    Q3 = source_df["price"].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 0.8 * IQR
    upper_bound = Q3 + 1.5 * IQR
    print("Q1 : ",Q1)
    print("Q3 : ",Q3)
    print("IQR : ",IQR)
    print("lower_bound : ",lower_bound)
    print("upper_bound : ",upper_bound)

    iqr_outliers = source_df[(source_df["price"] < lower_bound) ]
    iqr_outliers = source_df[(source_df["price"] > upper_bound)]

    # iqr_outliers = source_df[(source_df["price"] < lower_bound) | (source_df["price"] > upper_bound)]

    iqr_outliers.describe()

    source_df = source_df[(source_df["price"] >= lower_bound) & (source_df["price"] <= upper_bound)]
    print(source_df.shape)

    mlflow.log_params({"Training Conf__outliers_removed": True, 
                        "Outlier Handling Config__outlier_removal_method": "IQR",
                        "Outlier Handling Config__outlier_removal__lower_iqr": "0.8",
                        "Outlier Handling Config__outlier_removal__upper_iqr": "1.5",
                        "Outlier Handling Config__outliers_removed_lower_threshold": lower_bound,
                        "Outlier Handling Config__outliers_removed_upper_threshold": upper_bound,
                        "Outlier Handling Config__outliers_removed_total_outliers_removed": iqr_outliers.shape[0]})


    number_columns_df = source_df.select_dtypes(include=["int64","float64"])
    corr_df = number_columns_df.corr()
    plt.figure(figsize=(15,15))
    sns.heatmap(corr_df,annot=True)
    plt.savefig("./visualizations/correlation_heatmap.png")
    mlflow.log_artifact("./visualizations/correlation_heatmap.png", artifact_path="visualizations")
    hist_columns = ["price", "sqft_living", "sqft_lot", "sqft_above", "sqft_basement", "yr_since_built"]

    plt.figure(figsize=(10,10))
    plot_id = 1
    for i in hist_columns:
        plt.subplot(3,2,plot_id)
        sns.histplot(source_df[i], kde=True)
        plt.title(f"Distribution of {i}")
        plot_id += 1

    plt.tight_layout()
    plt.savefig("./visualizations/histograms.png")
    mlflow.log_artifact("./visualizations/histograms.png", artifact_path="visualizations")

    count_plot_columns = ["bedrooms", "bathrooms", "floors", "waterfront", "view", "condition" , "is_recently_renovated"]

    plt.figure(figsize =(10,10))
    plot_id = 1
    for i in count_plot_columns:
        plt.subplot(4,3,plot_id)
        sns.countplot(x=source_df[i])
        plt.title(f"Count plot of {i}")
        plot_id += 1

    plt.tight_layout()
    plt.savefig("./visualizations/count_plots.png")
    mlflow.log_artifact("./visualizations/count_plots.png", artifact_path="visualizations")

    price_vs_count_columns_comparision_columns = ["bedrooms", "bathrooms", "floors", "waterfront", "view", "condition" , "is_recently_renovated"]

    plt.figure(figsize=(15,15))
    plot_id = 1
    for i in price_vs_count_columns_comparision_columns :
        plt.subplot(4,2,plot_id)
        sns.barplot(x=source_df[i], y=source_df["price"])
        plt.title(f"Price vs {i}")
        plot_id +=1

    plt.tight_layout()
    plt.savefig("./visualizations/price_vs_count_plots.png")
    mlflow.log_artifact("./visualizations/price_vs_count_plots.png", artifact_path="visualizations")
    
    # price_vs_numerical_columns_comparision_columns = ["sqft_living", "sqft_lot", "sqft_above", "sqft_basement", "yr_since_built"]
    # plt.figure(figsize=(15,15))
    # plot_id = 1
    # for i in price_vs_numerical_columns_comparision_columns :
    #     plt.subplot(3,2,plot_id)
    #     sns.kdeplot(x=source_df[i], y=source_df["price"], fill=True, cmap='Blues')
    #     plt.title(f"Price vs {i}")
    #     plot_id +=1

    # plt.tight_layout()
    # plt.savefig("./visualizations/price_vs_numerical_plots.png")
    # mlflow.log_artifact("./visualizations/price_vs_numerical_plots.png", artifact_path="visualizations")
    
    plt.figure(figsize=(20,5) )
    sns.countplot(x=source_df["city"] )
    plt.xticks(rotation=45, ha='right')
    plt.savefig("./visualizations/city_count_plot.png")
    mlflow.log_artifact("./visualizations/city_count_plot.png", artifact_path="visualizations")

    plt.figure(figsize=(20,6))
    sns.boxplot(x="city", y="price", data=source_df)
    plt.xticks(rotation=45, ha='right')
    plt.title("Price Distribution by City")
    plt.tight_layout()
    plt.savefig("./visualizations/boxplots.png")
    mlflow.log_artifact("./visualizations/boxplots.png", artifact_path="visualizations")

    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

    # Fit and transform the 'city' column
    city_encoded = encoder.fit_transform(source_df[['city']])

    # Convert to DataFrame
    city_encoded_df = pd.DataFrame(city_encoded, columns=encoder.get_feature_names_out(['city']))

    # Drop the original 'city' column and concatenate the encoded columns
    X_encoded = pd.concat([source_df.drop('city', axis=1).reset_index(drop=True), city_encoded_df.reset_index(drop=True)], axis=1)

    x = X_encoded.drop("price", axis=1)
    y = X_encoded["price"]

    x_train,x_test, y_train,y_test = train_test_split(x,y,test_size=0.2, random_state=42)

    mlflow.log_params( {"Shape__x_train_shape": x_train.shape, "Shape__x_test_shape": x_test.shape, 
                       "Shape__y_train_shape": y_train.shape, "Shape__y_test_shape": y_test.shape})
    print(x_train.shape)
    print(x_test.shape)
    print(y_train.shape)
    print(y_test.shape)

    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()

    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    lr = LinearRegression()
    lr.fit(x_train_scaled, y_train)
    y_pred = lr.predict(x_test_scaled)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)

    signature = infer_signature(x_train, y_train)

    mlflow.log_metrics({"mean_squared_error": mse, "r2_score": r2,
                        "mean_absolute_error": mae, "root_mean_squared_error": rmse})
    
    mlflow.sklearn.log_model(sk_model =lr , name="Linear Regression Model",
                             signature=signature, input_example=x_train.iloc[:5])
    
    mlflow.log_artifact("main.py", artifact_path="training_script")

    print("Mean Squared Error: ", mse)
    print("R-squared: ", r2)
    print("Mean Absolute Error: ", mae)
    print("Root Mean Squared Error: ", rmse)




