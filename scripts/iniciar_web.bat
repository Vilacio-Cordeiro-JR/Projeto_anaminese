@echo off
REM Script de inicialização do sistema web
REM Medidas Fit - Sistema de Análise Corporal

echo ========================================
echo   MEDIDAS FIT - Sistema Web
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado!
    echo Instale Python 3.8+ de https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

REM Verificar/instalar dependências
echo Verificando dependencias...
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo [INSTALANDO] Flask e Flask-CORS...
    pip install flask flask-cors
    echo.
) else (
    echo [OK] Dependencias instaladas
    echo.
)

REM Navegar para o diretório web
cd web

REM Iniciar servidor
echo ========================================
echo   Iniciando servidor...
echo ========================================
echo.
echo Aguarde... o navegador abrira automaticamente
echo.
echo Acesse: http://localhost:5000
echo.
echo Pressione Ctrl+C para encerrar
echo ========================================
echo.

python app.py

pause
