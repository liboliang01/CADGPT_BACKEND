FROM python:3.11-windowsservercore-ltsc2022
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["start", "/min", "python" ,"manage.py" ,"runserver" ,"0.0.0.0:8001"]