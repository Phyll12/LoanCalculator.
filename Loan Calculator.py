import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tabulate import tabulate

# Loan calculation functions
def calculate_monthly_payment(principal, annual_rate, years):
    monthly_rate = annual_rate / 12
    months = years * 12
    monthly_payment = principal * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)
    return monthly_payment

def generate_amortization_schedule(principal, annual_rate, years):
    monthly_payment = calculate_monthly_payment(principal, annual_rate, years)
    monthly_rate = annual_rate / 12
    months = years * 12
    balance = principal
    schedule = []

    for i in range(1, months + 1):
        interest = balance * monthly_rate
        principal_payment = monthly_payment - interest
        balance -= principal_payment
        schedule.append([i, round(monthly_payment, 2), round(interest, 2), round(principal_payment, 2), round(balance, 2)])

    return schedule

# Risk assessment function
def assess_risk(credit_score=None, dti_ratio=None):
    if credit_score and credit_score > 700:
        return "Low Risk"
    elif credit_score and 600 <= credit_score <= 700:
        return "Medium Risk"
    elif credit_score and credit_score < 600:
        return "High Risk"

    if dti_ratio and dti_ratio < 30:
        return "Low Risk"
    elif dti_ratio and 30 <= dti_ratio <= 40:
        return "Medium Risk"
    elif dti_ratio and dti_ratio > 40:
        return "High Risk"

    return "Insufficient data to assess risk"

# Visualization function
def visualize_amortization(schedule):
    months = [row[0] for row in schedule]
    principals = [row[3] for row in schedule]
    interests = [row[2] for row in schedule]
    balances = [row[4] for row in schedule]

    # Plot setup
    fig, axs = plt.subplots(2, 1, figsize=(8, 8))
    
    # Principal vs Interest Payments
    axs[0].plot(months, principals, label="Principal Payment", color="blue")
    axs[0].plot(months, interests, label="Interest Payment", color="orange")
    axs[0].set_title("Principal vs Interest Payments Over Time")
    axs[0].set_xlabel("Month")
    axs[0].set_ylabel("Amount")
    axs[0].legend()
    axs[0].grid()

    # Remaining Balance
    axs[1].plot(months, balances, label="Remaining Balance", color="green")
    axs[1].set_title("Loan Balance Over Time")
    axs[1].set_xlabel("Month")
    axs[1].set_ylabel("Balance")
    axs[1].legend()
    axs[1].grid()

    plt.tight_layout()
    plt.show()

# GUI Application
def calculate_loan():
    try:
        # Fetch input values
        principal = float(entry_principal.get())
        annual_rate = float(entry_annual_rate.get()) / 100
        years = int(entry_years.get())
        credit_score = entry_credit_score.get()
        credit_score = int(credit_score) if credit_score else None
        dti_ratio = entry_dti_ratio.get()
        dti_ratio = float(dti_ratio) if dti_ratio else None
        
        # Generate schedule
        schedule = generate_amortization_schedule(principal, annual_rate, years)
        risk_category = assess_risk(credit_score, dti_ratio)

        # Display schedule in TreeView
        for row in schedule_tree.get_children():
            schedule_tree.delete(row)
        for row in schedule:
            schedule_tree.insert("", tk.END, values=row)
        
        # Display risk assessment
        risk_label.config(text=f"Risk Assessment: {risk_category}")
        
        # Enable visualization button
        visualize_button.config(state=tk.NORMAL)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

def show_visualization():
    principal = float(entry_principal.get())
    annual_rate = float(entry_annual_rate.get()) / 100
    years = int(entry_years.get())
    schedule = generate_amortization_schedule(principal, annual_rate, years)
    visualize_amortization(schedule)

# Main GUI window
root = tk.Tk()
root.title("Loan Calculator")
root.geometry("800x600")

# Input fields
tk.Label(root, text="Principal (Loan Amount):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_principal = tk.Entry(root)
entry_principal.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Annual Interest Rate (%):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_annual_rate = tk.Entry(root)
entry_annual_rate.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Loan Term (Years):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_years = tk.Entry(root)
entry_years.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Credit Score (Optional):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_credit_score = tk.Entry(root)
entry_credit_score.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Debt-to-Income Ratio (Optional):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_dti_ratio = tk.Entry(root)
entry_dti_ratio.grid(row=4, column=1, padx=10, pady=5)

# Buttons
calculate_button = tk.Button(root, text="Calculate Loan", command=calculate_loan)
calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

visualize_button = tk.Button(root, text="Visualize Data", command=show_visualization, state=tk.DISABLED)
visualize_button.grid(row=6, column=0, columnspan=2, pady=10)

# Risk assessment display
risk_label = tk.Label(root, text="Risk Assessment: ", font=("Arial", 12))
risk_label.grid(row=7, column=0, columnspan=2, pady=10)

# Amortization schedule display
tk.Label(root, text="Amortization Schedule:").grid(row=8, column=0, columnspan=2)
columns = ["Month", "Payment", "Interest", "Principal", "Balance"]
schedule_tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    schedule_tree.heading(col, text=col)
schedule_tree.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()
