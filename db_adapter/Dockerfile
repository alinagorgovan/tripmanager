FROM python:3.6
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
WORKDIR /db_adapter
COPY . /db_adapter
EXPOSE 5001
CMD ["python3.6", "db_adapter.py"]
