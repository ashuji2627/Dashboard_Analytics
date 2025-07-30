#data_visualization.py

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import io
import base64

class DynamicVisualizer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.categorical = df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.numerical = df.select_dtypes(include=['int', 'float']).columns.tolist()
        self.columns = df.columns.tolist()

    def pie_chart(self, col):
        fig = px.pie(self.df, names=col, title=f"{col} Distribution")
        fig.update_traces(textinfo='percent+label', pull=[0.05] * len(self.df[col].unique()))
        return fig

    def bar_chart(self, group_col, value_col, time_col=None):
        if time_col and time_col in self.df.columns:
            return px.bar(self.df, x=group_col, y=value_col, color=group_col, animation_frame=time_col)
        grouped_df = self.df.groupby(group_col)[value_col].sum().reset_index()
        return px.bar(grouped_df, x=group_col, y=value_col, color=group_col)

    def scatter_plot(self, x, y, color=None, time=None):
        return px.scatter(self.df, x=x, y=y, color=color, animation_frame=time)

    def line_chart(self, x, y, color=None, frame=None):
        return px.line(self.df, x=x, y=y, color=color, animation_frame=frame)

    def area_chart(self, x, y, color=None, frame=None):
        return px.area(self.df, x=x, y=y, color=color, animation_frame=frame)

    def histogram(self, col, frame=None):
        return px.histogram(self.df, x=col, nbins=30, animation_frame=frame)

    def heatmap(self, x, y, z, frame=None):
        if frame:
            return px.density_heatmap(self.df, x=x, y=y, z=z, animation_frame=frame, histfunc="avg")
        pivot = self.df.pivot_table(index=y, columns=x, values=z, aggfunc='mean')
        return px.imshow(pivot, text_auto=True)

    def boxplot(self, x, y, frame=None):
        return px.box(self.df, x=x, y=y, animation_frame=frame)

    def treemap(self, path, value):
        return px.treemap(self.df, path=path, values=value)

    def geospatial(self, color=None, projection="natural earth"):
        if "Latitude" in self.df.columns and "Longitude" in self.df.columns:
            return px.scatter_geo(self.df, lat='Latitude', lon='Longitude', color=color, projection=projection)
        elif "Location" in self.df.columns:
            return px.scatter_geo(self.df, locations="Location", locationmode="country names", color=color, projection=projection)
        else:
            raise ValueError("Requires 'Latitude'/'Longitude' or 'Location' column")
        
    def generate_plot():
        plt.figure()
        plt.plot([1, 2, 3], [4, 5, 6])  # Example plot
        plt.title("Sample Plot")
    
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        return encoded_image
