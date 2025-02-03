@echo off
echo Criando ambiente virtual...
python -m venv venv

echo Ativando ambiente virtual...
call .\venv\Scripts\activate

echo Instalando dependências...
python.exe -m pip install --upgrade pip
python.exe -m pip install -r requirements.txt

echo Configuração concluída! Use 'venv\Scripts\activate' para ativar o ambiente.
