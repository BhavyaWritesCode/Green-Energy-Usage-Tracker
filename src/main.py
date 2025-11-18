import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sv_ttk  # Modern theme engine

from data_operations import register_user, login_user, add_energy_usage, fetch_energy_usage_by_user, month_exists
from analytics import get_full_analytics
from recommendation import generate_recommendations
from visualization import generate_all_visualizations
from utils import is_valid_email, to_float, clean_string
from config import MONTHS


# Ensure graph directory exists
GRAPH_DIR = os.path.join("assets", "graphs")
os.makedirs(GRAPH_DIR, exist_ok=True)


# MAIN APPLICATION CLASS 
class EnergyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # WINDOW CONFIG
        self.title("Green Energy Usage Tracker")
        self.geometry("1000x650")
        self.minsize(1000, 650)

        # Apply modern theme
        sv_ttk.set_theme("dark")     # choose light / dark

        # Track logged-in user
        self.current_user = None

        # Container for frames
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (StartFrame, RegisterFrame, LoginFrame, DashboardFrame):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartFrame")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def set_user(self, user_dict):
        self.current_user = user_dict


# START / WELCOME SCREEN
class StartFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)

        ttk.Label(
            self,
            text="🌿 Green Energy Usage Tracker",
            font=("Segoe UI", 26, "bold")
        ).grid(row=0, column=0, pady=(60, 10))

        ttk.Label(
            self,
            text="Monitor • Analyze • Reduce • Live Greener",
            font=("Segoe UI", 13)
        ).grid(row=1, column=0, pady=(0, 40))

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, column=0, pady=30)

        ttk.Button(btn_frame, text="Login", width=20,
                   command=lambda: controller.show_frame("LoginFrame")).grid(row=0, column=0, padx=10)

        ttk.Button(btn_frame, text="Register", width=20,
                   command=lambda: controller.show_frame("RegisterFrame")).grid(row=0, column=1, padx=10)

        ttk.Button(self, text="Exit", width=18,
                   command=controller.quit).grid(row=3, column=0, pady=20)


# REGISTER SCREEN
class RegisterFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Create Account",
                  font=("Segoe UI", 22, "bold")).pack(pady=(40, 10))

        form = ttk.Frame(self)
        form.pack(pady=15)

        self.entries = {}
        labels = ["Full Name", "Email", "Password", "City"]

        for i, label in enumerate(labels):
            ttk.Label(form, text=label + ":", font=("Segoe UI", 11))\
                .grid(row=i, column=0, sticky="w", pady=8, padx=10)

            entry = ttk.Entry(form, width=35,
                              show="*" if label == "Password" else "")
            entry.grid(row=i, column=1, pady=8)
            self.entries[label] = entry

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Create Account", width=20,
                   command=self.register).grid(row=0, column=0, padx=10)

        ttk.Button(btn_frame, text="Back", width=15,
                   command=lambda: controller.show_frame("StartFrame"))\
            .grid(row=0, column=1, padx=10)

    def register(self):
        name = clean_string(self.entries["Full Name"].get())
        email = self.entries["Email"].get().strip()
        password = self.entries["Password"].get().strip()
        city = clean_string(self.entries["City"].get())

        if not name or not email or not password:
            messagebox.showerror("Error", "Fill all required fields.")
            return

        if not is_valid_email(email):
            messagebox.showerror("Error", "Invalid Email Format!")
            return

        if register_user(name, email, password, city):
            messagebox.showinfo("Success", "Account created. Please login.")
            self.controller.show_frame("LoginFrame")
        else:
            messagebox.showerror("Error", "Email already exists!")


# LOGIN SCREEN
class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Login",
                  font=("Segoe UI", 22, "bold")).pack(pady=(50, 20))

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Email:", font=("Segoe UI", 11)).grid(
            row=0, column=0, sticky="w", pady=8, padx=10)
        self.email_entry = ttk.Entry(form, width=35)
        self.email_entry.grid(row=0, column=1, pady=8)

        ttk.Label(form, text="Password:", font=("Segoe UI", 11))\
            .grid(row=1, column=0, sticky="w", pady=8, padx=10)
        self.password_entry = ttk.Entry(form, width=35, show="*")
        self.password_entry.grid(row=1, column=1, pady=8)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Login", width=20,
                   command=self.login).grid(row=0, column=0, padx=10)

        ttk.Button(btn_frame, text="Back", width=15,
                   command=lambda: controller.show_frame("StartFrame"))\
            .grid(row=0, column=1, padx=10)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        user = login_user(email, password)
        if user:
            self.controller.set_user(user)
            messagebox.showinfo("Welcome", f"Hello {user['name']}!")
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Error", "Invalid credentials!")


# DASHBOARD SCREEN
class DashboardFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        top = ttk.Frame(self)
        top.pack(fill="x", pady=10)

        self.welcome_label = ttk.Label(
            top, text="", font=("Segoe UI", 17, "bold"))
        self.welcome_label.pack(side="left", padx=20)

        ttk.Button(
            top, text="Logout", width=15, command=self.logout
        ).pack(side="right", padx=20)

        content = ttk.Frame(self)
        content.pack(fill="both", expand=True, padx=20, pady=15)

        left = ttk.Frame(content)
        left.pack(side="left", fill="y", padx=15)

        right = ttk.Frame(content)
        right.pack(side="right", fill="both", expand=True, padx=15)

        # Sidebar buttons
        buttons = [
            ("Add Monthly Usage", self.add_usage_window),
            ("View Analytics", self.show_analytics),
            ("View Recommendations", self.show_recommendations),
            ("Generate Visualizations", self.generate_visuals_thread)
        ]

        for text, func in buttons:
            ttk.Button(left, text=text, width=24,
                       command=func).pack(pady=12)

        # Info box
        self.info_area = scrolledtext.ScrolledText(
            right, wrap=tk.WORD, font=("Consolas", 10),
            width=70, height=28
        )
        self.info_area.pack(fill="both", expand=True)

    def tkraise(self, *args, **kwargs):
        user = self.controller.current_user
        if user:
            self.welcome_label.config(
                text=f"Welcome, {user['name']} (ID: {user['user_id']})")
        super().tkraise(*args, **kwargs)

    def logout(self):
        self.controller.set_user(None)
        self.controller.show_frame("StartFrame")

    # -------------------- Add Usage -------------------------
    def add_usage_window(self):
        user = self.controller.current_user
        if not user:
            return

        win = tk.Toplevel(self)
        win.title("Add Monthly Usage")
        win.geometry("420x340")
        win.resizable(False, False)

        form = ttk.Frame(win, padding=20)
        form.pack(fill="both", expand=True)

        ttk.Label(form, text="Month:").grid(
            row=0, column=0, pady=10, sticky="w")
        month_cb = ttk.Combobox(form, values=MONTHS,
                                width=25, state="readonly")
        month_cb.grid(row=0, column=1)
        month_cb.current(0)

        def make_input(label, row):
            ttk.Label(form, text=label).grid(
                row=row, column=0, pady=10, sticky="w")
            entry = ttk.Entry(form, width=27)
            entry.grid(row=row, column=1)
            return entry

        elec_entry = make_input("Electricity (kWh):", 1)
        water_entry = make_input("Water (Liters):", 2)
        solar_entry = make_input("Solar Units:", 3)

        def submit():
            month = month_cb.get()
            elec = to_float(elec_entry.get())
            water = to_float(water_entry.get())
            solar = to_float(solar_entry.get())

            if None in (elec, water, solar):
                messagebox.showerror("Error", "Enter valid values")
                return

            if month_exists(user["user_id"], month):
                messagebox.showwarning(
                    "Exists", "You already added data for this month.")
                return

            if add_energy_usage(user["user_id"], month, elec, water, solar):
                messagebox.showinfo("Success", "Usage added.")
                win.destroy()

        ttk.Button(form, text="Submit", command=submit).grid(
            row=4, column=0, columnspan=2, pady=20)

    # -------------------- Show Analytics -------------------------
    def show_analytics(self):
        user = self.controller.current_user
        analytics = get_full_analytics(user["user_id"])
        if not analytics:
            self._set_info("No data. Add usage first.")
            return

        text = "\n=== ANALYTICS ===\n\n"
        for e in analytics["monthly_summary"]:
            text += f"{e['month']}: Elec={e['electricity_kwh']} | Water={e['water_liters']} | Solar={e['solar_units']} | Carbon={e['carbon_footprint']}\n"

        text += "\n=== Averages ===\n"
        avg = analytics["average_usage"]
        for k, v in avg.items():
            text += f"{k}: {v}\n"

        self._set_info(text)

    # -------------------- Show Recommendations -------------------------
    def show_recommendations(self):
        user = self.controller.current_user
        data = fetch_energy_usage_by_user(user["user_id"])
        if not data:
            self._set_info("No usage data available.")
            return

        recs = generate_recommendations(
            data[-1], data[-2] if len(data) > 1 else None)

        text = "\n=== RECOMMENDATIONS ===\n\n"
        for r in recs:
            text += f"• {r}\n"

        self._set_info(text)

    # -------------------- Generate Visuals -------------------------
    def generate_visuals_thread(self):
        threading.Thread(target=self.generate_visuals, daemon=True).start()

    def generate_visuals(self):
        user = self.controller.current_user
        outputs = generate_all_visualizations(user["user_id"])
        if not outputs:
            self._set_info("No data to generate graphs.")
            return

        text = "Generated graphs:\n\n"
        for k, path in outputs.items():
            text += f"- {k}: {path}\n"

        self._set_info(text)

    # -------------------- Update Info Box -------------------------
    def _set_info(self, content):
        self.info_area.config(state="normal")
        self.info_area.delete("1.0", "end")
        self.info_area.insert("end", content)
        self.info_area.config(state="disabled")


# RUN APP
if __name__ == "__main__":
    app = EnergyApp()
    app.mainloop()
