FROM python:3.10.6
COPY . /app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python run.py