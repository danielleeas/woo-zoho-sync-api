# Use an official Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Install virtualenv
RUN python -m venv /.venv

# Activate the virtual environment and upgrade pip
RUN /.venv/bin/pip install --upgrade pip

# Copy requirements file
COPY requirements.txt .

# Install dependencies inside virtualenv
RUN /.venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variable to use the virtual environment
ENV PATH="/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Run FastAPI with Uvicorn inside virtual environment
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
