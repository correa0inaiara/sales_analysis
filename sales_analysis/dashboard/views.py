import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from django.conf import settings
from .models import SalesData

# Create your views here.

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        # Salvar o arquivo
        sales_data = SalesData(file=uploaded_file)
        sales_data.save()
        
        # Processar o arquivo
        file_path = os.path.join(settings.MEDIA_ROOT, sales_data.file.name)
        return analysis_results(request, file_path)
    
    return render(request, 'dashboard/upload.html')

def analysis_results(request, file_path=None):
    if not file_path and request.method == 'GET':
        latest_file = SalesData.objects.last()
        if latest_file:
            file_path = os.path.join(settings.MEDIA_ROOT, latest_file.file.name)
    
    if not file_path:
        return render(request, 'dashboard/upload.html')
    
    # Ler e analisar os dados
    df = pd.read_csv(file_path)
    
    # Análise básica
    total_sales = df['valor_venda'].sum()
    avg_sale = df['valor_venda'].mean()
    sales_by_product = df.groupby('produto')['valor_venda'].sum().sort_values(ascending=False)
    sales_by_region = df.groupby('regiao')['valor_venda'].sum()
    
    # Criar gráficos
    plt.switch_backend('Agg')  # Necessário para Django
    
    # Gráfico 1: Vendas por produto
    fig1, ax1 = plt.subplots()
    sales_by_product.plot(kind='bar', ax=ax1)
    ax1.set_title('Vendas por Produto')
    ax1.set_ylabel('Valor Total')
    buf1 = BytesIO()
    plt.savefig(buf1, format='png')
    plt.close(fig1)
    image1 = base64.b64encode(buf1.getvalue()).decode('utf-8')
    
    # Gráfico 2: Vendas por região
    fig2, ax2 = plt.subplots()
    sales_by_region.plot(kind='pie', autopct='%1.1f%%', ax=ax2)
    ax2.set_title('Distribuição de Vendas por Região')
    buf2 = BytesIO()
    plt.savefig(buf2, format='png')
    plt.close(fig2)
    image2 = base64.b64encode(buf2.getvalue()).decode('utf-8')
    
    context = {
        'total_sales': f"R$ {total_sales:,.2f}",
        'avg_sale': f"R$ {avg_sale:,.2f}",
        'top_products': sales_by_product.head(5).to_dict(),
        'chart1': image1,
        'chart2': image2,
        'file_name': os.path.basename(file_path),
    }
    
    return render(request, 'dashboard/results.html', context)