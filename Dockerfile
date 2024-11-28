FROM python:3.12

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock /code/
COPY debs/libssl.deb /code/
COPY debs/wkhtmltox.deb /code/
RUN pip install pipenv && pipenv install --system
RUN apt update && apt install -y xfonts-75dpi xfonts-base
RUN dpkg -i /code/libssl.deb
RUN dpkg -i /code/wkhtmltox.deb

COPY . /code/

RUN python manage.py collectstatic --no-input

COPY static /code/static/

