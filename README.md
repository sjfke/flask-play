# Build and Run a Flask Docker container

Building the docker image uses [Docker for Windows](https://docs.docker.com/desktop/windows/install/) on
*Windows 10 Home edition* where only ```WSL 2``` is available.

With *Windows 10 Pro* you can choose to use a
[Hyper-V backend](https://allthings.how/how-to-install-docker-on-windows-10/) or ```WSL 2```.

The documentation shows 

* running ``podman`` and ``podman-desktop`` on ``Linux`` but it is also possible on ``Windows``.
* running ``docker`` and ``docker-desktop`` on ``Windows`` but it is also possible on ``Linux``.

## Podman Prep Instructions

```shell
# Create podman volumes
sjfke@morpheus$ podman volume create postgres-flask-play
sjfke@morpheus$ podman volume create mongodb-flask-play
sjfke@morpheus$ podman volume create mongoconfigdb-flask-play

```
### Podman Compose Instructions

Uses the same ``compose.yaml`` written for the ``docker`` approach. 

```shell

# Using compose.yaml file
sjfke@morpheus$ podman compose -f ./compose.yaml up -d mongo # start MongoDB container
sjfke@morpheus$ podman exec -it flask-play-mongo-1 mongosh mongodb://root:example@localhost:27017 # mongosh
# Add contents as described in 'tests\momgodb-test-data.txt'

# Using compose.yaml file
sjfke@morpheus$ podman play kube --start ./pods/flask-play-mongo.yaml
sjfke@morpheus$ podman exec -it flask-play-mongo-1-pod mongosh mongodb://root:example@localhost:27017 # mongosh
# Add contents as described in 'tests\momgodb-test-data.txt'

# Define variables
sjfke@morpheus$ export CONTAINER_NAME="crazy-frog"
sjfke@morpheus$ export IMAGE_NAME= "localhost/flask-play"

# Build image
sjfke@morpheus$ podman build --tag $image --no-cache --squash -f ./Dockerfile
sjfke@morpheus$ podman image ls $image

# Run, test, delete container
sjfke@morpheus$ podman run --name $name -p 8080:8080 -d $image
sjfke@morpheus$ podman logs ${CONTAINER_NAME}
sjfke@morpheus$ podman exec -it ${CONTAINER_NAME} sh
sjfke@morpheus$ podman kube generate ${CONTAINER_NAME} -f ./pods/flask-play-web-1.yaml # generate pod manifest
sjfke@morpheus$ /usr/bin/firefox http://localhost:8485
sjfke@morpheus$ podman rm --force $name

# Image Maintenance
sjfke@morpheus$ podman image prune
```

### Podman Play Kube Instructions

```shell
# Preparation
sjfke@morpheus$ podman network create flask-play_net

# Create DataBase secrets (TODO)
# sjfke@morpheus$ podman secret create --env=true my_secret MYSECRET

# Using Play Kube Pod files 
sjfke@morpheus$ podman play kube --start ./pods/flask-play-mongo.yaml --net flask-play_net
sjfke@morpheus$ podman exec -it flask-play-mongo-1-pod mongosh mongodb://root:example@localhost:27017 # mongosh
# Add contents as described in 'tests\momgodb-test-data.txt'

# Run, test, delete container using podman play kube
sjfke@morpheus$ podman play kube --start ./pods/flask-play-dbgate.yaml --net flask-play_net
sjfke@morpheus$ podman play kube --start ./pods/flask-play-mongo.yaml --net flask-play_net
sjfke@morpheus$ podman play kube --start ./pods/flask-play-postgres.yaml --net flask-play_net
sjfke@morpheus$ podman play kube --start ./pods/flask-play-web.yaml --net flask-play_net

sjfke@morpheus$ /usr/bin/firefox http://localhost:8485
sjfke@morpheus$ podman play kube --down ./pods/flask-play-web.yaml

# Development, test (wash repeat cycle)
sjfke@morpheus$ export IMAGE="docker.io/library/flask-play-web"
sjfke@morpheus$ podman build --tag ${IMAGE} --no-cache --squash -f ./Dockerfile
sjfke@morpheus$ podman play kube --replace ./pods/flask-play-web.yaml --net flask-play_net
sjfke@morpheus$ /usr/bin/firefox http://localhost:8485
```





## Docker Compose

```shell
# Create docker volumes
PS C:\Users\sjfke> docker volume create postgres-flask-play
PS C:\Users\sjfke> docker volume create mongodb-flask-play
PS C:\Users\sjfke> docker volume create mongoconfigdb-flask-play

# Once compose.yaml is created, see references (ii, iii)
PS C:\Users\sjfke> docker compose -f .\compose.yaml up -d mongo # start MongoDB container
PS C:\Users\sjfke> docker exec -it flask-play-mongo-1 mongosh mongodb://root:example@localhost:27017 # mongosh
# Add contents as described in 'tests\momgodb-test-data.txt'

# Start the whole application
PS C:\Users\sjfke> docker compose -f .\compose.yaml up -d # builds flask-play-web image
PS C:\Users\sjfke> start http://localhost:8485
PS C:\Users\sjfke> start http://localhost:8486           # admin/admin
PS C:\Users\sjfke> docker compose -f .\compose.yaml down 

# Development, test (wash repeat cycle)
PS C:\Users\sjfke> docker compose -f .\compose.yaml down web
PS C:\Users\sjfke> docker compose build web
PS C:\Users\sjfke> docker compose -f .\compose.yaml up -d web
PS C:\Users\sjfke> start http://localhost:8485
```

1. [Docker: Overview of Docker Compose](https://docs.docker.com/compose/)
2. [Docker: Compose specification](https://docs.docker.com/compose/compose-file)
3. [Docker: Compose specification - ports](https://docs.docker.com/compose/compose-file/#ports)

## Docker Build instructions

```shell
# Define variables
PS C:\Users\sjfke> $name = "crazy-frog"
PS C:\Users\sjfke> $image = "localhost/flask-play"

# Build image
PS C:\Users\sjfke> docker build --squash -t $image -f .\Dockerfile $PWD
PS C:\Users\sjfke> docker image ls $image

# Run, test, delete container
PS C:\Users\sjfke> docker run --name $name -p 8080:8080 -d $image
PS C:\Users\sjfke> docker exec -it $name sh
PS C:\Users\sjfke> docker logs $name
PS C:\Users\sjfke> start http://localhost:8485
PS C:\Users\sjfke> docker rm --force $name
```

## Docker Image Maintenance

```bash
PS C:\Users\sjfke> docker image prune # clean up dangling images
PS C:\Users\sjfke> docker system prune 
PS C:\Users\sjfke> docker rmi $(docker images -f 'dangling=true' -q)       # UNIX, images with no tags
PS C:\Users\sjfke> $d = docker images -f 'dangling=true' -q; docker rmi $d # Powershell, images with no tags
```

* [DigitalOcean: How To Remove Docker Images, Containers, and Volumes](https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes)

## Postgresql modifications

Create the ``auth`` database

```bash
$ podman exec -it flask-play-posgres-1 /bin/bash
root@79685c6f4e96:/# createdb auth
root@79685c6f4e96:/# exit
```
[22.2. Creating a Database](https://www.postgresql.org/docs/current/manage-ag-createdb.html#MANAGE-AG-CREATEDB)

Need to grant ``podman flask-play_net network`` access to create the tables and use the ``auth`` database.

```bash
$ podman network inspect flask-play_net | grep subnet -A 5 | head -n 8
          "subnets": [
               {
                    "subnet": "10.89.0.0/24",
                    "gateway": "10.89.0.1"
               }
          ],
          "ipv6_enabled": false,
          "internal": false,
```

Update postgresql 'pg_hba.conf' file

```bash
$ podman cp flask-play-postgres-1:/var/lib/postgresql/data/pg_hba.conf .
$ gedit pg_hba.conf       
$ cat /tmp/pg_hba.conf 
# ...
# "local" is for Unix domain socket connections only
local   all             all                                     trust
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
# Podman flask-play_net IPv4 local connections:
host    all             all             10.89.0.4/24            trust
# IPv6 local connections:
host    all             all             ::1/128                 trust
# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     all                                     trust
host    replication     all             127.0.0.1/32            trust
host    replication     all             ::1/128                 trust

$ podman cp pg_hba.conf flask-play-postgres-1:/var/lib/postgresql/data/pg_hba.conf
$ podman restart flask-play-postgres-1
```
To create the tables, for the ``auth`` database.

```bash
$ podman exec -it flask-play-web-1 /bin/ash
/usr/src/app # python create-postgresql-tables.py 
/usr/src/app # exit
```

## Flask, Jinja and Python References

* [PyPi: Flask is a lightweight WSGI web application framework](https://pypi.org/project/Flask/)
* [PythonBasics: Flask HTTP methods, handle GET & POST requests](https://pythonbasics.org/flask-http-methods/)
* [PalletsProjects: Flask Quickstart](https://flask.palletsprojects.com/en/2.2.x/quickstart/)
* [TutorialsPoint: Flask Tutorial](https://www.tutorialspoint.com/flask/flask_quick_guide.htm)
* [PalletsProjects: API covers all the interfaces of Flask](https://flask.palletsprojects.com/en/2.2.x/api/)
* [PalletsProjects: Handling Application Errors](https://flask.palletsprojects.com/en/2.2.x/errorhandling/)
* [DelftStack: Flask Request Form](https://www.delftstack.com/howto/python-flask/flask-request-form/)
* [StackOverflow: How to get json data from another website in Flask?](https://stackoverflow.com/questions/33473803/how-to-get-json-data-from-another-website-in-flask)
* [StackOverflow: How to pass data to html page using flask?](https://stackoverflow.com/questions/51669102/how-to-pass-data-to-html-page-using-flask)
* [PalletsProjects: Jinja 3.0.x Template Designer Documentation](https://jinja.palletsprojects.com/en/3.0.x/templates/)
* [PyFormat: Using % and .format() for great good!](https://pyformat.info/)
* [DigitalOcean: How To Process Incoming Request Data in Flask](https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask)
* [LearnWithJason: How to Convert HTML Form Field Values to a JSON Object](https://www.learnwithjason.dev/blog/get-form-values-as-json)
* [PalletsProjects: Testing Flask Applications](https://flask.palletsprojects.com/en/2.2.x/testing/)
* [ReadTheDocs: Basic Usage of Pipenv](https://pipenv-fork.readthedocs.io/en/latest/basics.html)

## Flask, MongoDB References

* [PythonBasics: How to Set Up Flask with MongoDB](https://pythonbasics.org/flask-mongodb/)
* [PalletsProjects: MongoDB with MongoEngine](https://flask.palletsprojects.com/en/2.1.x/patterns/mongoengine/)
* [DevTo: How to spin MongoDB server with Docker and Docker Compose ](https://dev.to/sonyarianto/how-to-spin-mongodb-server-with-docker-and-docker-compose-2lef)
* [MongoDB: MongoDB Basics](https://www.mongodb.com/basics)
* [DockerHub: MongoDB document databases provide high availability and easy scalability](https://hub.docker.com/_/mongo/)
* [MongoDB: Docker and MongoDB](https://www.mongodb.com/compatibility/docker)
* [dockerhub: dbgate/dbgate](https://hub.docker.com/r/dbgate/dbgate/)
* [Securing Mongo Express web administrative interfaces](https://www.helpnetsecurity.com/2019/04/26/securing-mongo-express-web-administrative-interfaces/)

## Bootstrap References

* [GetBootstrap: Migrating to v5](https://getbootstrap.com/docs/5.0/migration/)
* [GetBootstrap: Bootstrap 5.2 Introduction](https://getbootstrap.com/docs/5.2/getting-started/introduction/)
* [GetBootstrap: Bootstrap 5.2 Reboot](https://getbootstrap.com/docs/5.2/content/reboot/)
* [GetBootstrap: Bootstrap 5.2 Grid system](https://getbootstrap.com/docs/5.2/layout/grid/)
* [*CSSTricks:* A Complete Guide to Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
* [GetBootstrap: Bootstrap 5.2 Forms](https://getbootstrap.com/docs/5.2/forms/overview/)
* [GetBootstrap: Bootstrap 5.2 Forms - Layout](https://getbootstrap.com/docs/5.2/forms/layout/)
* [GetBootstrap: Bootstrap 5.2 Form controls](https://getbootstrap.com/docs/5.2/forms/form-control/)
* [GetBootstrap: Bootstrap 5.2 Forms Checks and radios](https://getbootstrap.com/docs/5.2/forms/checks-radios/)
* [GetBootstrap: Bootstrap 5.2 Buttons](https://getbootstrap.com/docs/5.2/components/buttons/)
* [GetBootstrap: Bootstrap 5.2 Button Group](https://getbootstrap.com/docs/5.2/components/button-group/)
* [GetBootstrap: Bootstrap 5.2 Input group](https://getbootstrap.com/docs/5.2/forms/input-group/)
* [GetBootstrap: Bootstrap 5.2 Gutters](https://getbootstrap.com/docs/5.2/layout/gutters/)
* [GetBootstrap: Bootstrap 5.2 Spacing](https://getbootstrap.com/docs/5.2/utilities/spacing/)
* [GetBootstrap: Bootstrap 5.2 Flex](https://getbootstrap.com/docs/5.2/utilities/flex/)
* [W3Schools: Bootstrap 5 Text/Typography](https://www.w3schools.com/bootstrap5/bootstrap_typography.php)
* [GetBootstrap: Bootstrap 5.2 ](https://getbootstrap.com/docs/5.2/components/list-group/)
* [W3Schools: Bootstrap 5 Tutorial](https://www.w3schools.com/bootstrap5/index.php)
* [W3Schools: Bootstrap 5 Containers](https://www.w3schools.com/bootstrap5/bootstrap_containers.php)
* [W3Schools: Bootstrap 5 Grids](https://www.w3schools.com/bootstrap5/bootstrap_grid_basic.php)
* [Icons8: Free icons that match each other](https://icons8.com/icons)
* [Pixabay: Stunning free images & royalty free stock](https://pixabay.com/)


## Markdown References

* [GitHub: Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
* [MarkdownGuide: Cheat Sheet](https://www.markdownguide.org/cheat-sheet)
* [Readme.IO: Code Blocks](https://rdmd.readme.io/docs/code-blocks)

This repository provides a simple Python web application implemented using the Flask web framework and executed using
``gunicorn``. It is intended to be used to demonstrate building and test of Python Flask web applications
using [Docker](https://docs.docker.com/get-started/overview/)

Building the docker image uses [Docker for Windows](https://docs.docker.com/desktop/windows/install/) on
*Windows 10 Home edition* where only ```WSL 2``` is available. With *Windows 10 Pro* you can choose to use a
[Hyper-V backend](https://allthings.how/how-to-install-docker-on-windows-10/) or ```WSL 2```.

Application's Key files:

* config.py: GUNICORN settings;
* wsgi.py: define the pages (routes) that are visible;
* static: several bootstrap themes from [Bootstrap 4 themes](https://bootstrap.themes.guide/#themes)
* templates/base.html: boiler-plate for all html pages;
* templates/index.html: Standard Lorem Ipsum;
* templates/legal.html: Legal-style Lorem Ipsum;
* templates/pirate.html: Pirate-style Lorem Ipsum;
* templates/zombie.html: Zombie-style Lorem Ipsum

None of the bootstrap themes are enabled be default, edit ``templates/base.html`` to activate them.

## Implementation Notes

This sample Python application deploys a WSGI application using the ``gunicorn`` WSGI server. The requirements which
need to be satisfied for this to work are:

* The WSGI application code file needs to be named ``wsgi.py``.
* The WSGI application entry point within the code file needs to be named ``application``.
* The ``gunicorn`` package must be listed in the ``requirements.txt`` file for ``pip``.
* The *requirements.txt* file is generated using ``pipenv run pip freeze > requirements.txt``.

The example is derived
from [Getting Started with Flask](https://scotch.io/tutorials/getting-started-with-flask-a-python-microframework) but
has been modified to use [BootStrap 4](https://getbootstrap.com/docs/4.6/getting-started/introduction/), work
with [Green Unicorn - WSGI sever](https://docs.gunicorn.org/en/stable/), the content of the web-site changed to 
provide a sandbox for testing Flask

Other useful references:

* [The best Docker base image for your Python application (February 2021)](https://pythonspeed.com/articles/base-image-python-docker-images/)
* [Python: Official Docker Images](https://hub.docker.com/_/python)
* [Windows Subsystem for Linux Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
* [Docker on Hyper-V vs WSL 2](https://superuser.com/questions/1561465/docker-on-hyper-v-vs-wsl-2)
* [Install Docker Desktop on Windows](https://docs.docker.com/desktop/windows/install/)

## Docker File

A simple *Docker file* which using, ```python:3-alpine``` container, first it *pip installs* the required applications
specified in the *requirements.txt* file, copies the application files to the container, and finally, sets up the 
environment and starts *gunicorn*.

```bash
FROM python:3-alpine
# TODO: Put the maintainer name in the image metadata
MAINTAINER Sjfke (Geoff Collis) <gcollis@ymail.com>

# TODO: Rename the builder environment variable to inform users about application you provide them
ENV BUILDER_VERSION 1.0

# TODO: Set labels used in OpenShift to describe the builder image
LABEL io.k8s.name="Flask" \
      io.k8s.description="Sandbox for Flask Application for Docker" \
      io.k8s.display-name="Flask Sandbox" \
      io.k8s.version="0.1.0" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="Sandbox,0.1.0,Flask"

ENV PORT=8080
WORKDIR /usr/src/app

# Project uses 'pipenv' (Pipfile, Pipfile.lock), Docker needs requirements.txt
# $ pipenv run pip freeze > requirements.txt # generates requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# TODO (optional): Copy the builder files into /opt/app-root
# COPY ./<builder_folder>/ /opt/app-root/
COPY config.py ./
COPY static/* ./static/
COPY templates/* ./templates/
COPY wsgi.py ./

# TODO: Copy the S2I scripts to /usr/libexec/s2i, since openshift/base-centos7 image
# sets io.openshift.s2i.scripts-url label that way, or update that label
# COPY ./s2i/bin/ /usr/libexec/s2i

# TODO: Drop the root user and make the content of /opt/app-root owned by user 1001
# RUN chown -R 1001:1001 /opt/app-root

# This default user is created in the openshift/base-centos7 image
USER 1001

# TODO: Set the default port for applications built using this image
EXPOSE ${PORT}

# TODO: Set the default CMD for the image
CMD gunicorn -b 0.0.0.0:${PORT} wsgi
```

## MongoDB

```powershell
PS1> docker exec -it flask-play-mongo-1 mongosh --username root
```