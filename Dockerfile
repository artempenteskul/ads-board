FROM python:3.9.6-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

WORKDIR /app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip3 install --upgrade pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]


# --- commands to run ---
# docker build .
# docker run -d -p 8000:8000 {image}
