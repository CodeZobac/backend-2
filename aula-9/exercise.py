# Django BlogPost model and pytest tests
from django.db import models
from django.utils import timezone
from datetime import datetime

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    def get_excerpt(self, length=100):
        """Return a short excerpt of the content"""
        if len(self.content) <= length:
            return self.content
        return self.content[:length] + "..."
    
    def is_recent(self):
        """Check if the post was published in the last 7 days"""
        from datetime import timedelta
        recent_date = timezone.now() - timedelta(days=7)
        return self.published_date >= recent_date
    
    class Meta:
        ordering = ['-published_date']
