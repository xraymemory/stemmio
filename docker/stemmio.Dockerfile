FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN pip install spleeter

RUN apt update
RUN apt -y install ffmpeg
RUN apt -y install strace

WORKDIR /workspace/

COPY ./docker/spleeter_test.m4a .

ENTRYPOINT ["/bin/bash"]
