from django.shortcuts import render
from operator import attrgetter
from content.models import ContentPost
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from content.views import get_content_queryset

CONTENT_POST_PER_PAGE = 10

# Create your views here.

def home_screen_view(request, *args, **kwargs):
    context = {}

    # Search
    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    content_posts = sorted(get_content_queryset(query), key=attrgetter('date_updated'), reverse=True)


    page = request.GET.get('page', 1)
    content_posts_paginator = Paginator(content_posts, CONTENT_POST_PER_PAGE)
    try:
        content_posts = content_posts_paginator.page(page)
    except PageNotAnInteger:
        content_posts = content_posts_paginator.page(BLOG_POSTS_PER_PAGE)
    except EmptyPage:
        content_posts = content_posts_paginator.page(blog_posts_paginator.num_pages)

    context['content_posts'] = content_posts

    return render(request, "projects/home.html", context)

