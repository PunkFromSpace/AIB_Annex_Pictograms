import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Function to map hostility class to graphical properties
def get_hostility_symbol(hostility):
    if hostility == "safe":
        return {"circle_type": "dotted", "radius": 0.2, "line_width": 1.5}
    elif hostility == "moderate":
        return {"circle_type": "solid", "radius": 0.2, "line_width": 1.5}
    elif hostility == "hazardous":
        return {"circle_type": "double", "radius": 0.2, "line_width": 2.0}
    else:
        raise ValueError("Invalid hostility class. Choose from 'safe', 'moderate', or 'hazardous'.")

# Function to generate the pictograph
def draw_pictograph(data):
    fig, ax = plt.subplots(figsize=(5, 5))

    # Add the center circle for hostility class
    hostility = get_hostility_symbol(data["hostility"])
    if hostility["circle_type"] == "dotted":
        circle = patches.Circle((0.5, 0.5), hostility["radius"], fill=False, linestyle="dotted", linewidth=hostility["line_width"])
        ax.add_patch(circle)
    elif hostility["circle_type"] == "solid":
        circle = patches.Circle((0.5, 0.5), hostility["radius"], fill=False, linestyle="solid", linewidth=hostility["line_width"])
        ax.add_patch(circle)
    elif hostility["circle_type"] == "double":
        outer_circle = patches.Circle((0.5, 0.5), hostility["radius"], fill=False, linestyle="solid", linewidth=hostility["line_width"])
        inner_circle = patches.Circle((0.5, 0.5), hostility["radius"] - 0.05, fill=False, linestyle="solid", linewidth=hostility["line_width"])
        ax.add_patch(outer_circle)
        ax.add_patch(inner_circle)

    # Add a symbol for finiteness on the outer circle
    if data["finiteness"] == "infinite":
        ax.annotate("△", xy=(0.8, 0.5), fontsize=15, ha="center", va="center")
    elif data["finiteness"] == "finite":
        ax.annotate("T", xy=(0.8, 0.5), fontsize=15, ha="center", va="center")
    else:
        raise ValueError("Invalid finiteness. Choose from 'infinite' or 'finite'.")

    # Set limits and aspect ratio
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')  # Hide axes

    # Save the image with the annex code as the file name
    filename = f"{data['annex_code']}_symbol.png"
    plt.savefig(filename, dpi=300)
    print(f"Pictograph saved as '{filename}'.")
    plt.show()

# Function to handle GUI submission
def submit():
    annex_code = annex_code_entry.get().strip()
    hostility = hostility_var.get()
    finiteness = finiteness_var.get()

    # Validate inputs
    if not annex_code:
        messagebox.showerror("Input Error", "Please enter an annex code.")
        return

    if not hostility or not finiteness:
        messagebox.showerror("Input Error", "Please select both hostility and finiteness.")
        return

    # Collect data and generate the pictograph
    data = {
        "annex_code": annex_code,
        "hostility": hostility,
        "finiteness": finiteness
    }
    try:
        draw_pictograph(data)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the GUI
root = tk.Tk()
root.title("Pictograph Generator")

# Input fields
tk.Label(root, text="Annex Code:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
annex_code_entry = tk.Entry(root)
annex_code_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Hostility:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
hostility_var = tk.StringVar()
hostility_dropdown = ttk.Combobox(root, textvariable=hostility_var, state="readonly")
hostility_dropdown["values"] = ["Safe", "Moderate", "Hazardous"]
hostility_dropdown.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Finiteness:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
finiteness_var = tk.StringVar()
finiteness_dropdown = ttk.Combobox(root, textvariable=finiteness_var, state="readonly")
finiteness_dropdown["values"] = ["Infinite", "Finite"]
finiteness_dropdown.grid(row=2, column=1, padx=5, pady=5)

# Submit button
submit_button = tk.Button(root, text="Generate Pictograph", command=submit)
submit_button.grid(row=3, column=0, columnspan=2, pady=10)

# Run the GUI loop
root.mainloop()
