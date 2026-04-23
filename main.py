import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import json

# Глобальные переменные
favourites = []

# URL API
GITHUB_API_URL = "https://api.github.com/users/"

def search_user():
    username = search_entry.get().strip()
    if not username:
        messagebox.showwarning("Внимание", "Поле поиска не должно быть пустым.")
        return
    
    url = GITHUB_API_URL + username
    response = requests.get(url)
    if response.status_code == 200:
        user_data = response.json()
        display_search_result(user_data)
    else:
        messagebox.showerror("Ошибка", f"Пользователь '{username}' не найден.")

def display_search_result(user_data):
    result_list.delete(0, tk.END)
    info = f"{user_data['login']} ({user_data['name']})"
    result_list.insert(tk.END, info)
    result_list.bind('<Double-Button-1>', lambda e: add_to_favourites(user_data))

def add_to_favourites(user_data):
    if user_data['login'] not in [u['login'] for u in favourites]:
        favourites.append(user_data)
        favourites_list.insert(tk.END, user_data['login'])
    else:
        messagebox.showinfo("Информация", "Этот пользователь уже в избранном.")

def save_favourites():
    path = filedialog.asksaveasfilename(defaultextension=".json",
                                        filetypes=[("JSON Files", "*.json")])
    if path:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(favourites, f, ensure_ascii=False, indent=2)

def load_favourites():
    global favourites
    path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if path:
        with open(path, 'r', encoding='utf-8') as f:
            favourites = json.load(f)
        favourites_list.delete(0, tk.END)
        for user in favourites:
            favourites_list.insert(tk.END, user['login'])

# Создаем интерфейс
root = tk.Tk()
root.title("GitHub User Finder")
root.geometry("600x400")

# Поле поиска
tk.Label(root, text="Введите имя пользователя GitHub:").pack(pady=5)
search_entry = tk.Entry(root, width=50)
search_entry.pack(pady=5)

# Кнопка поиска
tk.Button(root, text="Поиск", command=search_user).pack(pady=5)

# Результаты поиска
tk.Label(root, text="Результат поиска:").pack(pady=5)
result_list = tk.Listbox(root, height=1)
result_list.pack(fill=tk.X, padx=10, pady=5)

# Инструкции по двойному клику или отдельной кнопке для добавления в избранное
tk.Label(root, text="Дважды кликните по результату, чтобы добавить в избранное.").pack(pady=5)

# Список избранных
tk.Label(root, text="Избранные пользователи:").pack(pady=5)
favourites_list = tk.Listbox(root)
favourites_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Кнопки для сохранения и загрузки
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Сохранить избранное", command=save_favourites).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Загрузить избранное", command=load_favourites).pack(side=tk.LEFT, padx=5)

root.mainloop()