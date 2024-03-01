# JSSG - Jtremesay's Static Site Generator
# Copyright (C) 2023 Jonathan Tremesaygues
#
# Dockerfile
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.
FROM ubuntu:noble AS site

# Update packages and install needed stuff
RUN apt-get update \
    && apt-get install -y --no-install-recommends npm python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/foehn

# Create venv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install python & node deps
COPY requirements.txt package.json package-lock.json ./
RUN pip install -Ur requirements.txt \
    && npm install

# Copy source dir
COPY manage.py tsconfig.json vite.config.ts entrypoint.sh ./
COPY proj/ proj/
COPY foehn/ foehn/

# Build
RUN DJANGO_DEBUG=true npm run build \
    && ./manage.py collectstatic --no-input

# Prod
EXPOSE 8002
ENTRYPOINT ["/opt/foehn/entrypoint.sh"]
CMD [ "daphne", "--bind", "0.0.0.0", "--port", "8002", "proj.asgi:application" ]