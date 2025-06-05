# sales_dashboard/views.py
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render, redirect
from django.contrib import messages
from file_uploader.models import UploadedFile
from file_uploader.views import get_file_path

def sales_upload(request):
    """Redireciona para upload específico de vendas"""
    from file_uploader.views import upload_file
    
    return upload_file(
        request, 
        file_type='sales',
        redirect_url='sales_dashboard:analyze'
    )

def analyze_sales(request, file_id):
    """Analisa dados de vendas de um arquivo específico"""
    file_path = get_file_path(file_id)
    
    if not file_path:
        messages.error(request, 'Arquivo não encontrado.')
        return redirect('sales_dashboard:upload')
    
    try:
        # Verificar se é arquivo de vendas
        uploaded_file = UploadedFile.objects.get(id=file_id)
        if uploaded_file.file_type != 'sales':
            messages.error(request, 'Este arquivo não é de dados de vendas.')
            return redirect('sales_dashboard:upload')
        
        # Ler e analisar os dados
        df = pd.read_csv(file_path)
        
        # Validar colunas necessárias
        required_columns = ['data', 'produto', 'quantidade', 'valor_venda', 'regiao']
        if not all(col in df.columns for col in required_columns):
            messages.error(request, 'Formato de arquivo inválido. Verifique as colunas necessárias.')
            return redirect('sales_dashboard:upload')
        
        # Análise básica
        total_sales = df['valor_venda'].sum()
        avg_sale = df['valor_venda'].mean()
        sales_by_product = df.groupby('produto')['valor_venda'].sum().sort_values(ascending=False)
        sales_by_region = df.groupby('regiao')['valor_venda'].sum()
        
        # Criar gráficos
        plt.switch_backend('Agg')
        
        # Gráfico 1: Vendas por produto
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sales_by_product.plot(kind='bar', ax=ax1, color='skyblue')
        ax1.set_title('Vendas por Produto')
        ax1.set_ylabel('Valor Total (R$)')
        ax1.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        buf1 = BytesIO()
        plt.savefig(buf1, format='png')
        plt.close(fig1)
        image1 = base64.b64encode(buf1.getvalue()).decode('utf-8')
        
        # Gráfico 2: Vendas por região
        fig2, ax2 = plt.subplots(figsize=(8, 8))
        sales_by_region.plot(kind='pie', autopct='%1.1f%%', ax=ax2, startangle=90)
        ax2.set_title('Distribuição de Vendas por Região')
        ax2.set_ylabel('')
        buf2 = BytesIO()
        plt.savefig(buf2, format='png')
        plt.close(fig2)
        image2 = base64.b64encode(buf2.getvalue()).decode('utf-8')
        
        # Marcar arquivo como processado
        uploaded_file.processed = True
        uploaded_file.save()
        
        context = {
            'total_sales': f"R$ {total_sales:,.2f}",
            'avg_sale': f"R$ {avg_sale:,.2f}",
            'top_products': sales_by_product.head(5).to_dict(),
            'chart1': image1,
            'chart2': image2,
            'file_name': uploaded_file.original_name,
            'upload_date': uploaded_file.uploaded_at,
        }
        
        return render(request, 'sales_dashboard/results.html', context)
        
    except Exception as e:
        messages.error(request, f'Erro ao processar arquivo: {str(e)}')
        return redirect('sales_dashboard:upload')

def sales_dashboard_home(request):
    """Página principal do sales_dashboard de vendas"""
    recent_files = UploadedFile.objects.filter(
        file_type='sales'
    ).order_by('-uploaded_at')[:5]
    
    return render(request, 'sales_dashboard/home.html', {
        'recent_files': recent_files
    })

# Manter compatibilidade com código antigo
def upload_file(request):
    """Compatibilidade com versão anterior"""
    return sales_upload(request)

def analysis_results(request, file_path=None):
    """Compatibilidade com versão anterior"""
    if file_path:
        # Lógica antiga para file_path direto
        pass
    else:
        # Redirecionar para nova estrutura
        return redirect('sales_dashboard:home')