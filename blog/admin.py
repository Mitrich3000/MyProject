from django.contrib import admin

from blog.models import Blog, Post


# Define the admin class
class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'content')

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(blog__owner__username=request.user)

    def save_model(self, request, obj, form, change):
        obj.blog = Blog.objects.get(owner=request.user)
        obj.save()


admin.site.register(Blog)
admin.site.register(Post, PostAdmin)
