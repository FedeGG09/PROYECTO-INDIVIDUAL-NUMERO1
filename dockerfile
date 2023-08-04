FROM python:3.10.8
COPY . carp1/carp2/carp3
WORKDIR /carp1/carp2/carp3
RUN pip install -r requirements.txt
ENTRYPOINT uvicorn --host 0.0.0.0 main:app --reload
