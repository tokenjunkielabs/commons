FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/agent

COPY requirements.txt /opt/agent/requirements.txt
RUN pip install --no-cache-dir -r /opt/agent/requirements.txt

COPY agent.py /opt/agent/agent.py

LABEL qfbench2.interface_version="2.0"

ENTRYPOINT ["python", "/opt/agent/agent.py"]
