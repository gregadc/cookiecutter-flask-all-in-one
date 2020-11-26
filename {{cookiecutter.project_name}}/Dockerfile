FROM python:{{cookiecutter.python_version}}

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -e .

EXPOSE 5000

COPY . /code

ENTRYPOINT ["/code/conf.sh"]

