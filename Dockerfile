FROM python:3.8

RUN mkdir -p /get_your_flat
WORKDIR /get_your_flat

COPY . /get_your_flat/

ENV TZ Europe/Moscow RUN echo "Preparing geographic area ..."

RUN pip install -r requirements.txt

ENV PYTHONPATH /get_your_flat

CMD ["python", "app.py"]