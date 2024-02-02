from django.db import models


class File(models.Model):
    class Meta:
        verbose_name = 'файл'
        verbose_name_plural = 'файлы'

    class FileTypeChoices(models.TextChoices):
        TXT = ('TXT', 'текст')
        IMG = ('IMG', 'изображение')
        PDF = ('PDF', 'PDF')
        NA = ('NA', 'неизвестен')

    VALID_FILES_EXTENSIONS = {
            FileTypeChoices.TXT: [
                'txt'
            ],
            FileTypeChoices.IMG: [
                'jpg',
                'jpeg',
                'png'       
            ],
            FileTypeChoices.PDF: [
                'pdf'
            ]
        }

    file = models.FileField(verbose_name='файл')
    type = models.CharField(
        max_length=10,
        choices=FileTypeChoices.choices,
        verbose_name='тип',
        default=FileTypeChoices.NA
    )
    uploaded_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='загружен')
    processed = models.BooleanField(verbose_name='обработан',
                                    default=False)