FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir /code

WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt

CMD python manage.py collectstatic
CMD python manage.py migrate
CMD python manage.py load_fixtures

CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8000", "--chdir", "swapi", "wsgi:application"]