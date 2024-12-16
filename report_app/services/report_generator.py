import pandas as pd
from django.db.models import Count, Q

from ..models import Application, Report


def save_report(report):
    Report.objects.create(data=report)


def generate_report(data):
    aggregated_data = Application.objects.aggregate(
        total_uploaded=Count('application_number'),
        total_duplicates=Count('application_number', filter=Q(
            application_state__icontains='Дубли')),
        total_new=Count('application_number', filter=Q(
            application_status__iexact='На создание')),
        total_extensions=Count('application_number', filter=Q(
            application_status__iexact='На расширение')),
        total_completed=Count('application_number', filter=Q(
            application_status__iexact='Обработка завершена')),
        total_returned=Count('application_number', filter=Q(
            application_status__iexact='Возвращена на уточнение')),
        total_sent_to_process=Count('application_number', filter=Q(
            application_status__icontains='Отправлена в обработку')),
        total_packages=Count('package_id', distinct=True),
        application_author=Count('application_author', distinct=True)
    )

    report = {
        'report': {
            'columns': ['Название', 'За указанный период', 'За все время'],
            'rows': [
                {
                    'title': 'Загруженных заявок',
                    'period': f"+{len(data)}",
                    'all_time': aggregated_data['total_uploaded']
                },
                {
                    'title': 'Дубли',
                    'period': f"+{data['Состояние заявки'].str.contains('Дубли').sum()}",
                    'all_time': aggregated_data['total_duplicates']
                },
                {
                    'title': 'На создание',
                    'period': f"+{data['Статус заявки'].eq('На создание').sum()}",
                    'all_time': aggregated_data['total_new']
                },
                {
                    'title': 'На расширение',
                    'period': f"+{data['Статус заявки'].eq('На расширение').sum()}",
                    'all_time': aggregated_data['total_extensions']
                },
                {
                    'title': 'Обработка завершена',
                    'period': f"+{data['Статус заявки'].eq('Обработка завершена').sum()}",
                    'all_time': aggregated_data['total_completed']
                },
                {
                    'title': 'Возвращена на уточнение',
                    'period': f"+{data['Статус заявки'].eq('Возвращена на уточнение').sum()}",
                    'all_time': aggregated_data['total_returned']
                },
                {
                    'title': 'Отправлена в обработку',
                    'period': f"+{data['Статус заявки'].str.contains('Отправлена в обработку').sum()}",
                    'all_time': aggregated_data['total_sent_to_process']
                },
                {
                    'title': 'Пакетов',
                    'period': f"+{data['ID пакета'].nunique()}",
                    'all_time': aggregated_data['total_packages']
                },
                {
                    'title': 'Пользователей',
                    'period': f"+{data['Автор заявки'].nunique()}",
                    'all_time': aggregated_data['application_author']
                }
            ]
        }
    }
    save_report(report)
    return report

def save_excel_to_db(file_path):
    data = pd.read_excel(file_path)
    # Так как в excel файле дата записана не в формате ISO 8601,
    # то сначала даты приводятся к этому стандарту, а затем конвертируются в
    # строковый тип данных, что бы их можно было использовать для создания моделей ORM
    data['Дата создания заявки'] = pd.to_datetime(
        data['Дата создания заявки'], format='%d.%m.%Y %H:%M:%S').dt.strftime('%Y-%m-%dT%H:%M:%S')
    data['Дата окончания обработки'] = pd.to_datetime(data['Дата окончания обработки'], format='%d.%m.%Y %H:%M:%S').dt.strftime(
        '%Y-%m-%dT%H:%M:%S').where(data['Дата окончания обработки'].notna(), None)

    def process_time(value):
        if value.strip().lower() == 'обработка не завершена':
            return None, False
        return value, True
    processing_data = data[
        'Время от создания заявки до конца обработки (в часах)'
    ].apply(process_time)

    data['Время от создания заявки до конца обработки (в часах)'] = processing_data.map(
        lambda x: x[0])
    data['Обработка завершена'] = processing_data.map(lambda x: x[1])

    for _, row in data.iterrows():
        Application.objects.update_or_create(
            application_number=row['Номер заявки'],
            defaults={
                'application_state': row['Состояние заявки'],
                'agreement': row.get('Согласование', None),
                'application_status': row['Статус заявки'],
                'application_author': row['Автор заявки'],
                'file_name': row['Имя файла'],
                'creation_date': row['Дата создания заявки'],
                'completion_date': row.get('Дата окончания обработки', None),
                'processing_time_hours': row.get('Время от создания заявки до конца обработки (в часах)', None),
                'processing_completed': row.get('Обработка завершена', False),
                'original_full_name': row.get('Полное наименование изначальное', None),
                'processed_full_name': row.get('Полное наименование после обработки', None),
                'material_code': row.get('Код материала', None),
                'similar_materials': row.get('Похожие материалы полученные из КП', None),
                'bei': row.get('БЕИ', None),
                'ntd': row.get('НТД', None),
                'package_id': row['ID пакета'],
            }
        )

    return data
