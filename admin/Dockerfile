FROM python:3.6
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
WORKDIR /admin
COPY . /admin
EXPOSE 5003
CMD ["python3.6", "admin.py"]