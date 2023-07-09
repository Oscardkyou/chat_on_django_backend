from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, verbose_name="Отправитель",
        on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, verbose_name="Получатель",
        on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=500, verbose_name="Сообщение")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")

    def __str__(self) -> str:
        return f"{self.date} {self.sender} -> {self.receiver}: {self.message}"
    
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-date"]