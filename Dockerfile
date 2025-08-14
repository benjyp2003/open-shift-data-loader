FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Command to run the application using uvicorn
CMD ["uvicorn", "services.fastapi:app", "--host", "0.0.0.0", "--port", "8000"]