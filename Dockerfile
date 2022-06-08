FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

