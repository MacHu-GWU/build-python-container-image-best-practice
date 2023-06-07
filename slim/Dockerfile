# ECR Gallery https://gallery.ecr.aws/docker/library/python
# --- stage 1 ---
# we install dependencies and run unit test
FROM public.ecr.aws/docker/library/python:3.9-slim AS build
# this is the working directory in the container
# it should have the same folder structure of your git repo
WORKDIR /usr/src/app
# copy the following file to working directory
# these file are not changing frequently, so it should go to the top of Dockerfile as a layer cache
COPY pyproject.toml \ 
    requirements.txt \
    requirements-test.txt \
    main.py \
    ./
# install virtualenv, then create virtualenv, install main and test dependencies
# since we are using Poetry to resolve the deterministic dependency, 
# this layer is not chaging frequently as before
RUN pip install virtualenv && \
    virtualenv .venv && \
    /usr/src/app/.venv/bin/pip install -r requirements.txt && \
    /usr/src/app/.venv/bin/pip install -r requirements-test.txt
# copy the source code and test cases to the working directory
# these two folder are chaging frequently
COPY my_project/ ./my_project
COPY tests/ ./tests
# install the source package itself and run unit test
# after that, destroy the virtualenv. because this virtualenv has lots of unnecessary dependencies
# we should create a clean virtualenv that include necessary dependencies.
# we also clean up the wheel, setuptools, pip as well
# finally we display the total size of the virtualenv
RUN /usr/src/app/.venv/bin/pip install . && \
    /usr/src/app/.venv/bin/pytest -s ./tests && \
    rm -r .venv && \
    virtualenv .venv && \
    /usr/src/app/.venv/bin/pip install --no-cache-dir -r requirements.txt && \
    /usr/src/app/.venv/bin/pip install --no-cache-dir . && \
    /usr/src/app/.venv/bin/pip uninstall wheel setuptools pip -y && \
    du /usr/src/app/.venv/ -h
ENTRYPOINT ["/usr/src/app/.venv/bin/python", "./main.py"]


# --- stage 2 ---
# we only copy the tested, built virtualenv to the final image
FROM public.ecr.aws/docker/library/python:3.9-slim
WORKDIR /usr/src/app
COPY --from=build /usr/src/app/.venv ./.venv
COPY --from=build /usr/src/app/main.py ./
ENTRYPOINT ["/usr/src/app/.venv/bin/python", "./main.py"]
