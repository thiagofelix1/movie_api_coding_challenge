from pyexpat import model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


class Score(models.Model):
    movie_id = models.CharField(max_length=20)
    movie_title = models.CharField(max_length=200)
    score_value = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    user_email = models.EmailField(verbose_name='email address')
    user_nickname = models.CharField(max_length=20)
    date = models.DateTimeField(default=timezone.now())


class Comment(models.Model):
    user_email = models.EmailField()
    user_nickname = models.CharField(max_length=20)
    text_comment = models.TextField()
    movie_id = models.CharField(max_length=20)
    movie_title = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now())
    comment_repeat = models.BooleanField(default=False)


class ReplayComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user_email = models.EmailField()
    user_nickname = models.CharField(max_length=20)
    text_replay_comment = models.TextField()
    date = models.DateTimeField(default=timezone.now())


class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like_result = models.BooleanField()
    user_email = models.EmailField()
    user_nickname = models.CharField(max_length=20)


class QuoteComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    text_quote_comment = models.TextField()
    movie_id = models.CharField(max_length=20)
    movie_title = models.CharField(max_length=200)
    user_email = models.EmailField()
    user_nickname = models.CharField(max_length=20)
    date = models.DateTimeField(default=timezone.now())
