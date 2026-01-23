"""
Главный файл для запуска графического интерфейса
"""

import sys
import os
import traceback

def main():
    try:
        is_exe = hasattr(sys, 'frozen') or hasattr(sys, '_MEIPASS')
        if is_exe:
            base_path = sys._MEIPASS
            src_path = os.path.join(base_path, 'src')
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            src_path = os.path.join(base_path, 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)

        src_parent = os.path.dirname(src_path)
        if src_parent not in sys.path:
            sys.path.insert(0, src_parent)

        try:
            import src.gui_app
            from src.gui_app import AcademicCalendarGUI
            print("✓ Импорт через src.gui_app")
            
        except ImportError:
            try:
                import importlib.util
                module_path = os.path.join(src_path, 'gui_app.py')
                
                spec = importlib.util.spec_from_file_location(
                    "gui_app_module", 
                    module_path
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                AcademicCalendarGUI = module.AcademicCalendarGUI
                print("✓ Импорт через importlib")
                
            except Exception as e:
                print(f"✗ Все способы импорта не удались: {e}")
                print(f"Путь к файлу: {os.path.join(src_path, 'gui_app.py')}")
                print(f"Файл существует: {os.path.exists(os.path.join(src_path, 'gui_app.py'))}")
                print(f"\nsys.path:")
                for p in sys.path:
                    print(f"  {p}")
                
                if not is_exe:
                    input("Нажмите Enter...")
                return 1

        import tkinter as tk
        print("✓ tkinter импортирован")

        root = tk.Tk()
        app = AcademicCalendarGUI(root)
        root.mainloop()
        
        return 0
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        traceback.print_exc()
        if not is_exe:
            input("Нажмите Enter...")
        return 1

if __name__ == "__main__":
    sys.exit(main())