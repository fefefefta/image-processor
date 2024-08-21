FROM python:3.12

WORKDIR /app

COPY src/ /app/src/
COPY requirements.txt /app/
COPY fonts/ /app/fonts

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="/app/src:${PYTHONPATH}"

RUN mkdir -p /app/media/

CMD ["python", "/app/src/main.py"]
