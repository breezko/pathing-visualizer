# Use a slim Python image
FROM python:3.13-slim

# Install uv globally
RUN pip install uv

# Set work directory
WORKDIR /app

# Copy project
COPY . .

# Install dependencies globally
RUN uv pip install -e . --system

# Expose Flask's default port
EXPOSE 5050

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run app
CMD ["python", "pathing/app.py"]
