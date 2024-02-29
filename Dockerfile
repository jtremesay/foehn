FROM ubuntu:noble
RUN apt-get update \
    && apt-get install -y --no-install-recommends npm python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Create venv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt package.json package-lock.json ./
RUN pip install -r requirements.txt \
    && pip freeze \
    && npm install
COPY manage.py vite.config.ts ./
COPY proj/ proj/
COPY chart/ chart/
COPY front/ front/
COPY foehn/ foehn/

RUN npm run build && ./manage.py collectstatic --no-input
CMD ./manage.py migrate && gunicorn -b 0.0.0.0 -w4 -kgevent proj.wsgi