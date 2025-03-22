from django.shortcuts import render

import os
import tempfile
from django.shortcuts import render
from django.http import HttpResponse, FileResponse, HttpResponseBadRequest
import yt_dlp

def download_video(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        if not video_url:
            return HttpResponseBadRequest("Не указан URL видео.")

        # Создаем временную директорию для загрузки
        temp_dir = tempfile.mkdtemp()
        output_template = os.path.join(temp_dir, '%(title)s.%(ext)s')
        ydl_opts = {
            'outtmpl': output_template,
            'format': 'best',
            # Можно добавить дополнительные настройки по необходимости
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                video_title = info.get('title', 'video')
                video_ext = info.get('ext', 'mp4')
                file_name = f"{video_title}.{video_ext}"
                file_path = os.path.join(temp_dir, file_name)
                if os.path.exists(file_path):
                    # Отправляем файл пользователю
                    response = FileResponse(open(file_path, 'rb'), content_type='video/mp4')
                    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                    return response
                else:
                    return HttpResponse("Ошибка: файл не найден.", status=500)
        except Exception as e:
            return HttpResponse("Произошла ошибка: " + str(e), status=500)
    return render(request, 'MainApp/download_form.html')
