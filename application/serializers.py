from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import Comment
from.movie_api import get_movie_by_id


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    nickname = serializers.CharField(max_length=20)
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100)


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ScoreSerializer(serializers.Serializer):
    movie_id = serializers.CharField(max_length=20)
    score_value = serializers.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )


class PostCommentSerializer(serializers.Serializer):
    text_comment = serializers.CharField()
    movie_id = serializers.CharField(max_length=20)


class PostReplayCommentSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()
    text_replay_comment = serializers.CharField()

    def validate_comment_id(self, value):
        """
        Check comment id exists
        """
        comment = Comment.objects.filter(id=value).first()
        if not comment:
            raise serializers.ValidationError("Comment not exists")
        return value


class PostLikeSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()
    like_result = serializers.BooleanField()

    def validate_comment_id(self, value):
        """
        Check comment id exists
        """
        comment = Comment.objects.filter(id=value).first()
        if not comment:
            raise serializers.ValidationError("Comment not exists")
        return value


class PostQuoteSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()
    text_quote_comment = serializers.CharField()
    movie_id = serializers.CharField(max_length=20)
    movie_title = ""

    def validate_comment_id(self, value):
        """
        Check comment id exists
        """
        comment = Comment.objects.filter(id=value).first()
        if not comment:
            raise serializers.ValidationError("Comment not exists")
        return value

    def validate_movie_id(self, value):
        """
        Check movie_id exists
        """
        movie_response = get_movie_by_id(value)
        if "Error" in movie_response:
            raise serializers.ValidationError("movie id not exists")
        if 'Title' in movie_response:
            self.movie_title = movie_response['Title']
        return value


class DeleteCommentSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()

    def validate_comment_id(self, value):
        """
        Check comment id exists
        """
        comment = Comment.objects.filter(id=value).first()
        if not comment:
            raise serializers.ValidationError("Comment not exists")
        return value


class MarkCommentRepeatSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()

    def validate_comment_id(self, value):
        """
        Check comment id exists
        """
        comment = Comment.objects.filter(id=value).first()
        if not comment:
            raise serializers.ValidationError("Comment not exists")
        return value


class MakeModeratorSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    token_moderator = serializers.CharField()
