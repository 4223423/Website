from django.db import models
import os

# 함수를 사용하는 방법과 class를 사용하는 방법

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length = 100, blank = True)
    content = models.TextField()
    
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d',blank=True)

    
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d',blank=True)
    
    def __str__(self) :
        return f'[{self.pk}]{self.title}' # 번호, 인덱스 출력
    
    
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
    
    def get_file_name(self) :
        return os.path.basename(self.file_upload.name)
    def get_file_ext(self) :
        return self.get_file_name().split('.')[-1]
    #author : 추후에 작성 예정.

# Create your models here.
