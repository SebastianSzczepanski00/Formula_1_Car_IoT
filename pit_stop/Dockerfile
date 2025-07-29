FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python3 python3-pip python3.12-venv
RUN python3 -m venv /venv
COPY requirements.txt .
COPY constants.yaml .
COPY formula_1_iot_utils.py .
RUN . ./venv/bin/activate && pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
COPY pit_stop.py .
CMD ["/bin/bash", "-c", "-u", ". ./venv/bin/activate && python pit_stop.py"]
