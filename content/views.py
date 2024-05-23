from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from content.models import ContentPost
from content.forms import CreateContentPostForm, UpdateContentPostForm
from account.models import Account

def create_content_view(request):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreateContentPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateContentPostForm()

    context['form'] = form

    return render(request, "content/create_content.html", context)

def detail_content_view(request, slug):

    context ={}

    content_post = get_object_or_404(ContentPost, slug=slug)
    context['content_post'] = content_post

    return render(request, 'content/detail_content.html', context)


def edit_content_view(request, slug):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    content_post = get_object_or_404(ContentPost, slug=slug)
    if request.POST:
        form = UpdateContentPostForm(request.POST or None, request.FILES or None, instance=content_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated Successfully"
            content_post = obj

    form = UpdateContentPostForm(
        initial = {
            "title": content_post.title,
            "body": content_post.body,
            "image": content_post.image,
        }
    )
    context['form'] = form
    return render(request, 'content/edit_content.html', context)

def get_content_queryset(query=None, slug=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = ContentPost.objects.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)
    return list(set(queryset))
