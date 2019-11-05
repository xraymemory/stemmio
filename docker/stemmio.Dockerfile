FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN pip install spleeter

RUN apt update
RUN apt -y install ffmpeg
RUN apt -y install strace

ENTRYPOINT ["/bin/bash"]
