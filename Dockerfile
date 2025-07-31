# Use Python base image
FROM python:3.13.5

# Set working directory
WORKDIR /run

# Copy dependency file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose Streamlit default port (change if using Flask/Dash)
EXPOSE 8501

# Run the app (adjust command for Flask, Dash, etc.)
CMD ["streamlit", "run", "run.py", "--server.port=8501", "--server.enableCORS=false"]
