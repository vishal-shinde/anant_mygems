import importlib.util
import os
import sys
import tkinter as tk
from tkinter import messagebox


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def _load_module(module_name: str, file_name: str):
    path = os.path.join(BASE_DIR, file_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Module file not found: {path}")

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module '{module_name}' from '{path}'")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _open_class_window(module_name: str, file_name: str, class_name: str, root_mode: bool = False):
    try:
        module = _load_module(module_name, file_name)
        app_cls = getattr(module, class_name)
        if root_mode:
            root = tk.Tk()
            app_cls(root)
            root.mainloop()
        else:
            app = app_cls()
            app.mainloop()
    except Exception as exc:  # pragma: no cover - UI fallback
        messagebox.showerror("Module Launch Error", f"Unable to open {class_name}:\n{exc}")


def open_legacy_sales_module():
    _open_class_window("sales_module", "sales_module.py", "SalesOrderApp")


def open_legacy_customer_module():
    _open_class_window("add_customer", "add_customer.py", "CustomerForm", root_mode=True)


def open_legacy_employee_module():
    _open_class_window("add_employee", "add_employee.py", "EmployeeForm", root_mode=True)


def open_legacy_expense_module():
    _open_class_window("EXPENSE_MANAGER", "EXPENSE_MANAGER.PY", "JewelryERPApp")


def open_legacy_purchase_module():
    _open_class_window("metal_purchase", "metal_purchase-WITH_SPLIT_LOT_FIXED_2.py", "MetalPurchaseApp", root_mode=True)


def open_legacy_labor_module():
    _open_class_window("add_labor", "add_labor.py", "LabourManagementApp", root_mode=True)


def open_legacy_inventory_module():
    _open_class_window("stone_mixing", "stone_mixing.py", "StoneLotMixingApp", root_mode=True)


def open_legacy_admin_module():
    _open_class_window("admin_users", "admin_users.py", "UserManagement", root_mode=True)


def open_legacy_material_return_module():
    _open_class_window("material_return", "material_return.py", "MaterialReturnForm", root_mode=True)
