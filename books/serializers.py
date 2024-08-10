from rest_framework import serializers
from .models import Book, Recommendation, Like

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'cover_image_url', 'google_books_id']

class RecommendationSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book', write_only=True)
    user = serializers.StringRelatedField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Recommendation
        fields = ['id', 'user', 'book', 'book_id', 'comment', 'created_at', 'likes_count']

    def get_likes_count(self, obj):
        return obj.like_set.count()

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'recommendation', 'created_at']