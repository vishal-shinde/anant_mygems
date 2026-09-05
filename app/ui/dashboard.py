import tkinter as tk
from tkinter import messagebox

from app.ui.legacy_bridge import (
    open_legacy_admin_module,
    open_legacy_customer_module,
    open_legacy_employee_module,
    open_legacy_expense_module,
    open_legacy_inventory_module,
    open_legacy_labor_module,
    open_legacy_material_return_module,
    open_legacy_purchase_module,
    open_legacy_sales_module,
)


class DashboardWindow(tk.Tk):
    def __init__(self, username: str):
        super().__init__()
        self.title("MYGEMS Dashboard")
        self.geometry("900x560")
        self.minsize(760, 500)
        self.configure(bg="#0f172a")
        self.username = username

        self._build_ui()

    def _build_ui(self):
        title = tk.Label(
            self,
            text=f"Welcome, {self.username}",
            font=("Segoe UI", 18, "bold"),
            fg="#f8fafc",
            bg="#0f172a",
        )
        title.pack(pady=(24, 12))

        summary = tk.Label(
            self,
            text="Unified ERP workspace",
            fg="#cbd5e1",
            bg="#0f172a",
            font=("Segoe UI", 11),
        )
        summary.pack(pady=(0, 24))

        cards = [
            ("Sales", "Open sales screen"),
            ("Purchases", "Track purchases and metal entries"),
            ("Customers", "Customer management"),
            ("Employees", "Employee and labor management"),
            ("Expenses", "Expense management"),
            ("Inventory", "Stock and lot management"),
            ("Labor", "Work and task tracking"),
            ("Admin", "User and permission management"),
            ("Returns", "Material return handling"),
        ]

        grid = tk.Frame(self, bg="#0f172a")
        grid.pack(padx=24, pady=8, fill="both", expand=True)

        for index, (label, description) in enumerate(cards):
            row = index // 3
            col = index % 3
            card = tk.Frame(grid, bg="#111827", bd=1, relief="solid", padx=18, pady=18)
            card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
            tk.Label(card, text=label, fg="#f8fafc", bg="#111827", font=("Segoe UI", 15, "bold")).pack(anchor="w")
            tk.Label(card, text=description, fg="#94a3b8", bg="#111827", font=("Segoe UI", 10)).pack(anchor="w", pady=(8, 0))
            action = tk.Button(card, text="Open", command=lambda name=label: self._open_module(name))
            action.pack(anchor="w", pady=(12, 0))

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)
        grid.rowconfigure(0, weight=1)
        grid.rowconfigure(1, weight=1)
        grid.rowconfigure(2, weight=1)

        footer = tk.Frame(self, bg="#0f172a")
        footer.pack(fill="x", padx=20, pady=(0, 20))
        tk.Button(footer, text="Logout", width=18, command=self._logout).pack(anchor="e")

    def _open_module(self, name: str):
        actions = {
            "Sales": open_legacy_sales_module,
            "Purchases": open_legacy_purchase_module,
            "Customers": open_legacy_customer_module,
            "Employees": open_legacy_employee_module,
            "Expenses": open_legacy_expense_module,
            "Inventory": open_legacy_inventory_module,
            "Labor": open_legacy_labor_module,
            "Admin": open_legacy_admin_module,
            "Returns": open_legacy_material_return_module,
        }

        action = actions.get(name)
        if action is None:
            messagebox.showinfo("Module", f"{name} is ready to be wired into the new app structure.")
            return

        self.withdraw()
        try:
            action()
        finally:
            self.deiconify()

    def _logout(self):
        self.destroy()
