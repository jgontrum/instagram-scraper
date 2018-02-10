FROM python:3.6
MAINTAINER Johannes Gontrum <gontrum@me.com>

RUN pip install virtualenv

COPY . /app
RUN cd /app && make clean && make

ENV PORT 80
EXPOSE 80

CMD ["bash", "/app/start.sh"]
