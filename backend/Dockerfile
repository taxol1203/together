FROM python:3.6.8
ENV PYTHONUNBUFFERED=1
WORKDIR /home/ubuntu/Together/backend
COPY requirements.txt ./
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
#COPY . .
#CMD ["python", "manage.py", "runserver", "8000:8000"]
#EXPOSE 8000
