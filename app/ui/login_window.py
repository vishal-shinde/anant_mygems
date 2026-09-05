import tkinter as tk
from tkinter import messagebox

from app.services.auth_service import authenticate


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MYGEMS Login")
        self.geometry("420x260")
        self.resizable(False, False)
        self.configure(bg="#f8fafc")

        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="MYGEMS", font=("Segoe UI", 24, "bold"), bg="#f8fafc", fg="#0f172a").pack(pady=(26, 12))

        form = tk.Frame(self, bg="#f8fafc")
        form.pack(padx=24, pady=10, fill="x")

        tk.Label(form, text="Username", bg="#f8fafc", anchor="w").pack(fill="x")
        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(form, textvariable=self.username_var, width=36)
        self.username_entry.pack(fill="x", pady=(4, 10))

        tk.Label(form, text="Password", bg="#f8fafc", anchor="w").pack(fill="x")
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(form, textvariable=self.password_var, show="*", width=36)
        self.password_entry.pack(fill="x", pady=(4, 16))

        btn = tk.Button(self, text="Login", width=20, command=self._login)
        btn.pack()

        self.username_entry.focus_set()
        self.bind("<Return>", lambda _event: self._login())

    def _login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()

        user = authenticate(username, password)
        if user is None:
            messagebox.showerror("Login failed", "Invalid username or password")
            return

        self.destroy()
        from app.ui.dashboard import DashboardWindow
        dashboard = DashboardWindow(user["username"])
        dashboard.mainloop()
