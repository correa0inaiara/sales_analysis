## Construindo a aplicação

# 1. Criar ambiente virtual (opcional mas recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 2. Instalar Django e outras dependências
pip install django pandas matplotlib openpyxl

# 3. Criar projeto Django
django-admin startproject sales_analysis
cd sales_analysis

# 4. Criar app principal
python manage.py startapp dashboard

## Rodando a aplicação

# 1. Aplicar migrações (criar banco de dados)
python manage.py makemigrations
python manage.py migrate

# 2. Criar superusuário (opcional - para acessar o admin)
python manage.py createsuperuser

# 3. Iniciar o servidor de desenvolvimento
python manage.py runserver