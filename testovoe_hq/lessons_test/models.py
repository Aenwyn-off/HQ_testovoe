from django.db import models
from django.contrib.auth.models import User


# Модель для продукта
class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Модель для доступа к продукту для пользователя
class ProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} Access"


# Модель для урока
class Lesson(models.Model):
    products = models.ManyToManyField(Product, related_name='lessons')
    name = models.CharField(max_length=255)
    video_link = models.URLField()
    duration_seconds = models.PositiveIntegerField()

    def __str__(self):
        return self.name


# Модель для фиксации просмотра урока пользователями
class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)  # Статус "Просмотрено" или "Не просмотрено"
    viewed_time_seconds = models.PositiveIntegerField(default=0)  # Время просмотра в секундах

    def set_viewed_status(self):
        if self.viewed_time_seconds >= (self.lesson.duration_seconds * 0.8):
            self.viewed = True
        else:
            self.viewed = False

    def save(self, *args, **kwargs):
        self.set_viewed_status()
        super().save(*args, **kwargs)

    def __str__(self):
        status = "Просмотрено" if self.viewed else "Не просмотрено"
        return f"{self.user.username} - {self.lesson.name} - {status}"