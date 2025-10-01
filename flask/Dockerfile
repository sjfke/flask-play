FROM python:3-alpine
# Change User to perform privileged actions
USER 0
# TODO: Rename the builder environment variable to inform users about application you provide them
# ENV BUILDER_VERSION 1.0
ENV UID=1001
ENV PORT=8080

# TODO: Set labels used in OpenShift to describe the builder image
LABEL io.k8s.name="Flask" \
      io.k8s.description="Sandbox for Flask Application for Docker" \
      io.k8s.display-name="Flask Sandbox" \
      io.k8s.version="0.1.0" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="Sandbox,0.1.0,Flask"



# Project uses 'pipenv' (Pipfile, Pipfile.lock), Docker needs requirements.txt
# $ pipenv run pip freeze > requirements.txt # generates requirements.txt
WORKDIR /tmp
COPY requirements.txt ./
RUN pip install --root-user-action=ignore --no-cache-dir -r requirements.txt && rm /tmp/requirements.txt

# TODO (optional): Copy the builder files into /opt/app-root
# COPY ./<builder_folder>/ /opt/app-root/
WORKDIR /usr/src/app

# Copies ./<builder_folder>/ /usr/src/app
COPY gunicorn.config.py ./
COPY create-postgresql-tables.py drop-postgresql-tables.py ./
COPY project/*.py ./project/
COPY project/static ./project/static/
COPY project/templates ./project/templates/

# TODO: Drop the root user and make the content of /opt/app-root owned by user 1001
# RUN chown -R 1001:1001 /opt/app-root

# This default user is created in the openshift/base-centos7 image
# USER ${UID}

# TODO: Set the default port for applications built using this image
EXPOSE ${PORT}

# TODO: Set the default CMD for the image
# CMD gunicorn -b 0.0.0.0:${PORT} wsgi
# TODO: investigate this form
# ENTRYPOINT ["my-program", "start"] # https://docs.docker.com/reference/build-checks/json-args-recommended/
# "Application Factory” Pattern: gunicorn --workers=2 'project:create_app()', see project/__init__.py
CMD gunicorn -b 0.0.0.0:${PORT} 'project:create_app()'
# CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "project:create_app()"] # ENV not supported in this CMD form
# CMD tail -F /dev/null # docker run -it flask-auth-web /bin/bash