FROM python:{{cookiecutter.python}}

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -e .

EXPOSE 5000

ENTRYPOINT ["/usr/src/app/conf.sh"]

