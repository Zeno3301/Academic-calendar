@echo off
chcp 65001 >nul
echo ========================================
echo  University Calendar Generator - GUI
echo ========================================
echo.

if not "%VIRTUAL_ENV%" == "" (
    echo [✓] Виртуальное окружение активировано
) else (
    if exist "venv\Scripts\activate.bat" (
        echo [ ] Активируем виртуальное окружение...
        call venv\Scripts\activate.bat
    ) else (
        echo [!] Виртуальное окружение не найдено
        echo     Создайте: python -m venv venv
        pause
        exit /b 1
    )
)

python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден!
    pause
    exit /b 1
)

echo.
echo Запуск графического интерфейса...
echo.

python run_gui.py

if errorlevel 1 (
    echo.
    echo [ОШИБКА] Не удалось запустить GUI
    pause
    exit /b 1
)

echo.
echo Программа завершена.
pause