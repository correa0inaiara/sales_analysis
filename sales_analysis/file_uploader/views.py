# file_uploader/views.py
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import UploadedFile
from .forms import FileUploadForm

def upload_file(request, file_type, redirect_url=None):
    """
    View genérica para upload de arquivos
    file_type: tipo do arquivo (sales, inventory, etc.)
    redirect_url: para onde redirecionar após upload
    """
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.file_type = file_type
            uploaded_file.original_name = request.FILES['file'].name
            if request.user.is_authenticated:
                uploaded_file.uploaded_by = request.user
            uploaded_file.save()
            
            messages.success(request, 'Arquivo enviado com sucesso!')
            
            # Redirecionar para a app específica
            if redirect_url:
                return redirect(redirect_url, file_id=uploaded_file.id)
            
            return redirect('file_uploader:success', file_id=uploaded_file.id)
    else:
        form = FileUploadForm()
    
    context = {
        'form': form,
        'file_type': file_type,
        'file_type_display': dict(UploadedFile.FILE_TYPES).get(file_type, file_type)
    }
    return render(request, 'file_uploader/upload.html', context)

def upload_success(request, file_id):
    """Página de sucesso após upload"""
    try:
        uploaded_file = UploadedFile.objects.get(id=file_id)
        return render(request, 'file_uploader/success.html', {'file': uploaded_file})
    except UploadedFile.DoesNotExist:
        messages.error(request, 'Arquivo não encontrado.')
        return redirect('file_uploader:upload')

def get_file_path(file_id):
    """Função utilitária para outras apps obterem o caminho do arquivo"""
    try:
        uploaded_file = UploadedFile.objects.get(id=file_id)
        return os.path.join(settings.MEDIA_ROOT, uploaded_file.file.name)
    except UploadedFile.DoesNotExist:
        return None