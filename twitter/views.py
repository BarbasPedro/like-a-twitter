from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from twitter.forms import PostModelForm
from twitter.models import Post, User


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
        if self.request.user.is_authenticated:
            following_status = {
                post.id: self.request.user.following.filter(id=post.author.id).exists()
                for post in context['posts']
            }
            context['following_status'] = following_status
            following_list = self.request.user.following.exclude(username=self.request.user.username)
            context['following_list'] = following_list
            context['following_count'] = following_list.count()
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

@login_required
@csrf_exempt
def follow_user(request, user_id):
    if request.method == 'POST':
        user_to_follow = User.objects.get(id=user_id)
        if user_to_follow in request.user.following.all():
            request.user.following.remove(user_to_follow)
            user_to_follow.followers.remove(request.user)
            followed = False
        else:
            request.user.following.add(user_to_follow)
            user_to_follow.followers.add(request.user)
            followed = True

        total_following = request.user.following.count()
        total_followers = user_to_follow.followers.count()
        following_list_data = [{'username': user.username} for user in request.user.following.all()]

        return JsonResponse({
            'followed': followed,
            'total_following': total_following,
            'total_followers': total_followers,
            'following_list': following_list_data,
            'clicked_user_id': user_id,
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)
