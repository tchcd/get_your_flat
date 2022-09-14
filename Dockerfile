FROM python:3.8

RUN mkdir -p /app

WORKDIR /app

COPY . /app

ENV TZ Europe/Moscow RUN echo "Preparing geographic area ..."

RUN pip install -r requirements.txt

ENV PYTHONPATH /app

#ENTRYPOINT ["/get_your_flat/run.sh"]
CMD ["python", "app.py"]