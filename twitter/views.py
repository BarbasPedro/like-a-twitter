from django.shortcuts import render

from twitter.models import Post


def feed_view(request):
    search = request.GET.get('search')
    posts = Post.objects.all()

    if search:
        posts = Post.objects.filter(author__icontains=search)

    print(posts)
    return render(
        request,
        'feed.html',
        {'posts': posts}
    )
