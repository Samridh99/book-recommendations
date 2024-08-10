from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, Recommendation

class BookRecommendationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            description='Test Description',
            cover_image_url='http://example.com/cover.jpg',
            google_books_id='testid123'
        )

    def test_search_books(self):
        response = self.client.get('/api/books/search/?q=python')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_recommendation(self):
        data = {
            'book_id': self.book.id,
            'comment': 'Great book!'
        }
        response = self.client.post('/api/recommendations/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_like_recommendation(self):
        recommendation = Recommendation.objects.create(user=self.user, book=self.book, comment='Nice read')
        response = self.client.post(f'/api/recommendations/{recommendation.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unlike_recommendation(self):
        recommendation = Recommendation.objects.create(user=self.user, book=self.book, comment='Nice read')
        self.client.post(f'/api/recommendations/{recommendation.id}/like/')
        response = self.client.post(f'/api/recommendations/{recommendation.id}/unlike/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)