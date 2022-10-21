FROM python:3
EXPOSE 8085
WORKDIR /django_ci
COPY ./ /django_ci
RUN pip install -r /django_ci/requirements.txt
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8085"]
