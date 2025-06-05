# file_uploader/models.py
from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    FILE_TYPES = [
        ('sales', 'Dados de Vendas'),
        ('inventory', 'Dados de Estoque'),
        ('customers', 'Dados de Clientes'),
    ]
    
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    original_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    processed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.original_name} ({self.file_type}) - {self.uploaded_at}"