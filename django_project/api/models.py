from django.db import models


class File(models.Model):
    class Meta:
        verbose_name = 'файл'
        verbose_name_plural = 'файлы'

    file = models.FileField(verbose_name='файл')
    uploaded_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='загружен')
    processed = models.BooleanField(verbose_name='обработан',
                                    default=False)