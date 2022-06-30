from django.contrib import admin
from .models import QuoteComment, Score, Comment, ReplayComment, Like
# Register your models here.

admin.site.register(Score)
admin.site.register(Comment)
admin.site.register(ReplayComment)
admin.site.register(Like)
admin.site.register(QuoteComment)
