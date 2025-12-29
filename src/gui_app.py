"""
Графический интерфейс для генератора учебного календаря
Версия: 2.0 (с информацией о сегодняшнем дне)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import datetime
from datetime import timedelta
import csv
import os


class AcademicCalendarGUI:
    """Главное окно приложения"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("NEFU Academic Calendar Generator")
        self.root.geometry("1100x750")  # Немного увеличили окно
        self.root.resizable(True, True)
        
        # Иконка (если есть файл icon.ico в папке)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Стили
        self.setup_styles()
        
        # Данные
        self.calendar_data = []
        self.current_year = datetime.date.today().year
        
        # Создаем интерфейс
        self.create_widgets()
        
    def setup_styles(self):
        """Настройка стилей для виджетов - упрощенная для Windows"""
        # Простые цвета без сложных тем
        self.bg_color = "#f0f0f0"
        self.fg_color = "#333333"
        self.accent_color = "#1e3a8a"  # Темно-синий NEFU
        self.highlight_color = "#e6f0ff"
        
        self.root.configure(bg=self.bg_color)
        
    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        
        # Главный контейнер
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 1. ЗАГОЛОВОК с логотипом NEFU
        header_frame = tk.Frame(main_frame, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Логотип NEFU (символический)
        nefu_label = tk.Label(
            header_frame,
            text="NEFU",
            font=("Arial", 24, "bold"),
            fg="#1e3a8a",  # Темно-синий NEFU
            bg=self.bg_color
        )
        nefu_label.pack(side=tk.LEFT)
        
        title_label = tk.Label(
            header_frame,
            text="Академический календарь",
            font=("Arial", 18, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        title_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # 2. ПАНЕЛЬ УПРАВЛЕНИЯ
        control_frame = tk.LabelFrame(
            main_frame, 
            text="Параметры генерации",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.accent_color,
            padx=15,
            pady=15
        )
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Сетка для элементов управления
        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
        control_frame.columnconfigure(2, weight=1)
        control_frame.columnconfigure(3, weight=1)
        control_frame.columnconfigure(4, weight=1)
        
        # Год
        year_label = tk.Label(
            control_frame,
            text="Учебный год:",
            font=("Arial", 11),
            bg=self.bg_color
        )
        year_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.year_var = tk.StringVar(value=str(self.current_year))
        year_spinbox = tk.Spinbox(
            control_frame, 
            from_=2000, 
            to=2100, 
            textvariable=self.year_var,
            width=12,
            font=("Arial", 11),
            justify=tk.CENTER,
            bg="white",
            relief=tk.SUNKEN,
            borderwidth=2
        )
        year_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Количество недель
        weeks_label = tk.Label(
            control_frame,
            text="Количество недель:",
            font=("Arial", 11),
            bg=self.bg_color
        )
        weeks_label.grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        
        self.weeks_var = tk.StringVar(value="52")
        weeks_spinbox = tk.Spinbox(
            control_frame, 
            from_=1, 
            to=100, 
            textvariable=self.weeks_var,
            width=8,
            font=("Arial", 11),
            justify=tk.CENTER,
            bg="white",
            relief=tk.SUNKEN,
            borderwidth=2
        )
        weeks_spinbox.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        
        # Показывать примечания
        self.show_notes_var = tk.BooleanVar(value=True)
        notes_check = tk.Checkbutton(
            control_frame, 
            text="Показывать примечания",
            font=("Arial", 11),
            variable=self.show_notes_var,
            bg=self.bg_color,
            activebackground=self.bg_color
        )
        notes_check.grid(row=0, column=4, sticky=tk.W)
        
        # 3. БОЛЬШИЕ КНОПКИ ДЕЙСТВИЙ
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Кнопка генерации (ГЛАВНАЯ - самая большая)
        generate_btn = tk.Button(
            button_frame,
            text="СГЕНЕРИРОВАТЬ КАЛЕНДАРЬ",
            command=self.generate_calendar,
            width=30,
            height=2,
            bg="#1e3a8a",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            borderwidth=3,
            cursor="hand2",
            activebackground="#2563eb",
            activeforeground="white"
        )
        generate_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Кнопка информации о годе
        info_btn = tk.Button(
            button_frame,
            text="ИНФОРМАЦИЯ О ГОДЕ",
            command=self.show_year_info,
            width=22,
            height=2,
            bg="#0ea5e9",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            borderwidth=2,
            cursor="hand2",
            activebackground="#38bdf8",
            activeforeground="white"
        )
        info_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Фрейм для остальных кнопок
        other_buttons_frame = tk.Frame(button_frame, bg=self.bg_color)
        other_buttons_frame.pack(side=tk.LEFT)
        
        # Кнопка экспорта
        export_btn = tk.Button(
            other_buttons_frame,
            text="Экспорт в CSV",
            command=self.export_to_csv,
            width=18,
            bg="#10b981",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            borderwidth=2,
            cursor="hand2",
            activebackground="#34d399",
            activeforeground="white"
        )
        export_btn.pack(pady=(0, 5))
        
        # Кнопка очистки
        clear_btn = tk.Button(
            other_buttons_frame,
            text="Очистить таблицу",
            command=self.clear_output,
            width=18,
            bg="#ef4444",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            borderwidth=2,
            cursor="hand2",
            activebackground="#f87171",
            activeforeground="white"
        )
        clear_btn.pack()
        
        # 4. ИНФОРМАЦИОННАЯ ПАНЕЛЬ (две колонки)
        info_container = tk.Frame(main_frame, bg=self.bg_color)
        info_container.pack(fill=tk.X, pady=(0, 15))

        
        # ЛЕВАЯ колонка - информация о сегодняшнем дне (БОЛЬШОЙ ШРИФТ, ВЫДЕЛЕННАЯ)
        today_info_frame = tk.LabelFrame(
            info_container, 
            text="СЕГОДНЯ",
            font=("Arial", 12, "bold"),
            bg="#e6f0ff",
            fg="#1e3a8a",
            padx=15,
            pady=15,
            relief=tk.RAISED
        )
        today_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.today_info_text = tk.StringVar(value="Сгенерируйте\nкалендарь")
        today_label = tk.Label(
            today_info_frame, 
            textvariable=self.today_info_text,
            font=("Arial", 18, "bold"),
            bg="#e6f0ff",
            fg="#1e3a8a",
            justify=tk.CENTER,
            padx=20,
            pady=20
        )
        today_label.pack(fill=tk.BOTH, expand=True)
        
        # ПРАВАЯ колонка - информация о годе
        year_info_frame = tk.LabelFrame(
            info_container, 
            text="Информация о годе",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.accent_color,
            padx=15,
            pady=15
        )
        year_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        
        self.info_text = tk.StringVar(value="Выберите год и нажмите 'СГЕНЕРИРОВАТЬ КАЛЕНДАРЬ'")
        info_label = tk.Label(
            year_info_frame, 
            textvariable=self.info_text,
            wraplength=400,
            font=("Arial", 11),
            bg="#f8fafc",
            fg="#1e293b",
            justify=tk.LEFT,
            relief=tk.SUNKEN,
            borderwidth=1,
            padx=10,
            pady=10
        )
        info_label.pack(fill=tk.BOTH, expand=True)
        
        # 5. ТАБЛИЦА С РЕЗУЛЬТАТАМИ
        table_container = tk.Frame(main_frame, bg=self.bg_color)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        table_label = tk.Label(
            table_container,
            text="Сгенерированный календарь",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        table_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Создаем Treeview для таблицы внутри отдельного фрейма
        table_inner_frame = tk.Frame(table_container, bg=self.bg_color)
        table_inner_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_table(table_inner_frame)
        
        # 6. СТАТУС БАР внизу окна
        status_frame = tk.Frame(self.root, bg="#1e293b", height=25)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = tk.Label(
            status_frame,
            textvariable=self.status_var,
            bg="#1e293b",
            fg="white",
            font=("Arial", 10),
            anchor=tk.W,
            padx=10
        )
        status_bar.pack(fill=tk.X)
        
    def create_table(self, parent):
        """Создание красивой таблицы для отображения календаря"""
        
        # Создаем стиль для таблицы
        style = ttk.Style()
        style.configure("Treeview.Heading", 
                       font=("Arial", 11, "bold"),
                       background=self.accent_color,
                       foreground="white")
        style.configure("Treeview", 
                       font=("Arial", 10),
                       rowheight=25,
                       background="white",
                       fieldbackground="white")
        
        # Создаем Treeview с прокруткой
        columns = ("week", "start", "end", "parity", "notes")
        
        self.tree = ttk.Treeview(
            parent, 
            columns=columns, 
            show="headings",
            height=18,
            style="Treeview"
        )
        
        # Настраиваем колонки
        self.tree.heading("week", text="№ недели")
        self.tree.heading("start", text="Начало недели")
        self.tree.heading("end", text="Конец недели")
        self.tree.heading("parity", text="Четность")
        self.tree.heading("notes", text="Примечания")
        
        self.tree.column("week", width=80, anchor=tk.CENTER, minwidth=80)
        self.tree.column("start", width=120, anchor=tk.CENTER, minwidth=120)
        self.tree.column("end", width=120, anchor=tk.CENTER, minwidth=120)
        self.tree.column("parity", width=100, anchor=tk.CENTER, minwidth=100)
        self.tree.column("notes", width=250, anchor=tk.W, minwidth=200)
        
        # Добавляем прокрутку
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Настраиваем расширение таблицы
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        # Бинд событий
        self.tree.bind("<Double-Button-1>", self.on_item_double_click)
        
        # Добавляем подсказку
        hint_label = tk.Label(
            parent,
            text="Двойной клик по строке - подробная информация о неделе",
            font=("Arial", 9, "italic"),
            bg=self.bg_color,
            fg="#64748b"
        )
        hint_label.grid(row=1, column=0, columnspan=2, pady=(5, 0), sticky=tk.W)
        
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
    
    def generate_academic_calendar(self, start_year, total_weeks=52):
        """Генерирует учебный календарь с правильной четностью"""
        weeks = []
        
        try:
            start_year = int(start_year)
            sept_1 = datetime.date(start_year, 9, 1)
            
            # Определяем начало первой учебной недели
            if sept_1.weekday() == 6:  # Воскресенье
                first_monday = sept_1 + timedelta(days=1)
                current_date = first_monday
            else:
                first_monday = sept_1 - timedelta(days=sept_1.weekday())
                current_date = first_monday
            
            # Генерируем недели
            for week_num in range(1, total_weeks + 1):
                start_week = current_date
                end_week = current_date + timedelta(days=6)
                
                # Определяем четность (1-я неделя всегда нечётная)
                parity = "* Нечётная" if week_num % 2 == 1 else "** Чётная"
                
                # Проверяем текущая ли это неделя
                today = datetime.date.today()
                is_current = start_week <= today <= end_week
                
                # Проверяем содержит ли неделя 1 сентября
                contains_sept_1 = start_week <= sept_1 <= end_week
                
                # Формируем примечания
                notes = []
                if contains_sept_1:
                    if sept_1.weekday() == 6:
                        notes.append("Начало уч.года (со 2 сентября)")
                    else:
                        notes.append("Начало учебного года")
                if is_current:
                    notes.append("Текущая неделя")
                
                weeks.append({
                    'week_num': week_num,
                    'start_date': start_week,
                    'end_date': end_week,
                    'parity': parity,
                    'notes': ", ".join(notes) if notes else "",
                    'is_current': is_current,
                    'contains_sept_1': contains_sept_1  # ← ВОТ ЭТУ СТРОКУ ДОБАВЛЯЕМ!
                })
                
                current_date += timedelta(days=7)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка генерации календаря:\n{str(e)}")
            
        return weeks
    
    def generate_calendar(self):
        """Обработчик кнопки генерации"""
        try:
            # Получаем параметры
            year = int(self.year_var.get())
            weeks_count = int(self.weeks_var.get())
            
            # Обновляем статус
            self.status_var.set("Генерация календаря...")
            self.root.update()
            
            # Генерируем календарь
            self.calendar_data = self.generate_academic_calendar(year, weeks_count)
            
            # Обновляем информацию о годе
            self.update_year_info(year)
            
            # Обновляем информацию о сегодняшнем дне
            self.update_today_info()
            
            # Очищаем таблицу
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Заполняем таблицу
            for week in self.calendar_data:
                tags = ()
                # Выделяем текущую неделю другим цветом
                if week['is_current']:
                    tags = ('current', 'highlight')
                elif week['contains_sept_1']:
                    tags = ('first_week',)
                
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
            
            # Настраиваем теги для выделения
            self.tree.tag_configure('current', background='#ffeb3b')  # Желтый для текущей недели
            self.tree.tag_configure('highlight', font=('Arial', 10, 'bold'))  # Жирный шрифт
            self.tree.tag_configure('first_week', background='#e3f2fd')  # Голубой для недели с 1 сентября
            
            # Статистика
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
    
    def update_today_info(self):
        """Обновляет информацию о сегодняшнем дне"""
        today = datetime.date.today()
        today_str = today.strftime("%d.%m.%Y")
        
        # Находим текущую неделю в сгенерированном календаре
        current_week = None
        week_num = None
        parity = None
        
        if self.calendar_data:
            for week in self.calendar_data:
                if week['start_date'] <= today <= week['end_date']:
                    current_week = week
                    week_num = week['week_num']
                    parity = week['parity']
                    break
        
        if current_week:
            # Если сегодняшний день входит в текущий календарь
            today_info = f"Сегодня: {today_str}\nНеделя: {week_num}\n {parity}"
            self.today_info_text.set(today_info)
        else:
            # Если календарь не сгенерирован или сегодня вне диапазона
            if self.calendar_data:
                self.today_info_text.set(f"Сегодня: {today_str}\n(дата вне диапазона календаря)")
            else:
                self.today_info_text.set(f"Сегодня: {today_str}\n(сгенерируйте календарь)")
    
    def show_year_info(self):
        """Показывает подробную информацию о годе в красивом окне"""
        try:
            year = int(self.year_var.get())
            analysis = self.analyze_year_structure(year)
            
            info_window = tk.Toplevel(self.root)
            info_window.title(f"Информация о {year}-{year+1} учебном годе")
            info_window.geometry("650x450")
            info_window.resizable(False, False)
            info_window.configure(bg=self.bg_color)
            
            # Заголовок окна
            header_frame = tk.Frame(info_window, bg=self.accent_color)
            header_frame.pack(fill=tk.X, pady=(0, 15))
            
            title_label = tk.Label(
                header_frame,
                text=f"📚 УЧЕБНЫЙ ГОД {year}-{year+1}",
                font=("Arial", 14, "bold"),
                bg=self.accent_color,
                fg="white",
                pady=10
            )
            title_label.pack()
            
            # Основной контент
            content_frame = tk.Frame(info_window, bg=self.bg_color, padx=20, pady=10)
            content_frame.pack(fill=tk.BOTH, expand=True)
            
            # Создаем стилизованный текст
            text_info = f"""
┌─────────────────────────────────────────────┐
│  1 СЕНТЯБРЯ {year} ГОДА                      │
├─────────────────────────────────────────────┤
│  • Дата: {analysis['sept_1'].strftime('%d.%m.%Y')}             │
│  • День недели: {analysis['sept_1_weekday_name']:15} │
│  • Тип года: {'ОСОБЫЙ (воскресенье)' if analysis['week_type'] == 'special' else 'ОБЫЧНЫЙ':16} │
│                                              │
│  ПЕРВАЯ УЧЕБНАЯ НЕДЕЛЯ:                     │
│  • Начало: {analysis['start_date'].strftime('%d.%m.%Y')}                │
│  • Окончание: {(analysis['start_date'] + timedelta(days=6)).strftime('%d.%m.%Y')}          │
│  • Четность: {analysis['first_week_parity']:18} │
│  • Содержит 1 сентября: {'НЕТ (воскресенье)' if analysis['week_type'] == 'special' else 'ДА':12} │
└─────────────────────────────────────────────┘
"""
            
            if analysis['week_type'] == 'special':
                text_info += f"""
{'═'*60}
 ВНИМАНИЕ: 1 сентября - воскресенье!
 Учебный год начинается со 2 сентября {year} года.
 Первая учебная неделя: 2-8 сентября.
{'═'*60}
"""
            
            # Отображаем текст в красивом виджете
            text_widget = tk.Text(
                content_frame,
                wrap=tk.WORD,
                font=("Consolas", 11),
                bg="#f8fafc",
                fg="#1e293b",
                relief=tk.FLAT,
                borderwidth=0,
                height=15,
                padx=10,
                pady=10
            )
            text_widget.insert(tk.INSERT, text_info)
            text_widget.configure(state='disabled')
            text_widget.pack(fill=tk.BOTH, expand=True)
            
            # Добавляем рамку вокруг текста
            text_frame = tk.Frame(content_frame, bg="#cbd5e1", padx=1, pady=1)
            text_frame.place(in_=text_widget, x=0, y=0, relwidth=1, relheight=1)
            text_widget.lift()
            
            # Кнопка закрытия
            close_frame = tk.Frame(info_window, bg=self.bg_color)
            close_frame.pack(fill=tk.X, pady=(10, 20))
            
            close_btn = tk.Button(
                close_frame,
                text="Закрыть",
                command=info_window.destroy,
                width=15,
                bg="#64748b",
                fg="white",
                font=("Arial", 10, "bold"),
                relief=tk.RAISED,
                cursor="hand2"
            )
            close_btn.pack()
            
            # Центрируем окно
            info_window.update_idletasks()
            width = info_window.winfo_width()
            height = info_window.winfo_height()
            x = (info_window.winfo_screenwidth() // 2) - (width // 2)
            y = (info_window.winfo_screenheight() // 2) - (height // 2)
            info_window.geometry(f'{width}x{height}+{x}+{y}')
            
            # Поднимаем окно поверх других
            info_window.transient(self.root)
            info_window.grab_set()
            self.root.wait_window(info_window)
            
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректный год")
    
    def export_to_csv(self):
        """Экспорт календаря в CSV файл"""
        if not self.calendar_data:
            messagebox.showwarning("Нет данных", "Сначала сгенерируйте календарь")
            return
        
        # Диалог сохранения файла
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
                
                # Заголовок
                writer.writerow(['Номер недели', 'Начало недели', 'Конец недели',
                               'Четность'])
                
                # Данные
                for week in self.calendar_data:
                    writer.writerow([
                        week['week_num'],
                        week['start_date'].strftime("%d.%m.%Y"),
                        week['end_date'].strftime("%d.%m.%Y"),
                        "Нечётная" if "Нечётная" in week['parity'] else "Чётная",
                    ])
            
            self.status_var.set(f"✓ Календарь экспортирован в: {os.path.basename(filename)}")
            messagebox.showinfo("Экспорт завершен", 
                              f"Календарь успешно экспортирован в файл:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Ошибка экспорта", f"Не удалось сохранить файл:\n{str(e)}")
            self.status_var.set("Ошибка экспорта")
    
    def clear_output(self):
        """Очистка результатов"""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Очищаем данные
        self.calendar_data = []
        
        # Сбрасываем информацию
        self.info_text.set("Выберите год и нажмите 'СГЕНЕРИРОВАТЬ КАЛЕНДАРЬ'")
        self.today_info_text.set("Сгенерируйте\nкалендарь")
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


def main():
    """Запуск GUI приложения"""
    root = tk.Tk()
    app = AcademicCalendarGUI(root)
    
    # Центрируем окно
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()