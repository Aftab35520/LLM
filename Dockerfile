FROM python:3.10-slim

# System deps
RUN apt-get update && apt-get install -y curl

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Pull SMALL model (Render free can handle this)
RUN ollama serve & sleep 6 && ollama pull phi

EXPOSE 8000

CMD ollama serve & uvicorn main:app --host 0.0.0.0 --port 8000
