FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/app.py
COPY sov33_benchmark_general.py /app/sov33_benchmark_general.py
COPY sov33_benchmark_agentic.py /app/sov33_benchmark_agentic.py
COPY sov33_model_card.md /app/sov33_model_card.md

ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

CMD ["python3", "app.py"]
