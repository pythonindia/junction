from celery import shared_task


@shared_task
def add(x, y):
    # dummy task
    print x+y
