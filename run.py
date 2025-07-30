# run.py

import streamlit as st
import pandas as pd
from Modules.data_visualization import DynamicVisualizer
from api_handler import fetch_data_from_api
from Modules.stats_functions import StatisticalAnalyzer
from Modules.predictors import PredictionEngine
import base64
from io import StringIO
import pdfplumber

st.set_page_config(page_title="Shop Trends Dashboard", layout="wide")

st.markdown(
    """
    <h1 style='text-align: center;'>Shop Trends Dashboard</h1>
    <p style='text-align: center; color: grey;'>Visualizing customer shopping behavior and trends</p>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_data(file) -> pd.DataFrame:
    try:
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        elif file.name.endswith((".xls", ".xlsx")):
            return pd.read_excel(file)
        elif file.name.endswith(".json"):
            return pd.read_json(file)
        elif file.name.endswith(".pdf"):
            with pdfplumber.open(file) as pdf:
                text = "\n".join(page.extract_text() or '' for page in pdf.pages)
                # Try to parse text into table
                tables = []
                for page in pdf.pages:
                    table = page.extract_table()
                    if table:
                        tables.append(pd.DataFrame(table[1:], columns=table[0]))
                if tables:
                    return pd.concat(tables, ignore_index=True)
                else:
                    raise ValueError("No table found in PDF.")
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        st.error(f"File loading error: {e}")
        return pd.DataFrame()

# Adding background color image from local host
def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

add_bg_from_local("img.avif")

st.title("Upload Data")

# Option for Upload or API
option = st.radio("Choose data source:", ["Upload CSV", "Provide API URL"])

df = pd.DataFrame()
if option == "Upload CSV":
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv", "xls", "xlsx", "json", "pdf"])
    if uploaded_file is not None:
        df =load_data(uploaded_file)
elif option == "Provide API URL":
    api_url = st.text_input("Enter API URL")
    if api_url:
        try:
            df = fetch_data_from_api(api_url)
            st.success("Data fetched successfully!")
        except Exception as e:
            st.error(str(e))

if df.empty:
    st.warning("Please upload a CSV or provide a valid API URL.")
    st.stop()

# Preprocessing
df.columns = df.columns.str.strip().str.replace(' +', ' ', regex=True)
if 'Purchase Amount' in df.columns:
    df.rename(columns={'Purchase Amount': 'Amount'}, inplace=True)

viz = DynamicVisualizer(df)
analyzer = StatisticalAnalyzer(df)
predictor = PredictionEngine(df)

# --- KPIs ---
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", len(df))
col2.metric("Avg Purchase", f"${df['Amount'].mean():.2f}" if 'Amount' in df else "N/A")
col3.metric("Avg Rating", f"{df['Review Rating'].mean():.2f}" if 'Review Rating' in df else "N/A")

# --- Dynamic Visual Section ---
with st.expander("Dynamic Plotly Visualizations"):
    plot_type = st.selectbox("Plot Type", [
        "Pie Chart", "Bar Chart", "Scatter Plot", "Line Chart", "Area Chart",
        "Histogram", "Heatmap", "Boxplot", "Treemap", "Geospatial"
    ])

    if plot_type == "Pie Chart":
        col = st.selectbox("Column", viz.categorical)
        st.plotly_chart(viz.pie_chart(col), use_container_width=True)

    elif plot_type == "Bar Chart":
        group = st.selectbox("Group By", viz.categorical)
        value = st.selectbox("Value", viz.numerical)
        time = st.selectbox("Time (Optional)", ['None'] + viz.categorical)
        st.plotly_chart(viz.bar_chart(group, value, time if time != 'None' else None), use_container_width=True)

    elif plot_type == "Scatter Plot":
        x = st.selectbox("X-Axis", viz.numerical)
        y = st.selectbox("Y-Axis", viz.numerical, index=1)
        color = st.selectbox("Color (Optional)", ['None'] + viz.columns)
        time = st.selectbox("Time (Optional)", ['None'] + viz.columns)
        st.plotly_chart(viz.scatter_plot(x, y,
                                         color=None if color == 'None' else color,
                                         time=None if time == 'None' else time),
                        use_container_width=True)

    elif plot_type == "Line Chart":
        x = st.selectbox("X-Axis", viz.columns)
        y = st.selectbox("Y-Axis", viz.numerical)
        color = st.selectbox("Color (Optional)", ['None'] + viz.categorical)
        frame = st.selectbox("Frame (Optional)", ['None'] + viz.categorical)
        st.plotly_chart(viz.line_chart(x, y,
                                       color if color != 'None' else None,
                                       frame if frame != 'None' else None),
                        use_container_width=True)

    elif plot_type == "Area Chart":
        x = st.selectbox("X-Axis", viz.columns)
        y = st.selectbox("Y-Axis", viz.numerical)
        color = st.selectbox("Color (Optional)", ['None'] + viz.categorical)
        frame = st.selectbox("Frame (Optional)", ['None'] + viz.categorical)
        st.plotly_chart(viz.area_chart(x, y,
                                       color if color != 'None' else None,
                                       frame if frame != 'None' else None),
                        use_container_width=True)

    elif plot_type == "Histogram":
        col = st.selectbox("Column", viz.numerical)
        frame = st.selectbox("Frame (Optional)", ['None'] + viz.categorical)
        st.plotly_chart(viz.histogram(col, frame if frame != 'None' else None), use_container_width=True)

    elif plot_type == "Heatmap":
        x = st.selectbox("X-Axis", viz.categorical)
        y = st.selectbox("Y-Axis", [c for c in viz.categorical if c != x])
        z = st.selectbox("Value", viz.numerical)
        frame = st.selectbox("Frame (Optional)", ['None'] + viz.categorical)
        st.plotly_chart(viz.heatmap(x, y, z, frame if frame != 'None' else None), use_container_width=True)

    elif plot_type == "Boxplot":
        x = st.selectbox("X-Axis (Category)", viz.categorical)
        y = st.selectbox("Y-Axis (Numeric)", viz.numerical)
        frame = st.selectbox("Frame (Optional)", ['None'] + viz.categorical)
        st.plotly_chart(viz.boxplot(x, y, frame if frame != 'None' else None), use_container_width=True)

    elif plot_type == "Treemap":
        path = st.multiselect("Hierarchy", viz.categorical, max_selections=3)
        value = st.selectbox("Value", viz.numerical)
        if path:
            st.plotly_chart(viz.treemap(path, value), use_container_width=True)

    elif plot_type == "Geospatial":
        projection = st.selectbox("Projection", [
            "equirectangular", "mercator", "orthographic", "natural earth", "kavrayskiy7",
            "miller", "robinson", "sinusoidal"
        ])
        color = st.selectbox("Color By (Optional)", ['None'] + viz.columns)
        try:
            fig = viz.geospatial(color=None if color == 'None' else color, projection=projection)
            st.plotly_chart(fig, use_container_width=True)
        except ValueError as e:
            st.warning(str(e))

# --- Stats & Prediction Section ---
with st.expander("Statistical Summary"):
    analyzer.display_summary_statistics()
    analyzer.display_correlation_matrix()
with st.expander("Predictions"):
    analyzer.display_skewness_kurtosis()
    predictor.simple_linear_regression()

with st.expander("View Raw Data"):
    st.dataframe(df)
