import tkinter as tk
import sys
import os

def force_gui_visible():
    root = tk.Tk()
    
    # Настройки окна
    root.title("NEFU Calendar Generator")
    root.geometry("800x600")
    
    # Принудительное отображение
    root.attributes('-alpha', 0.0)  # Сначала невидимое
    root.deiconify()  # Показываем
    root.update()     # Обновляем
    
    # Делаем видимым
    root.attributes('-alpha', 1.0)
    
    # Проверяем видимость
    print(f"Window visible: {root.winfo_viewable()}")
    
    # Создаем простой интерфейс
    from tkinter import ttk, Label
    
    label = Label(root, text="NEFU Calendar Generator\n\n"
                            "Если вы видите это окно,\n"
                            "GUI работает правильно!",
                 font=("Arial", 16))
    label.pack(pady=50)
    
    # Импортируем основное приложение
    try:
        # Добавляем путь к src
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(current_dir, 'src')
        
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
        
        from gui_app import CalendarGeneratorApp
        app = CalendarGeneratorApp(root)
        print("Main app loaded")
        
    except ImportError as e:
        print(f"Import error: {e}")
        # Показываем сообщение об ошибке в GUI
        error_label = Label(root, text=f"Ошибка импорта:\n{e}", 
                           fg="red", font=("Arial", 10))
        error_label.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    force_gui_visible()