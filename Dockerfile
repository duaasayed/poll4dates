FROM python:3.11-slim
WORKDIR /poll4dates
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN python3 -m venv venv
RUN . venv/bin/activate
COPY . .
RUN pip install -r requirements.txt

