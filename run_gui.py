#!/usr/bin/env python3
"""
Запуск графического интерфейса генератора календаря
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from gui_app import main as gui_main
    print("Запуск графического интерфейса...")
    print("=" * 50)
    gui_main()
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("\nУбедитесь, что:")
    print("1. Установлен Python 3.8+")
    print("2. Файл src/gui_app.py существует")
    print("3. Все зависимости установлены")
    input("\nНажмите Enter для выхода...")
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc()
    input("\nНажмите Enter для выхода...")