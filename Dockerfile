FROM python:3.10
COPY . /home/
WORKDIR /home/
RUN apt-get update -y
RUN pip install flask jsonlint python-dotenv
RUN pip install --upgrade pip
RUN apt-get install nano -y
RUN pip install --upgrade pip 
RUN pip install --no-cache-dir --upgrade -r /home/requirements.txt
CMD hotname -I
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
RUN python3 /home/app.py
#RUN apt-get install python3 -y
#RUN apt-get install python-pip -y
#RUN pip3 install flask -ypip install dotenv-python
#ENTRYPOINT FLASK_AP P=/home/app.py flask run --host=0.0.0.0
