# inventory_dashboard/views.py
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render, redirect
from django.contrib import messages
from file_uploader.models import UploadedFile
from file_uploader.views import get_file_path

def inventory_upload(request):
    """Redireciona para upload específico de estoque"""
    from file_uploader.views import upload_file
    
    return upload_file(
        request, 
        file_type='inventory',
        redirect_url='inventory_dashboard:analyze'
    )

def analyze_inventory(request, file_id):
    """Analisa dados de estoque de um arquivo específico"""
    file_path = get_file_path(file_id)
    
    if not file_path:
        messages.error(request, 'Arquivo não encontrado.')
        return redirect('inventory_dashboard:upload')
    
    try:
        # Verificar se é arquivo de estoque
        uploaded_file = UploadedFile.objects.get(id=file_id)
        if uploaded_file.file_type != 'inventory':
            messages.error(request, 'Este arquivo não é de dados de estoque.')
            return redirect('inventory_dashboard:upload')
        
        # Ler e analisar os dados
        df = pd.read_csv(file_path)
        
        # Validar colunas necessárias para estoque
        required_columns = ['produto', 'quantidade_atual', 'quantidade_minima', 'preco_unitario']
        if not all(col in df.columns for col in required_columns):
            messages.error(request, 'Formato de arquivo inválido. Colunas necessárias: produto, quantidade_atual, quantidade_minima, preco_unitario')
            return redirect('inventory_dashboard:upload')
        
        # Análise de estoque
        total_items = len(df)
        total_value = (df['quantidade_atual'] * df['preco_unitario']).sum()
        low_stock = df[df['quantidade_atual'] <= df['quantidade_minima']]
        out_of_stock = df[df['quantidade_atual'] == 0]
        
        # Criar gráficos
        plt.switch_backend('Agg')
        
        # Gráfico 1: Status do estoque
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        status_counts = [
            len(df[df['quantidade_atual'] > df['quantidade_minima']]),  # Normal
            len(low_stock[low_stock['quantidade_atual'] > 0]),  # Baixo
            len(out_of_stock)  # Zerado
        ]
        colors = ['green', 'orange', 'red']
        labels = ['Estoque Normal', 'Estoque Baixo', 'Sem Estoque']
        
        ax1.bar(labels, status_counts, color=colors)
        ax1.set_title('Status do Estoque por Produto')
        ax1.set_ylabel('Quantidade de Produtos')
        buf1 = BytesIO()
        plt.savefig(buf1, format='png')
        plt.close(fig1)
        image1 = base64.b64encode(buf1.getvalue()).decode('utf-8')
        
        # Gráfico 2: Valor do estoque por produto
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        df['valor_estoque'] = df['quantidade_atual'] * df['preco_unitario']
        top_values = df.nlargest(10, 'valor_estoque')
        
        ax2.barh(top_values['produto'], top_values['valor_estoque'], color='lightblue')
        ax2.set_title('Top 10 - Valor em Estoque por Produto')
        ax2.set_xlabel('Valor (R$)')
        plt.tight_layout()
        buf2 = BytesIO()
        plt.savefig(buf2, format='png')
        plt.close(fig2)
        image2 = base64.b64encode(buf2.getvalue()).decode('utf-8')
        
        # Marcar arquivo como processado
        uploaded_file.processed = True
        uploaded_file.save()
        
        context = {
            'total_items': total_items,
            'total_value': f"R$ {total_value:,.2f}",
            'low_stock_count': len(low_stock),
            'out_of_stock_count': len(out_of_stock),
            'low_stock_items': low_stock[['produto', 'quantidade_atual', 'quantidade_minima']].to_dict('records'),
            'chart1': image1,
            'chart2': image2,
            'file_name': uploaded_file.original_name,
            'upload_date': uploaded_file.uploaded_at,
        }
        
        return render(request, 'inventory_dashboard/results.html', context)
        
    except Exception as e:
        messages.error(request, f'Erro ao processar arquivo: {str(e)}')
        return redirect('inventory_dashboard:upload')

def dashboard_home(request):
    """Página principal do dashboard de estoque"""
    recent_files = UploadedFile.objects.filter(
        file_type='inventory'
    ).order_by('-uploaded_at')[:5]
    
    return render(request, 'inventory_dashboard/home.html', {
        'recent_files': recent_files
    })