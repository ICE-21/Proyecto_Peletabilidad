@echo off

echo ==================================
echo   Iniciando PelletAI
echo ==================================

call .venv\Scripts\activate

streamlit run app.py

pause