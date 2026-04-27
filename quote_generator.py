import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

DEFAULT_QUOTES = [
    {"text": "Будь изменением, которое ты хочешь увидеть в мире.", "author": "Махатма Ганди", "topic": "Мотивация"},
    {"text": "Жизнь - это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "topic": "Жизнь"},
    {"text": "Воображение важнее знания.", "author": "Альберт Эйнштейн", "topic": "Мудрость"},
    {"text": "То, что нас не убивает, делает нас сильнее.", "author": "Фридрих Ницше", "topic": "Вдохновение"},
    {"text": "Единственный способ делать великую работу - любить то, что ты делаешь.", "author": "Стив Джобс", "topic": "Мотивация"},
    {"text": "Не трать время на стук в стену в надежде превратить её в дверь.", "author": "Коко Шанель", "topic": "Жизнь"},
]

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("750x650")
        self.root.resizable(True, True)

        # Загрузка данных
        self.load_quotes()
        self.load_history()

        # Переменные для фильтров
        self.selected_author = tk.StringVar(value="Все")
        self.selected_topic = tk.StringVar(value="Все")

        # Интерфейс
        self.create_widgets()
        self.update_filter_values()
        self.filter_history()

    def load_quotes(self):
        """Загрузка цитат из JSON или создание базы по умолчанию"""
        if os.path.exists("quotes.json"):
            try:
                with open("quotes.json", "r", encoding="utf-8") as f:
                    self.quotes = json.load(f)
                print(f"Загружено {len(self.quotes)} цитат из quotes.json")
            except:
                self.quotes = DEFAULT_QUOTES.copy()
        else:
            self.quotes = DEFAULT_QUOTES.copy()
            self.save_quotes()
            print("Создан файл quotes.json с цитатами по умолчанию")

    def save_quotes(self):
        with open("quotes.json", "w", encoding="utf-8") as f:
            json.dump(self.quotes, f, ensure_ascii=False, indent=4)
        print(f"Сохранено {len(self.quotes)} цитат в quotes.json")

    def load_history(self):
        if os.path.exists("history.json"):
            try:
                with open("history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
                print(f"Загружено {len(self.history)} записей истории")
            except:
                self.history = []
        else:
            self.history = []

    def save_history(self):
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)
        print(f"Сохранено {len(self.history)} записей истории")

    def create_widgets(self):
        # Фрейм для отображения цитаты
        quote_frame = tk.LabelFrame(self.root, text="Случайная цитата", font=("Arial", 12, "bold"))
        quote_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.quote_text_label = tk.Label(quote_frame, text="", font=("Arial", 14), wraplength=650, justify="center", fg="#2c3e50")
        self.quote_text_label.pack(pady=20)

        self.author_label = tk.Label(quote_frame, text="", font=("Arial", 10, "italic"), fg="#7f8c8d")
        self.author_label.pack(pady=(0, 20))

        # Кнопки управления
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="🎲 Сгенерировать цитату", command=self.generate_quote, 
                 bg="#4CAF50", fg="white", padx=10, font=("Arial", 10)).pack(side="left", padx=5)
        tk.Button(btn_frame, text="➕ Добавить новую цитату", command=self.add_quote_dialog, 
                 bg="#2196F3", fg="white", padx=10, font=("Arial", 10)).pack(side="left", padx=5)

        # Фильтры
        filter_frame = tk.LabelFrame(self.root, text="Фильтры истории", font=("Arial", 10, "bold"))
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Автор:", font=("Arial", 9)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.author_combo = ttk.Combobox(filter_frame, textvariable=self.selected_author, state="readonly", width=25)
        self.author_combo.grid(row=0, column=1, padx=5, pady=5)
        self.author_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_history())

        tk.Label(filter_frame, text="Тема:", font=("Arial", 9)).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.topic_combo = ttk.Combobox(filter_frame, textvariable=self.selected_topic, state="readonly", width=20)
        self.topic_combo.grid(row=0, column=3, padx=5, pady=5)
        self.topic_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_history())

        tk.Button(filter_frame, text="🔄 Сбросить фильтры", command=self.reset_filters, 
                 bg="#95a5a6", fg="white", padx=10).grid(row=0, column=4, padx=10)

        # История
        history_frame = tk.LabelFrame(self.root, text="История цитат", font=("Arial", 10, "bold"))
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Добавим информацию о количестве
        self.history_info_label = tk.Label(history_frame, text="", font=("Arial", 8), fg="#7f8c8d")
        self.history_info_label.pack(anchor="w", padx=5, pady=(5, 0))

        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side="right", fill="y")

        self.history_listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set, height=10, 
                                          font=("Arial", 9), selectmode=tk.SINGLE)
        self.history_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        scrollbar.config(command=self.history_listbox.yview)

        # Добавим кнопку очистки истории
        clear_btn = tk.Button(history_frame, text="🗑 Очистить историю", command=self.clear_history,
                             bg="#e74c3c", fg="white", padx=10)
        clear_btn.pack(pady=5)

    def update_filter_values(self):
        """Обновление значений в выпадающих списках"""
        authors = sorted(set(q["author"] for q in self.quotes))
        topics = sorted(set(q["topic"] for q in self.quotes))
        
        self.author_combo['values'] = ["Все"] + authors
        self.topic_combo['values'] = ["Все"] + topics

    def refresh_quote_display(self, quote=None):
        if quote:
            self.quote_text_label.config(text=f'"{quote["text"]}"')
            self.author_label.config(text=f"— {quote['author']} (Тема: {quote['topic']})")
        else:
            self.quote_text_label.config(text="✨ Нажмите «Сгенерировать», чтобы увидеть цитату ✨")
            self.author_label.config(text="")

    def generate_quote(self):
        if not self.quotes:
            messagebox.showwarning("Нет цитат", "Сначала добавьте хотя бы одну цитату!")
            return

        quote = random.choice(self.quotes)
        self.refresh_quote_display(quote)

        # Сохраняем в историю
        history_entry = {
            "text": quote["text"],
            "author": quote["author"],
            "topic": quote["topic"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(history_entry)
        self.save_history()
        self.filter_history()  # обновляем отображение истории

    def add_quote_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить новую цитату")
        dialog.geometry("450x350")
        dialog.grab_set()
        dialog.resizable(False, False)

        tk.Label(dialog, text="Текст цитаты:", font=("Arial", 10, "bold")).pack(pady=(10,0))
        text_entry = tk.Text(dialog, height=5, width=50, font=("Arial", 10))
        text_entry.pack(pady=5, padx=10)

        tk.Label(dialog, text="Автор:", font=("Arial", 10, "bold")).pack(pady=(10,0))
        author_entry = tk.Entry(dialog, width=50, font=("Arial", 10))
        author_entry.pack(pady=5)

        tk.Label(dialog, text="Тема:", font=("Arial", 10, "bold")).pack(pady=(10,0))
        topic_entry = tk.Entry(dialog, width=50, font=("Arial", 10))
        topic_entry.pack(pady=5)

        def save_new():
            text = text_entry.get("1.0", tk.END).strip()
            author = author_entry.get().strip()
            topic = topic_entry.get().strip()

            # Проверка на пустые строки
            if not text:
                messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
                return
            if not author:
                messagebox.showerror("Ошибка", "Автор не может быть пустым!")
                return
            if not topic:
                messagebox.showerror("Ошибка", "Тема не может быть пустой!")
                return

            new_quote = {"text": text, "author": author, "topic": topic}
            self.quotes.append(new_quote)
            self.save_quotes()
            self.update_filter_values()  # Обновляем фильтры
            dialog.destroy()
            messagebox.showinfo("Успех", f"Цитата добавлена!\nВсего цитат: {len(self.quotes)}")

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="💾 Сохранить", command=save_new, bg="#4CAF50", fg="white", padx=20, font=("Arial", 10)).pack(side="left", padx=5)
        tk.Button(btn_frame, text="❌ Отмена", command=dialog.destroy, bg="#95a5a6", fg="white", padx=20, font=("Arial", 10)).pack(side="left", padx=5)

    def filter_history(self):
        """Фильтрация и отображение истории"""
        self.history_listbox.delete(0, tk.END)
        author_filter = self.selected_author.get()
        topic_filter = self.selected_topic.get()

        filtered_count = 0
        for entry in reversed(self.history):  # показываем последние сверху
            if author_filter != "Все" and entry["author"] != author_filter:
                continue
            if topic_filter != "Все" and entry["topic"] != topic_filter:
                continue

            # Форматируем отображение
            display_text = f'{entry["timestamp"]} | "{entry["text"][:60]}..." | {entry["author"]} | [{entry["topic"]}]'
            self.history_listbox.insert(tk.END, display_text)
            filtered_count += 1

        # Обновляем информацию
        self.history_info_label.config(text=f"Показано записей: {filtered_count} из {len(self.history)}")

    def reset_filters(self):
        self.selected_author.set("Все")
        self.selected_topic.set("Все")
        self.filter_history()

    def clear_history(self):
        """Очистка всей истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.filter_history()
            messagebox.showinfo("Успех", "История очищена!")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()