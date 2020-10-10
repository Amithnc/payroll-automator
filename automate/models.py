from django.db import models
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import time

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name,max_length=None): 
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        time.sleep(2)    
        return name

class employee(models.Model):
    employee_file=models.FileField(upload_to='file',storage=OverwriteStorage(),help_text="please upload file",verbose_name='employee details',default='')
    
    def __str__(self):
        return str(self.employee_file) 