FROM python:3.11-slim

WORKDIR /worker

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /worker

CMD ["python", "worker.py"]