# Use the official Python 3.11 slim image for a lightweight base
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install the required Python packages from requirements.txt
RUN pip install -r requirements.txt

# Expose port 8501 for Streamlit
EXPOSE 8501

# Run the Streamlit app when the container starts
CMD ["streamlit", "run", "client.py"]
