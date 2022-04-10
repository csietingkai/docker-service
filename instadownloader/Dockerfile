FROM python:3.8.0-alpine
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY src /app
WORKDIR /app
ENV PATH=/home/app/.local/bin:$PATH
EXPOSE 5000
CMD [ "python", "./app.py" ]
