import logging

from django.db import models

logger = logging.getLogger(__name__)


class Report(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID отчета')
    # Отчет будет сохраняться в json-формате
    data = models.JSONField(verbose_name='Данные отчета')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')

    def save(self, *args, **kwargs):
        if not self.id:
            logger.info('Создается новый отчет.')
        else:
            logger.info(f'Обновление отчета с ID: {self.id}.')
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'report'

    def __str__(self):
        return f'Report {self.id}'


class Application(models.Model):
    # Основная информация
    application_number = models.CharField(max_length=255,
                                          verbose_name='Номер заявки',
                                          primary_key=True)
    application_state = models.CharField(max_length=255,
                                         verbose_name='Состояние заявки')
    agreement = models.CharField(max_length=255,
                                 null=True,
                                 blank=True,
                                 verbose_name='Согласование')
    application_status = models.CharField(max_length=255,
                                          verbose_name='Статус заявки')
    application_author = models.CharField(max_length=255,
                                          verbose_name='Автор заявки')
    file_name = models.CharField(max_length=255, verbose_name='Имя файла')

    # Даты и время
    creation_date = models.DateTimeField(verbose_name='Дата создания заявки')
    completion_date = models.DateTimeField(
        null=True, blank=True, verbose_name='Дата окончания обработки')
    processing_time_hours = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Время от создания заявки до конца обработки (в часах)')
    processing_completed = models.BooleanField(
        default=False, verbose_name='Обработка завершена')

    # Материалы и согласование
    original_full_name = models.TextField(
        null=True, blank=True, verbose_name='Полное наименование изначальное')
    processed_full_name = models.TextField(
        null=True,
        blank=True,
        verbose_name='Полное наименование после обработки')
    material_code = models.CharField(max_length=255,
                                     null=True,
                                     blank=True,
                                     verbose_name='Код материала')
    similar_materials = models.TextField(
        null=True,
        blank=True,
        verbose_name='Похожие материалы полученные из КП')

    # Дополнительные поля
    bei = models.CharField(max_length=255,
                           null=True,
                           blank=True,
                           verbose_name='БЕИ')
    ntd = models.CharField(max_length=255,
                           null=True,
                           blank=True,
                           verbose_name='НТД')
    package_id = models.CharField(max_length=255, verbose_name='ID пакета')

    class Meta:
        db_table = 'application'

    def __str__(self):
        return (
            f'Номер заявки: {self.application_number}, '
            f'Состояние заявки: {self.application_state}, Согласование: {self.agreement}, '
            f'Статус заявки: {self.application_status}, Автор заявки: {self.application_author}, '
            f'Имя файла: {self.file_name}, Дата создания заявки: {self.creation_date}, '
            f'Дата окончания обработки: {self.completion_date}, Время обработки (часы): {self.processing_time_hours}, '
            f'Обработка завершена: {self.processing_completed}, '
            f'Полное наименование изначальное: {self.original_full_name}, Полное наименование после обработки: {self.processed_full_name}, '
            f'Код материала: {self.material_code}, Похожие материалы: {self.similar_materials}, '
            f'БЕИ: {self.bei}, НТД: {self.ntd}, ID пакета: {self.package_id}')
