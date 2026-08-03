from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    featured = models.BooleanField(default=False, help_text='Show on home page')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class Industry(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']
        verbose_name_plural = 'industries'

    def __str__(self):
        return self.title


class JobOpening(models.Model):
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class ContactInquiry(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'contact inquiries'

    def __str__(self):
        return f'{self.name} <{self.email}>'
