# TO DO: THIS FILE

FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN pip install spleeter

RUN apt update
RUN apt -y install ffmpeg

ENTRYPOINT ["/bin/bash"]
