# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy necessary files
COPY app.py app.py
COPY models/ models/
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
