from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, Recommendation, Like
from .serializers import BookSerializer, RecommendationSerializer, LikeSerializer
from .google_books_api import search_books, get_book_details
import logging

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = "books/index.html"

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        results = search_books(query)
        return Response(results)

    @action(detail=False, methods=['post'])
    def add_from_google_books(self, request):
        google_books_id = request.data.get('google_books_id')
        if not google_books_id:
            return Response({'error': 'google_books_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        book_data = get_book_details(google_books_id)
        volume_info = book_data.get('volumeInfo', {})
        
        book, created = Book.objects.get_or_create(
            google_books_id=google_books_id,
            defaults={
                'title': volume_info.get('title', ''),
                'author': ', '.join(volume_info.get('authors', [])),
                'description': volume_info.get('description', ''),
                'cover_image_url': volume_info.get('imageLinks', {}).get('thumbnail', ''),
            }
        )
        
        serializer = self.get_serializer(book)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

    def create(self, request, *args, **kwargs):
        logger.info(f"Received data: {request.data}")
        logger.info(f"User: {request.user}")
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        recommendation = self.get_object()
        user = request.user
        like, created = Like.objects.get_or_create(user=user, recommendation=recommendation)
        if created:
            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'already liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        recommendation = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(user=user, recommendation=recommendation)
            like.delete()
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'status': 'not liked'}, status=status.HTTP_400_BAD_REQUEST)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer