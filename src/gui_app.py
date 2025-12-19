"""
Docstring for university-calendar.src.gui_app
ver. 1.0
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext  
import datetime
from datetime import timedelta
import csv
import os


class AcademicCalendarGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NEFU calendar Generator")
        self.root.geometry("1000x700")
        self.root.resizable(True,True)

        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        self.setup_styles()
        self.calendar_data = []
        self.current_year = datetime.date.today().year

        self.create_widgets()

    def setup_styles(self):

        style = ttk.Style()
        
        available_themes = style.theme_names()
        print(f"Доступные темы: {available_themes}")

        if 'vista' in available_themes:
            style.theme_use('vista')
        elif 'winnative' in available_themes:
            style.theme_use('winnative')
        elif 'xpnative' in available_themes:
            style.theme_use('xpnative')
        else:
            style.theme_use('default')  

        self.bg_color = "#f0f0f0"
        self.fg_color = "#333333"
        self.accent_color = "#2c5aa0"
        self.highlight_color = "#e6f0ff"
        self.root.configure(bg=self.bg_color)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)

        title_label = ttk.Label(
            main_frame, 
            text="🎓 NEFU Academic Calendar Generator", 
            font=("Arial", 16, "bold"),
            foreground=self.accent_color
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky=tk.W)
    
        control_frame = ttk.LabelFrame(main_frame, text="Настройки", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(1, weight=1)

        ttk.Label(control_frame, text="Учебный год:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.year_var = tk.StringVar(value=str(self.current_year))
        year_spinbox = ttk.Spinbox(
            control_frame, 
            from_=2000, 
            to=2100, 
            textvariable=self.year_var,
            width=10
        )
        year_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))

        ttk.Label(control_frame, text="Недель:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        
        self.weeks_var = tk.StringVar(value="52")
        weeks_spinbox = ttk.Spinbox(
            control_frame, 
            from_=1, 
            to=100, 
            textvariable=self.weeks_var,
            width=5
        )
        weeks_spinbox.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        
        # Показывать примечания
        self.show_notes_var = tk.BooleanVar(value=True)
        notes_check = ttk.Checkbutton(
            control_frame, 
            text="Показывать примечания", 
            variable=self.show_notes_var
        )
        notes_check.grid(row=0, column=4, sticky=tk.W, padx=(0, 20))

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(0, 10), sticky=tk.W)

        generate_btn = ttk.Button(
            button_frame,
            text="📅 Сгенерировать календарь",
            command=self.generate_calendar,
            width=25
        )
        generate_btn.grid(row=0, column=0, padx=(0, 10))

        export_btn = ttk.Button(
            button_frame,
            text="💾 Экспорт в CSV",
            command=self.export_to_csv,
            width=20
        )
        export_btn.grid(row=0, column=1, padx=(0, 10))

        info_btn = ttk.Button(
            button_frame,
            text="ℹ️ Информация о годе",
            command=self.show_year_info,
            width=20
        )
        info_btn.grid(row=0, column=2, padx=(0, 10))
        
        clear_btn = ttk.Button(
            button_frame,
            text="🗑️ Очистить",
            command=self.clear_output,
            width=15
        )
        clear_btn.grid(row=0, column=3)

        info_frame = ttk.LabelFrame(main_frame, text="Информация о годе", padding="10")
        info_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.info_text = tk.StringVar(value="Выберите год и нажмите 'Сгенерировать'")
        info_label = ttk.Label(
            info_frame, 
            textvariable=self.info_text,
            wraplength=800
        )
        info_label.grid(row=0, column=0, sticky=tk.W)

        table_frame = ttk.LabelFrame(main_frame, text="Учебный календарь", padding="5")
        table_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        self.create_table(table_frame)

        self.status_var = tk.StringVar(value="Готов")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            padding=(5, 2)
        )
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def create_table(self, parent):

        """Table for calendar"""

        columns = ("week", "start", "end", "parity", "notes")
        
        self.tree = ttk.Treeview(
            parent, 
            columns=columns, 
            show="headings",
            height=20
        )

        self.tree.heading("week", text="Неделя")
        self.tree.heading("start", text="Начало недели")
        self.tree.heading("end", text="Конец недели")
        self.tree.heading("parity", text="Четность")
        self.tree.heading("notes", text="Примечания")
        
        self.tree.column("week", width=80, anchor=tk.CENTER)
        self.tree.column("start", width=120, anchor=tk.CENTER)
        self.tree.column("end", width=120, anchor=tk.CENTER)
        self.tree.column("parity", width=100, anchor=tk.CENTER)
        self.tree.column("notes", width=200, anchor=tk.W)

        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.tree.bind("<Double-Button-1>", self.on_item_double_click)

    def generate_academic_calendar(self, start_year, total_weeks=52):
        """Генерирует учебный календарь с правильной четностью"""
        weeks = []
        
        try:
            start_year = int(start_year)
            sept_1 = datetime.date(start_year, 9, 1)
            
            # Определяем начало первой учебной недели
            if sept_1.weekday() == 6:  # Воскресенье
                # Если 1 сентября - воскресенье, учебный год начинается 2 сентября
                first_monday = sept_1 + timedelta(days=1)
                current_date = first_monday
            else:
                # Находим понедельник недели, содержащей 1 сентября
                first_monday = sept_1 - timedelta(days=sept_1.weekday())
                current_date = first_monday
            
            # Важный момент: Определяем была ли предыдущая неделя нечетной
            # Для этого нужно знать четность последней недели предыдущего учебного года
            # По умолчанию: 1 сентября всегда начинается с нечетной недели
            # Но для точности нужно считать от какого-то известного года
            
            # Простой подход: 1-я неделя всегда нечетная (*)
            # Это стандартная практика в большинстве вузов
            
            # Генерируем недели
            for week_num in range(1, total_weeks + 1):
                start_week = current_date
                end_week = current_date + timedelta(days=6)
                
                # Определяем четность (1-я неделя всегда нечётная)
                # parity = "*" если нечетная, "**" если четная
                parity = "🔸 Нечётная" if week_num % 2 == 1 else "🔹 Чётная"
                
                # Проверяем текущая ли это неделя
                today = datetime.date.today()
                is_current = start_week <= today <= end_week
                
                # Формируем примечания
                notes = []
                if start_week <= sept_1 <= end_week:
                    if sept_1.weekday() == 6:  # Воскресенье
                        notes.append("Начало уч.года (со 2 сентября)")
                    else:
                        notes.append("Начало учебного года")
                if is_current:
                    notes.append("Текущая неделя")
                
                # Специальная проверка для 2024 года
                if start_year == 2024 and week_num == 1:
                    # Для 2024: 2-8 сентября - первая неделя
                    notes.append("Особый год: 1 сентября - воскресенье")
                
                weeks.append({
                    'week_num': week_num,
                    'start_date': start_week,
                    'end_date': end_week,
                    'parity': parity,
                    'notes': ", ".join(notes) if notes else "",
                    'is_current': is_current,
                    'year_type': 'normal' if sept_1.weekday() != 6 else 'special_sunday'
                })
                
                current_date += timedelta(days=7)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка генерации календаря:\n{str(e)}")
            
        return weeks
    
    def generate_calendar(self):
        """Обработчик кнопки генерации"""
        try:
            year = int(self.year_var.get())
            weeks_count = int(self.weeks_var.get())
            
            self.status_var.set("Генерация календаря...")
            self.root.update()

            self.calendar_data = self.generate_academic_calendar(year, weeks_count)

            self.update_year_info(year)

            for item in self.tree.get_children():
                self.tree.delete(item)

            for week in self.calendar_data:
                tags = ('current',) if week['is_current'] else ()
                
                self.tree.insert("", tk.END,
                    values=(
                        week['week_num'],
                        week['start_date'].strftime("%d.%m.%Y"),
                        week['end_date'].strftime("%d.%m.%Y"),
                        week['parity'],
                        week['notes'] if self.show_notes_var.get() else ""
                    ),
                    tags=tags
                )
            self.tree.tag_configure('current', background=self.highlight_color)

            odd_weeks = sum(1 for w in self.calendar_data if "Нечётная" in w['parity'])
            even_weeks = len(self.calendar_data) - odd_weeks
            
            self.status_var.set(
                f"✓ Сгенерировано {len(self.calendar_data)} недель "
                f"({odd_weeks} нечётных, {even_weeks} чётных)"
            )
            
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения")
            self.status_var.set("Ошибка ввода данных")
            
    def update_year_info(self, year):
        """Обновляет информацию о выбранном годе"""
        analysis = self.analyze_year_structure(year)
        
        info = (f"📅 Учебный год: {year}-{year+1}\n"
               f"1 сентября: {analysis['sept_1_weekday_name']}\n"
               f"Первая неделя: {analysis['start_date'].strftime('%d.%m.%Y')} - "
               f"{(analysis['start_date'] + timedelta(days=6)).strftime('%d.%m.%Y')}\n"
               f"Четность 1-й недели: {analysis['first_week_parity']}")
        
        if analysis['week_type'] == 'special':
            info += f"\n⚠️ Особый год: 1 сентября - воскресенье"
        
        self.info_text.set(info)
        
    def check_special_years(self):
        """Проверяет какие годы являются особыми (1 сентября - воскресенье)"""
        special_years = []
        for year in range(2000, 2051):
            sept_1 = datetime.date(year, 9, 1)
            if sept_1.weekday() == 6:  # Воскресенье
                special_years.append(year)
        
        return special_years
    def show_year_info(self):
        """Показывает подробную информацию о годе"""
        try:
            year = int(self.year_var.get())
            analysis = self.analyze_year_structure(year)
            special_years = self.check_special_years()
            
            info_window = tk.Toplevel(self.root)
            info_window.title(f"Информация о {year}-{year+1} учебном годе")
            info_window.geometry("600x400")
            info_window.resizable(False, False)
            
            text = f"""УЧЕБНЫЙ ГОД: {year}-{year+1}

1 СЕНТЯБРЯ {year} ГОДА:
• Дата: {analysis['sept_1'].strftime('%d.%m.%Y')}
• День недели: {analysis['sept_1_weekday_name']}
• Тип года: {'ОСОБЫЙ (воскресенье)' if analysis['week_type'] == 'special' else 'Обычный'}

ПЕРВАЯ УЧЕБНАЯ НЕДЕЛЯ:
• Начинается: {analysis['start_date'].strftime('%d.%m.%Y')} (понедельник)
• Заканчивается: {(analysis['start_date'] + timedelta(days=6)).strftime('%d.%m.%Y')}
• Четность: {analysis['first_week_parity']}
• Содержит 1 сентября: {'Нет (воскресенье)' if analysis['week_type'] == 'special' else 'Да'}"""
            
            if analysis['week_type'] == 'special':
                text += f"\n• Особенность: Учебный год начинается со 2 сентября"
            
            # Добавляем информацию о соседних годах
            text += "\n\nСОСЕДНИЕ ГОДА ДЛЯ СРАВНЕНИЯ:\n"
            for y in [year-2, year-1, year, year+1, year+2]:
                s1 = datetime.date(y, 9, 1)
                weekdays = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
                marker = " ← текущий" if y == year else ""
                special_mark = " (воскресенье!)" if s1.weekday() == 6 else ""
                text += f"• {y}-{y+1}: 1 сентября - {weekdays[s1.weekday()]}{special_mark}{marker}\n"
            
            # Добавляем информацию об особых годах
            text += f"\nБЛИЖАЙШИЕ ОСОБЫЕ ГОДА (1 сентября - воскресенье):\n"
            for y in special_years:
                if year-5 <= y <= year+5:
                    marker = " ← текущий" if y == year else ""
                    text += f"• {y}-{y+1}{marker}\n"
            
            text_widget = scrolledtext.ScrolledText(info_window, wrap=tk.WORD, 
                                                   font=("Consolas", 10))
            text_widget.insert(tk.INSERT, text)
            text_widget.configure(state='disabled')
            text_widget.pack(expand=True, fill='both', padx=10, pady=10)
            
            # Кнопка закрытия
            tk.Button(info_window, text="Закрыть", 
                     command=info_window.destroy).pack(pady=(0, 10))
            
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректный год")
            
    def export_to_csv(self):
        if not self.calendar_data:
            messagebox.showwarning("Нет данных", "Сначала сгенерируйте календарь")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"academic_calendar_{self.year_var.get()}_{int(self.year_var.get())+1}.csv"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')

                writer.writerow(['Номер недели', 'Начало недели', 'Конец недели',
                               'Четность', 'Примечания', 'Текущая неделя'])

                for week in self.calendar_data:
                    writer.writerow([
                        week['week_num'],
                        week['start_date'].strftime("%d.%m.%Y"),
                        week['end_date'].strftime("%d.%m.%Y"),
                        "Нечётная" if "Нечётная" in week['parity'] else "Чётная",
                        week['notes'],
                        'Да' if week['is_current'] else 'Нет'
                    ])
            
            self.status_var.set(f"✓ Календарь экспортирован в: {os.path.basename(filename)}")
            messagebox.showinfo("Экспорт завершен", 
                              f"Календарь успешно экспортирован в файл:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Ошибка экспорта", f"Не удалось сохранить файл:\n{str(e)}")
            self.status_var.set("Ошибка экспорта")
            
    def clear_output(self):
        """Очистка результатов"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.calendar_data = []

        self.info_text.set("Выберите год и нажмите 'Сгенерировать'")
        self.status_var.set("Готов")
        
    def on_item_double_click(self, event):
        """Обработчик двойного клика по строке таблицы"""
        item = self.tree.selection()[0]
        values = self.tree.item(item, 'values')
        
        if values:
            messagebox.showinfo(
                "Информация о неделе",
                f"Неделя №{values[0]}\n"
                f"Период: {values[1]} - {values[2]}\n"
                f"Четность: {values[3]}\n"
                f"Примечания: {values[4] if values[4] else 'нет'}"
            )
    def analyze_year_structure(self, year):
        """Анализирует структуру учебного года и возвращает детали"""
        sept_1 = datetime.date(year, 9, 1)
        weekdays = ["понедельник", "вторник", "среда", "четверг", 
                   "пятница", "суббота", "воскресенье"]
        
        if sept_1.weekday() == 6:  # Воскресенье
            first_monday = sept_1 + timedelta(days=1)
            start_date = first_monday
            week_type = "special"  # Особый год
            description = "1 сентября - воскресенье, учебный год начинается 2 сентября"
        else:
            first_monday = sept_1 - timedelta(days=sept_1.weekday())
            start_date = first_monday
            week_type = "normal"  # Обычный год
            description = f"1 сентября - {weekdays[sept_1.weekday()]}"
        
        return {
            'year': year,
            'sept_1': sept_1,
            'sept_1_weekday': sept_1.weekday(),
            'sept_1_weekday_name': weekdays[sept_1.weekday()],
            'first_monday': first_monday,
            'start_date': start_date,
            'week_type': week_type,
            'description': description,
            'first_week_parity': "* (нечётная)"  # Первая неделя всегда нечётная
        }

def main():
    """Запуск GUI приложения"""
    root = tk.Tk()
    app = AcademicCalendarGUI(root) 

    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()