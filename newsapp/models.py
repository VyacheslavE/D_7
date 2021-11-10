from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator
#from newsapp.models import *


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete = models.CASCADE)
    author_rate = models.IntegerField(default=0)

    def update_rating(self):
        posts_rate = self.post_set.all().aggregate(postRate=Sum('post_rate'))
        p_rate = 0
        p_rate += posts_rate.get('postRate')

        comments_rate = self.author_user.comment_set.all().aggregate(commentRate=Sum('comment_rate'))
        c_rate = 0
        c_rate += comments_rate.get('commentRate')

        self.author_rate = p_rate * 3 + c_rate
        self.save()

    def __str__(self):
        return f'{self.author_user}'


#  создаём категорию, к которой будет привязываться новость
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # названия категорий тоже не должны повторяться

    def __str__(self):
        return f'{self.name.title()}'


# Создаём модель новость
class News(models.Model):
    news_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    news_create_time = models.DateTimeField(auto_now_add=True)
    news_text = models.TextField(default="None")
    name = models.CharField(
        max_length=100,
        unique=True,  # названия не должны повторяться
    )

    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='all_news',  # все новости в категории будут доступны через поле news
    )

    def __str__(self):
        return f'{self.name.title()}: {self.news_text[:50]}  {self.news_create_time} '

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу новости
        return f'/news/{self.id}'


class NewsCategory(models.Model):
    news_temp = models.ForeignKey(News, on_delete=models.CASCADE)
    category_temp = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_news = models.ForeignKey(News, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(default = "None")
    comment_creation_time = models.DateTimeField(auto_now_add=True)
    comment_rate = models.IntegerField(default = 0)


    def like(self):
        self.comment_rate += 1
        self.save()

    def dislike(self):
        if self.comment_rate:
            self.comment_rate -= 1
            self.save()




