# file_uploader/forms.py
from django import forms
from .models import UploadedFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.csv,.xlsx,.xls'
            })
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Validar extensão
            valid_extensions = ['.csv', '.xlsx', '.xls']
            file_extension = file.name.lower().split('.')[-1]
            if f'.{file_extension}' not in valid_extensions:
                raise forms.ValidationError('Apenas arquivos CSV ou Excel são permitidos.')
            
            # Validar tamanho (5MB máximo)
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Arquivo muito grande. Máximo 5MB.')
        
        return file