# ===============================
# Stage 1: build with all tools
# ===============================
FROM python:3.13-rc-slim AS builder

WORKDIR /app

# Install necessary tools to compile packages
RUN apt-get update && apt-get install -y gcc libffi-dev build-essential curl && \
    pip install --upgrade pip && \
    pip install uv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy only the config file
COPY pyproject.toml ./

# Generate requirements.txt file from pyproject.toml
RUN uv pip compile --output-file=requirements.txt pyproject.toml

# Install dependencies in a temporary venv
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt

# ===============================
# Stage 2: lightweight image for execution
# ===============================
FROM python:3.13-rc-slim AS runtime

# Create a non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy only the venv from the build image
COPY --from=builder /venv /venv

# Activate the venv
ENV PATH="/venv/bin:$PATH"

# Copy the app code
COPY . .

# User permissions
RUN chown -R appuser:appuser /app

# Use secure user
USER appuser

# Expose Streamlit port
EXPOSE 8501

# Launch the app
CMD ["streamlit", "run", "main_web.py", "--server.port=8501", "--server.address=0.0.0.0"]
