from celery import Celery

app = Celery('tmp', broker='amqp://sqsm:sqsm1234@127.0.0.1/')

@app.task
def add_num(x,y):
    return float(x)+float(y)