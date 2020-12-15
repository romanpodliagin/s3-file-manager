FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install nano -y

RUN mkdir /src
WORKDIR /src
ADD requirements.txt /src/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ADD . /src/

RUN python manage.py migrate
#RUN python manage.py load_models

RUN python manage.py collectstatic --noinput
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('testuser', 'testuser@gmail.com', 'testpwd')" | python manage.py shell
