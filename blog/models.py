from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.db import models
from django.urls.base import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from MyBlog import settings


class Blog(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    subscribed = models.ManyToManyField(User, related_name='subscribed', null=True, blank=True)
    created = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Текст')
    readed_user = models.ManyToManyField(User, null=True, blank=True)
    posted = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=[str(self.id)])

    class Meta:
        ordering = ["-posted"]
        verbose_name_plural = 'Публикации'


@receiver(post_save, sender=Post)
def send_mail(sender, instance, **kwargs):
    post = instance
    users = Blog.objects.filter(subscribed__post=post)
    message = 'Новая публикация на сайте, перейти ' + str(settings.SITE_URL) + str(post.get_absolute_url())
    datatuple = (
        ('Новая публикация', message, 'from@mymail.com', users),
    )
    print(datatuple)
    send_mass_mail(datatuple, fail_silently=True)
