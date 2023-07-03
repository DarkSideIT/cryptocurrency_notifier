FROM python:3


WORKDIR /cryptocurrency_notifier


COPY requirements.txt .


RUN pip install -r requirements.txt


COPY . .


ENV DJANGO_SETTINGS_MODULE=cryptocurrency_notifier.settings


RUN python manage.py migrate


EXPOSE 5000


CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]