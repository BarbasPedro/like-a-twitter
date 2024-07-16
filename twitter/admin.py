from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from twitter.models import Post, User


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        group, created = Group.objects.get_or_create(name='User')
        instance.groups.add(group)

class PostAdmin(admin.ModelAdmin):
    list_display=('author', 'content')
    search_fields=('author__username',)

admin.site.register(Post, PostAdmin)
admin.site.register(User)
