FROM python:3.9
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY ./src /app/src
COPY ./scripts /app/scripts
CMD ["source", "/app/scripts/start.sh"]