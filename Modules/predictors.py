import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

class PredictionEngine:
    def __init__(self, df):
        self.df = df

    def simple_linear_regression(self):
        st.subheader("📐 Simple Linear Regression")
        numeric_columns = self.df.select_dtypes(include='number').columns.tolist()

        if len(numeric_columns) < 2:
            st.warning("Need at least two numerical columns for regression.")
            return

        x_column = st.selectbox("Select independent variable (X):", numeric_columns)
        y_column = st.selectbox("Select dependent variable (Y):", [col for col in numeric_columns if col != x_column])

        X = self.df[[x_column]]
        y = self.df[y_column]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        st.write("### Model Evaluation")
        st.write(f"R-squared: {r2_score(y_test, predictions):.2f}")
        st.write(f"MSE: {mean_squared_error(y_test, predictions):.2f}")

        st.line_chart(pd.DataFrame({"Actual": y_test.values, "Predicted": predictions}, index=y_test.index))