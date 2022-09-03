FROM python:3.8

RUN mkdir -p /get_your_flat
WORKDIR /get_your_flat

COPY . /get_your_flat/

ENV TZ Europe/Moscow RUN echo "Preparing geographic area ..."
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#RUN apt-get update
#RUN curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN apt-get install ./google-chrome*.deb --yes
#RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
#RUN rm google-chrome-stable_current_amd64.deb

RUN pip install -r requirements.txt

ENV PYTHONPATH /get_your_flat

CMD ["python", "app.py"]