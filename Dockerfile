FROM python:3.10

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip 

RUN pip install -r requisites.txt

EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0"]
