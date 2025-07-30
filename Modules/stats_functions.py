import pandas as pd
import streamlit as st
import numpy as np
from scipy import stats

class StatisticalAnalyzer:
    def __init__(self, df):
        self.df = df

    def display_summary_statistics(self):
        st.subheader("Summary Statistics")
        st.write(self.df.describe(include='all'))

    def display_correlation_matrix(self):
        st.subheader("Correlation Matrix")
        st.dataframe(self.df.corr(numeric_only=True))

    def display_skewness_kurtosis(self):
        st.subheader("Skewness and Kurtosis")
        numeric_data = self.df.select_dtypes(include=np.number)
        skewness = numeric_data.skew()
        kurtosis = numeric_data.kurtosis()

        st.write("### Skewness")
        st.dataframe(skewness)
        st.write("### Kurtosis")
        st.dataframe(kurtosis)
