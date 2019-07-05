FROM python:3.7
RUN mkdir /scrap
RUN mkdir -p /var/log/supervisor
RUN pip install gunicorn json-logging-py
WORKDIR /scrap
ADD requirements.txt /scrap/
RUN apt-get update 
RUN apt-get install -y software-properties-common
RUN pip3 install -r requirements.txt
ADD . /scrap
COPY scrap.conf /etc/supervisor/conf.d/scrap.conf
VOLUME [ "/scrap" ]
EXPOSE 5000:5000