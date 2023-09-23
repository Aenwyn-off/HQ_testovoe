from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Product, Lesson, LessonView, ProductAccess
from django.db.models import Count, Sum, F
from django.db.models.functions import Now


# API для вывода списка всех уроков по всем продуктам, к которым пользователь имеет доступ
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_lessons_by_user(request):
    user = request.user
    products = ProductAccess.objects.filter(user=user).values_list('product_id', flat=True)
    lessons = Lesson.objects.filter(products__in=products)
    lesson_data = []

    for lesson in lessons:
        lesson_view = LessonView.objects.filter(user=user, lesson=lesson).first()
        viewed = lesson_view.viewed if lesson_view else False
        viewed_time_seconds = lesson_view.viewed_time_seconds if lesson_view else 0

        lesson_data.append({
            'lesson_name': lesson.name,
            'video_link': lesson.video_link,
            'viewed': viewed,
            'viewed_time_seconds': viewed_time_seconds,
        })

    return Response(lesson_data)


# API для вывода списка уроков по конкретному продукту, к которому пользователь имеет доступ
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_lessons_by_product(request, product_id):
    user = request.user
    product = get_object_or_404(ProductAccess, user=user, product_id=product_id).product
    lessons = Lesson.objects.filter(products=product)
    lesson_data = []

    for lesson in lessons:
        lesson_view = LessonView.objects.filter(user=user, lesson=lesson).first()
        viewed = lesson_view.viewed if lesson_view else False
        viewed_time_seconds = lesson_view.viewed_time_seconds if lesson_view else 0

        lesson_data.append({
            'lesson_name': lesson.name,
            'video_link': lesson.video_link,
            'viewed': viewed,
            'viewed_time_seconds': viewed_time_seconds,
            'last_viewed_at': lesson_view.updated_at if lesson_view else None,
        })

    return Response(lesson_data)


# API для отображения статистики по продуктам
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product_statistics(request):
    user = request.user

    product_statistics = Product.objects.annotate(
        total_viewed_lessons=Count('lessons__lessonview', filter=F('lessons__lessonview__viewed')),
        total_viewed_time=Sum('lessons__lessonview__viewed_time_seconds'),
        total_users=Count('productaccess'),
        purchase_percent=(Count('productaccess') / Count('productaccess__user')) * 100,
    )

    product_data = []

    for product in product_statistics:
        product_data.append({
            'product_name': product.name,
            'total_viewed_lessons': product.total_viewed_lessons,
            'total_viewed_time_seconds': product.total_viewed_time,
            'total_users': product.total_users,
            'purchase_percent': product.purchase_percent,
        })

    return Response(product_data)
