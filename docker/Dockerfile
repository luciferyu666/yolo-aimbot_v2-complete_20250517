
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python","cli/main.py","--config","config/kmbox_net.yaml","--source","examples/sample_frame.jpg"]
