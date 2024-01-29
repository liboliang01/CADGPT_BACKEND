# Start From Code (Recommended)
## Environment
Anaconda + Python3.11 
```
conda create -n YOUR_ENV_NAME python=3.11
pip install -r requirements
```

## Start Server
```
start /min python manage.py runserver 0.0.0.0:8001
```


# Start From Docker Image

```
docker run -p 8001:8001 -d cadgpt_backend
```