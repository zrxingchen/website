import uuid
import os
# 导入django 模块
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
#引用第三方模块

# Create your models here.
# 文章分类 表
class Category(models.Model):
    name = models.CharField(max_length=255,verbose_name='类别名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


#最大限度的避免图片被覆盖
def article_img_path(instance,filename):
    # 截取后缀名
    ext = filename.split('.')[-1]
    # 计算uuid 截取 32位
    filename = '{}.{}'.format(uuid.uuid4(),ext)
    # return '{0}/{1}/{2}'.format(instance.user.id,"avatar",filename)
    return os.path.join('avatar',filename)
    # 返回前置为用户名 后置为文件名

#  创建文章表
class Article(models.Model):
    title = models.CharField(verbose_name='文章标题',max_length=50)
    author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
    img = models.ImageField(upload_to=article_img_path,null=True,blank=True,verbose_name="文章配图")
    content = models.TextField(verbose_name='文章内容')
    abstract = models.TextField(verbose_name='文章摘要',null=True,blank=True,max_length=255)
    visited = models.PositiveIntegerField(verbose_name='访问量',default=0)
    category = models.ManyToManyField('Category',verbose_name='文章分类')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    class Meta:
        verbose_name = '文章内容'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']


    def __str__(self):
        return self.title

    # 可以通过调用这个函数 ，直接返回详情页的url地址
    def get_absolute_url(self):
        return reverse("blog:blog_detail",kwargs={'a_id':self.id})

    # 访问量+1
    def increase_visited(self):
        self.visited += 1
        self.save(update_fields=['visited'])




