FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /src
WORKDIR /src
ADD requirements.txt /src/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ADD . /src/

RUN python manage.py migrate
RUN python manage.py load_models
