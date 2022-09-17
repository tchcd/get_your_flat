FROM python:3.8

RUN mkdir -p /app

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install openssh-server -y
RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 app
RUN echo 'app:psswrd' | chpasswd
RUN service ssh start

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD ["bash", "run.sh"]
