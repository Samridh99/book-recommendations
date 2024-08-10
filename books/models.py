from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    cover_image_url = models.URLField()
    google_books_id = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.title

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s recommendation for {self.book.title}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'recommendation')

    def __str__(self):
        return f"{self.user.username} likes {self.recommendation}"