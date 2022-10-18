FROM python

WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip freeze

COPY manage.py manage.py
COPY proj proj
COPY chart chart
COPY foehn foehn

RUN ./manage.py collectstatic --no-input
CMD ./manage.py migrate && gunicorn -b 0.0.0.0 -w4 -kgevent proj.wsgi