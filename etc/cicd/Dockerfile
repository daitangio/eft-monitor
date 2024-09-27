FROM python:3.12.3-bullseye

# This build is optimized to avoid regenerating the cached images if the poetry config does not change
# if it changes, all the build is done
# otherwise, most of the time we expect only tiny modifrications to the etf_monitor/tests folders
WORKDIR /workspace
COPY ./bin/installVirtualEnv ./bin/installVirtualEnv
COPY poetry.lock pyproject.toml ./
RUN ls -l
RUN ./bin/installVirtualEnv
COPY tests ./tests
COPY etf_monitor ./etf_monitor
COPY ./bin/doPylint  ./bin/doPylint 
COPY pylint.rc ./
# RUN ./bin/doPylint
RUN mkdir  /workspace/data
CMD fastapi dev etf_monitor/server.py
