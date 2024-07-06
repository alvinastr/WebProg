from django.urls import path
from content.views import (
    create_content_view,
    detail_content_view,
    edit_content_view,

)

app_name = 'content'

urlpatterns = [
    path('create/', create_content_view, name='create'),
    path('<slug>/', detail_content_view, name='detail'),
    path('<slug>/edit/', edit_content_view, name='edit'),
]
