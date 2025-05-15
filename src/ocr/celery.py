import os

from django.conf import settings
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ocr.settings")

app = Celery("ocr")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
    print(f"Task ID: {self.request.id}")
    print(f"Task Name: {self.name}")
    print(f"Task Args: {self.request.args}")
    print(f"Task Kwargs: {self.request.kwargs}")
    print(f"Task Requeue: {self.request.requeue}")
    print(f"Task Delivery Info: {self.request.delivery_info}")