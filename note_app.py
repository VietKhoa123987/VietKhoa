from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import hashlib

# ===== JSON FILES =====
json_file = "notes.json"
users_file = "users.json"

# ===== USER FUNCTIONS =====
def load_users():
    if not os.path.exists(users_file):
        return []
    with open(users_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(users_file, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ===== NOTE FUNCTIONS =====
def load_notes_from_json():
    if not os.path.exists(json_file):
        return []
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_notes_to_json(notes_data):
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(notes_data, f, indent=4, ensure_ascii=False)

# ===== ĐĂNG KÝ =====
# ===== ĐĂNG KÝ =====
def register():
    register_window = Toplevel()
    register_window.title("Đăng Ký")
    register_window.geometry("400x250")
    register_window.resizable(False, False)

    bg_label = Label(register_window, image=background_img)
    bg_label.place(relwidth=1, relheight=1)

    Label(register_window, text="Tài khoản:", font=("Helvetica", 12), bg="#ffffff").place(x=150, y=30)
    entry_user = Entry(register_window, font=("Helvetica", 12), width=30)
    entry_user.place(x=80, y=60)

    Label(register_window, text="Mật khẩu:", font=("Helvetica", 12), bg="#ffffff").place(x=150, y=100)
    entry_pass = Entry(register_window, show="*", font=("Helvetica", 12), width=30)
    entry_pass.place(x=80, y=130)

    def save_register():
        username = entry_user.get().strip()
        password = entry_pass.get()

        if not username or not password:
            messagebox.showerror("Lỗi", "Không được để trống")
            return

        users = load_users()
        for user in users:
            if user["username"] == username:
                messagebox.showerror("Lỗi", "Tài khoản đã tồn tại")
                return

        users.append({"username": username, "password": hash_password(password)})
        save_users(users)
        messagebox.showinfo("Thành công", "Đăng ký thành công")
        register_window.destroy()

    Button(register_window, text="Đăng ký", font=("Helvetica", 12), command=save_register).place(x=160, y=180)
# ===== ĐĂNG NHẬP =====
def login():
    username = user_entry.get()
    password = pass_entry.get()
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == hash_password(password):
            login_window.destroy()
            show_note_app()
            return
    messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu")

# ===== GIAO DIỆN CHÍNH =====
def show_note_app():
    window.deiconify()
    window.title("Ứng dụng Ghi chú")
    window.geometry("600x400")
    Label(window, text="Chào mừng bạn đến với ứng dụng ghi chú!", font=("Helvetica", 14)).pack(pady=20)

# ===== MAIN WINDOW =====
window = tk.Tk()
window.withdraw()

# Load ảnh nền và resize
bg_img_raw = Image.open("background.png")  # đổi tên nếu cần
bg_img_resized = bg_img_raw.resize((400, 250))
background_img = ImageTk.PhotoImage(bg_img_resized)

# Login window
login_window = Toplevel(window)
login_window.title("Đăng Nhập")
login_window.geometry("400x250")
login_window.resizable(False, False)

bg_label_login = Label(login_window, image=background_img)
bg_label_login.place(relwidth=1, relheight=1)

# Không dùng Frame trắng, chỉ đặt label và entry trực tiếp lên ảnh nền
Label(login_window, text="Tài khoản:", font=("Helvetica", 12), bg="#ffffff").place(x=150, y=30)
user_entry = Entry(login_window, font=("Helvetica", 12), width=30)
user_entry.place(x=80, y=60)

Label(login_window, text="Mật khẩu:", font=("Helvetica", 12), bg="#ffffff").place(x=150, y=100)
pass_entry = Entry(login_window, show="*", font=("Helvetica", 12), width=30)
pass_entry.place(x=80, y=130)

Button(login_window, text="Đăng Nhập", font=("Helvetica", 12), command=login).place(x=150, y=170)
Button(login_window, text="Đăng Ký", font=("Helvetica", 12), command=register).place(x=155, y=200)

# ===== CHẠY =====
window.mainloop()
