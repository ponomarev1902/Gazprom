import logging
import os

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .services.report_generator import generate_report, save_excel_to_db

logger = logging.getLogger(__name__)


@csrf_exempt
def upload_file_view(request):
    logger.info(f'обрабатывается запрос {request}')
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        file_path = fs.save(file.name, file)
        file_full_path = fs.path(file_path)

        data = save_excel_to_db(file_full_path)
        os.remove(file_full_path)
        report = generate_report(data)

        return render(request, 'report_app/result.html', {'report': report})

    return render(request, 'report_app/upload.html')
