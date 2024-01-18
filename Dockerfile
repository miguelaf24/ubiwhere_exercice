FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

RUN mkdir /app
WORKDIR /app

COPY app.py /app
COPY park_manager.py /app
COPY *.py /app
RUN mkdir  model
RUN mkdir  data
RUN mkdir  utils

COPY utils/. /app/utils
COPY model/model.py /app/model
COPY data /app/data
COPY requirements.txt /app

RUN apt-get update -y
RUN apt-get install -y --no-install-recommends\
    python3\
    python3-pip\
    libgl1-mesa-glx\
    libglib2.0-0
RUN ldconfig

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt
EXPOSE 5000