# Python image
FROM python:3.11-slim-buster

# Set the working directory
WORKDIR .

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements_web.txt

# Copy the rest of the source code
COPY . .

# Run Python script
CMD ["streamlit", "run", "main.py"]
