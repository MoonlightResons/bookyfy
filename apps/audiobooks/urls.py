from django.urls import path
from .views import add_audiobook, stream_audio, audiobook_detail, comment_detail, add_like

urlpatterns = [
    path('create/audiobook/', add_audiobook, name='create-audiobook'),
    path('<int:audiobook_id>/stream/', stream_audio, name='audiobook-stream'),
    path('<int:audiobook_id>/detail/', audiobook_detail, name='audiobook-detail'),
    path('<int:audiobook_id>/like/', add_like, name='audiobook-like'),
    path('<int:audiobook_id>/<int:comment_id>/comment/', comment_detail, name='audio-comment-detail'),
]
