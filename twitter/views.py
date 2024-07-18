from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView

from twitter.forms import PostModelForm
from twitter.models import Post


class FeedView(ListView, FormView):
    model = Post
    template_name = 'feed.html'
    context_object_name = 'posts'
    form_class = PostModelForm
    success_url = reverse_lazy('feed')

    def get_queryset(self):
        posts = super().get_queryset().order_by('-created_at')
        search = self.request.GET.get('search')
        if search:
            posts = posts.filter(author__icontains=search)
        return posts

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        for post in context['posts']:
            post.liked = post.likes.filter(id=self.request.user.id).exists()
        return context

class NewPostCreateView(CreateView):
    model = Post
    form_class = PostModelForm
    template_name = 'new_post.html'
    success_url = '/feed/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def like_post(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    if request.user.is_authenticated:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})
    return JsonResponse({'error': 'You must be logged in to like posts.'}, status=403)
