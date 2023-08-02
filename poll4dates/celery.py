from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poll4dates.settings')

app = Celery( 'celery_app',
               broker='redis://localhost:6379/0',
               backend='redis://localhost:6379/0'
            )
            
app.autodiscover_tasks()
