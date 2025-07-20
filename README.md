# Build and Run a Flask Docker container

Building the docker image uses [Docker for Windows](https://docs.docker.com/desktop/windows/install/) on
*Windows 10 Home edition* where only ```WSL 2``` is available.

With *Windows 10 Pro* you can choose to use a
[Hyper-V backend](https://allthings.how/how-to-install-docker-on-windows-10/) or ```WSL 2```.

## Podman Build Instructions

```shell
# Define variables
PS C:\Users\sjfke> $name = "crazy-frog"
PS C:\Users\sjfke> $image = "localhost/flask-play"

# Build image
PS C:\Users\sjfke> podman build --tag $image --no-cache --squash -f .\Dockerfile
PS C:\Users\sjfke> podman image ls $image

# Run, test, delete container
PS C:\Users\sjfke> podman run --name $name -p 8080:8080 -d $image
PS C:\Users\sjfke> podman logs $name
PS C:\Users\sjfke> podman exec -it $name sh
PS C:\Users\sjfke> podman kube generate $name -f .\flask-pod.yaml # generate pod manifest
PS C:\Users\sjfke> start http://localhost:8080
PS C:\Users\sjfke> podman rm --force $name

# Run, test, delete container using podman play kube
PS C:\Users\sjfke> podman play kube --start .\flask-pod.yaml
PS C:\Users\sjfke> $container = "$name-pod-$name"
PS C:\Users\sjfke> podman exec -it $container bash
PS C:\Users\sjfke> start http://localhost:8080
PS C:\Users\sjfke> podman play kube --down .\flask-pod.yaml

# Development, test (wash repeat cycle)
PS C:\Users\sjfke> podman build --tag $image --no-cache --squash -f .\Dockerfile
PS C:\Users\sjfke> podman play kube --replace .\flask-pod.yaml
PS C:\Users\sjfke> start http://localhost:8080

# Image Maintenance
PS C:\Users\sjfke> podman image prune
```

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
PS C:\Users\sjfke> start http://localhost:8080
PS C:\Users\sjfke> docker rm --force $name
```

## Docker Compose

```shell
# Once compose.yaml is created, see references (ii, iii)
PS C:\Users\sjfke> docker compose -f .\compose.yaml up -d # builds flask-play-web image
PS C:\Users\sjfke> start http://localhost:8080
PS C:\Users\sjfke> start http://localhost:3000           # admin/admin
PS C:\Users\sjfke> docker compose -f .\compose.yaml down 

# Development, test (wash repeat cycle)
PS C:\Users\sjfke> docker compose -f .\compose.yaml down web
PS C:\Users\sjfke> docker compose build web
PS C:\Users\sjfke> docker compose -f .\compose.yaml up -d web
PS C:\Users\sjfke> start http://localhost:8080
```

1. [Docker: Overview of Docker Compose](https://docs.docker.com/compose/)
2. [Docker: Compose specification](https://docs.docker.com/compose/compose-file)
3. [Docker: Compose specification - ports](https://docs.docker.com/compose/compose-file/#ports)

## Docker Image Maintenance

```bash
PS C:\Users\sjfke> docker image prune # clean up dangling images
PS C:\Users\sjfke> docker system prune 
PS C:\Users\sjfke> docker rmi $(docker images -f 'dangling=true' -q)       # UNIX, images with no tags
PS C:\Users\sjfke> $d = docker images -f 'dangling=true' -q; docker rmi $d # Powershell, images with no tags
```

* [DigitalOcean: How To Remove Docker Images, Containers, and Volumes](https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes)

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