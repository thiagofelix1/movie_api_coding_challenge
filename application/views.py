from django.db.models import Avg
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MakeModeratorSerializer, PostCommentSerializer, CreateUserSerializer, PostLikeSerializer, LoginUserSerializer, PostQuoteSerializer, PostReplayCommentSerializer, ScoreSerializer, DeleteCommentSerializer, MarkCommentRepeatSerializer
from application import authorization
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsAuthenticated, IsUserBasicPermissions, IsUserAdvancedPermissions, IsUserModeratorPermissions
from .models import Like, QuoteComment, ReplayComment, Score, Comment
from.movie_api import get_movie_by_id, get_movie_by_title


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_movie(request):
    """
    Movie information by https://www.omdbapi.com/
    """
    movie_title = request.query_params.get('title')
    if not movie_title:
        return Response({
            "title": [
                "This parameter is required."
            ]
        })
    movie_data = get_movie_by_title(movie_title)
    if "Error" in movie_data:
        return Response(movie_data, status=status.HTTP_400_BAD_REQUEST)
    score_average = Score.objects.filter(movie_id=movie_data['id']).aggregate(
        Avg('score_value'))['score_value__avg']
    query_comments = Comment.objects.filter(movie_id=movie_data['id'])
    quote_comments = QuoteComment.objects.filter(movie_id=movie_data['id']).values(
        'comment__id', 'comment__text_comment', 'comment__user_nickname',
        'comment__date', 'text_quote_comment', 'user_nickname', 'date')
    comments = []
    for comment in query_comments:
        replay_comments = ReplayComment.objects.filter(
            comment=comment).values('user_nickname', 'text_replay_comment', 'date')
        likes = Like.objects.filter(comment=comment, like_result=True).count()
        dislikes = Like.objects.filter(
            comment=comment, like_result=False).count()
        comments.append({
            'id': comment.id,
            'user_nickname': comment.user_nickname,
            'text_comment': comment.text_comment,
            'date': comment.date,
            'likes': likes,
            'dislikes': dislikes,
            'comment_repeat': comment.comment_repeat,
            'replay_comments': replay_comments
        })
    response = {
        'movie_data': movie_data,
        'score': score_average,
        'comments': comments,
        'quotes': quote_comments
    }
    return Response(response)


@api_view(['POST'])
def sign_up(request):
    """
    Create user in authorization api
    """
    serializer = CreateUserSerializer(
        data=request.data, context={'request', request})
    serializer.is_valid(raise_exception=True)
    response = authorization.sign_up_authorization_api(
        data=serializer.validated_data)
    return Response(response['response'], status=response['status'])


@api_view(['POST'])
def sign_in(request):
    """
    Login user in authorization api and return token
    """
    serializer = LoginUserSerializer(
        data=request.data, context={'request', request})
    serializer.is_valid(raise_exception=True)
    data = {
        'username': serializer.validated_data['email'],
        'password': serializer.validated_data['password']
    }
    response = authorization.sign_in_authorization_api(data)
    return Response(response['response'], status=response['status'])


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_score(request):
    serializer = ScoreSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    token = request.META['HTTP_TOKEN']
    user_data = authorization.validate_token_authorization_api(data={
                                                               'token': token})
    movie_response = get_movie_by_id(serializer.validated_data['movie_id'])
    if "Error" in movie_response:
        return Response(movie_response, status=status.HTTP_400_BAD_REQUEST)

    score_user_exists = Score.objects.filter(
        user_email=user_data['email'], movie_id=movie_response['id']).first()
    if score_user_exists:
        return Response({
            "score_created": False,
            "score_status": "User has already rated this movie"
        })
    score_obj = Score.objects.create(
        movie_id=movie_response['id'],
        movie_title=movie_response['Title'],
        score_value=serializer.validated_data['score_value'],
        user_email=user_data['email'],
        user_nickname=user_data['nickname']
    )
    add_points_response = authorization.add_points_user({
        'points': 1,
        'token': user_data['token']
    })
    return Response({
        'score_created': True,
        'add_points_status': add_points_response
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsUserBasicPermissions])
def create_comment(request):
    serializer = PostCommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    token = request.META['HTTP_TOKEN']
    user_data = authorization.validate_token_authorization_api(data={
                                                               'token': token})
    movie_response = get_movie_by_id(serializer.validated_data['movie_id'])

    if "Error" in movie_response:
        return Response(movie_response, status=status.HTTP_400_BAD_REQUEST)

    comment_obj = Comment.objects.create(
        user_email=user_data['email'],
        user_nickname=user_data['nickname'],
        text_comment=serializer.validated_data['text_comment'],
        movie_id=movie_response['id'],
        movie_title=movie_response['Title']
    )

    add_points_response = authorization.add_points_user({
        'points': 1,
        'token': user_data['token']
    })

    return Response({
        'comment_created': True,
        'add_points_status': add_points_response
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsUserBasicPermissions])
def create_replay_comment(request):
    serializer = PostReplayCommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    comment = Comment.objects.filter(
        id=serializer.validated_data['comment_id']).first()

    token = request.META['HTTP_TOKEN']
    user_data = authorization.validate_token_authorization_api(data={
                                                               'token': token})

    replay_comment_obj = ReplayComment.objects.create(
        comment=comment,
        text_replay_comment=serializer.validated_data['text_replay_comment'],
        user_email=user_data['email'],
        user_nickname=user_data['nickname']
    )

    add_points_response = authorization.add_points_user({
        'points': 1,
        'token': user_data['token']
    })

    return Response({
        'replay_comment_created': True,
        'add_points_status': add_points_response
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsUserAdvancedPermissions])
def create_like(request):
    serializer = PostLikeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    token = request.META['HTTP_TOKEN']
    user_data = authorization.validate_token_authorization_api(data={
                                                               'token': token})
    comment = Comment.objects.filter(
        id=serializer.validated_data['comment_id']).first()
    like_object = Like.objects.filter(
        comment=comment,
        user_email=user_data['email'],
        user_nickname=user_data['nickname']
    ).first()

    if not like_object:
        Like.objects.create(
            comment=comment,
            like_result=serializer.validated_data['like_result'],
            user_email=user_data['email'],
            user_nickname=user_data['nickname']
        )
    else:
        like_object.like_result = serializer.validated_data['like_result']
        like_object.save()

    return Response({
        'like_created': True,
        'like_result': serializer.validated_data['like_result']
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsUserAdvancedPermissions])
def create_quote_comment(request):
    serializer = PostQuoteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    token = request.META['HTTP_TOKEN']
    user_data = authorization.validate_token_authorization_api(data={
                                                               'token': token})

    comment = Comment.objects.get(id=serializer.validated_data['comment_id'])

    QuoteComment.objects.create(
        comment=comment,
        text_quote_comment=serializer.validated_data['text_quote_comment'],
        movie_id=serializer.validated_data['movie_id'],
        movie_title=serializer.movie_title,
        user_email=user_data['email'],
        user_nickname=user_data['nickname']
    )

    return Response({
        'quote_created': True
    }, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsUserModeratorPermissions])
def delete_comment(request):
    serializer = DeleteCommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    Comment.objects.get(id=serializer.validated_data['comment_id']).delete()
    return Response({
        'comment_delete_status': True
    })


@api_view(['PUT'])
@permission_classes([IsUserModeratorPermissions])
def mark_comment_repeat(request):
    serializer = MarkCommentRepeatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    comment = Comment.objects.get(id=serializer.validated_data['comment_id'])
    comment.comment_repeat = True
    comment.save()
    return Response({
        'status_mark_comment_repeat': True
    })


@api_view(['POST'])
@permission_classes([IsUserModeratorPermissions])
def make_moderator(request):
    serializer = MakeModeratorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response_obj = authorization.make_moderator(request.data)
    return Response(response_obj['response'], status=response_obj['status'])
