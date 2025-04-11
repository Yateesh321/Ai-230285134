import tkinter as tk
from tkinter import ttk, messagebox
from owlready2 import *
import math

# Load the ontology
onto = get_ontology("geometry_ontology.owl").load()

class GeometryTutor:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent Tutoring System for Geometry")
        self.root.geometry("600x500")  # Increased size for more shapes
        
        self.create_widgets()
    
    def create_widgets(self):
        # Shape selection
        ttk.Label(self.root, text="Select a shape:").pack(pady=10)
        self.shape_var = tk.StringVar()
        self.shape_combobox = ttk.Combobox(self.root, textvariable=self.shape_var, 
                                         values=["Triangle", "Rectangle", "Square", 
                                                "Circle", "Parallelogram", "Trapezoid", "Rhombus"])
        self.shape_combobox.pack(pady=5)
        self.shape_combobox.bind("<<ComboboxSelected>>", self.update_input_fields)
        
        # Input frame
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(pady=20)
        
        # Calculate button
        ttk.Button(self.root, text="Calculate Area", command=self.calculate_area).pack(pady=10)
        
        # Result display
        self.result_label = ttk.Label(self.root, text="", font=('Arial', 12))
        self.result_label.pack(pady=20)
        
        # Explanation frame
        self.explanation_frame = ttk.LabelFrame(self.root, text="Explanation")
        self.explanation_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.explanation_text = tk.Text(self.explanation_frame, height=6, wrap="word")
        self.explanation_text.pack(pady=5, padx=5, fill="both", expand=True)
        
        # Initially hide input fields until shape is selected
        self.input_fields = []
    
    def update_input_fields(self, event=None):
        # Clear previous input fields
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        self.input_fields = []
        
        shape = self.shape_var.get()
        
        if shape == "Triangle":
            ttk.Label(self.input_frame, text="Base:").grid(row=0, column=0, padx=5, pady=5)
            base_entry = ttk.Entry(self.input_frame)
            base_entry.grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(self.input_frame, text="Height:").grid(row=1, column=0, padx=5, pady=5)
            height_entry = ttk.Entry(self.input_frame)
            height_entry.grid(row=1, column=1, padx=5, pady=5)
            
            self.input_fields = [("base", base_entry), ("height", height_entry)]
            
        elif shape == "Rectangle":
            ttk.Label(self.input_frame, text="Length:").grid(row=0, column=0, padx=5, pady=5)
            length_entry = ttk.Entry(self.input_frame)
            length_entry.grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(self.input_frame, text="Width:").grid(row=1, column=0, padx=5, pady=5)
            width_entry = ttk.Entry(self.input_frame)
            width_entry.grid(row=1, column=1, padx=5, pady=5)
            
            self.input_fields = [("length", length_entry), ("width", width_entry)]
            
        elif shape == "Square":
            ttk.Label(self.input_frame, text="Side:").grid(row=0, column=0, padx=5, pady=5)
            side_entry = ttk.Entry(self.input_frame)
            side_entry.grid(row=0, column=1, padx=5, pady=5)
            
            self.input_fields = [("side", side_entry)]
            
        elif shape == "Circle":
            ttk.Label(self.input_frame, text="Radius:").grid(row=0, column=0, padx=5, pady=5)
            radius_entry = ttk.Entry(self.input_frame)
            radius_entry.grid(row=0, column=1, padx=5, pady=5)
            
            self.input_fields = [("radius", radius_entry)]
            
        elif shape == "Parallelogram":
            ttk.Label(self.input_frame, text="Base:").grid(row=0, column=0, padx=5, pady=5)
            base_entry = ttk.Entry(self.input_frame)
            base_entry.grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(self.input_frame, text="Height:").grid(row=1, column=0, padx=5, pady=5)
            height_entry = ttk.Entry(self.input_frame)
            height_entry.grid(row=1, column=1, padx=5, pady=5)
            
            self.input_fields = [("base", base_entry), ("height", height_entry)]
            
        elif shape == "Trapezoid":
            ttk.Label(self.input_frame, text="Base 1:").grid(row=0, column=0, padx=5, pady=5)
            base1_entry = ttk.Entry(self.input_frame)
            base1_entry.grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(self.input_frame, text="Base 2:").grid(row=1, column=0, padx=5, pady=5)
            base2_entry = ttk.Entry(self.input_frame)
            base2_entry.grid(row=1, column=1, padx=5, pady=5)
            
            ttk.Label(self.input_frame, text="Height:").grid(row=2, column=0, padx=5, pady=5)
            height_entry = ttk.Entry(self.input_frame)
            height_entry.grid(row=2, column=1, padx=5, pady=5)
            
            self.input_fields = [("base1", base1_entry), ("base2", base2_entry), ("height", height_entry)]
            
        elif shape == "Rhombus":
            ttk.Label(self.input_frame, text="Diagonal 1:").grid(row=0, column=0, padx=5, pady=5)
            d1_entry = ttk.Entry(self.input_frame)
            d1_entry.grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(self.input_frame, text="Diagonal 2:").grid(row=1, column=0, padx=5, pady=5)
            d2_entry = ttk.Entry(self.input_frame)
            d2_entry.grid(row=1, column=1, padx=5, pady=5)
            
            self.input_fields = [("diagonal1", d1_entry), ("diagonal2", d2_entry)]
    
    def calculate_area(self):
        shape_type = self.shape_var.get()
        if not shape_type:
            messagebox.showerror("Error", "Please select a shape first!")
            return
        
        try:
            # Get input values
            inputs = {}
            for field_name, entry in self.input_fields:
                value = float(entry.get())
                if value <= 0:
                    raise ValueError("Dimensions must be positive numbers")
                inputs[field_name] = value
            
            # Calculate area based on shape
            if shape_type == "Triangle":
                area = 0.5 * inputs["base"] * inputs["height"]
                explanation = f"Area of Triangle = 1/2 × base × height\n= 1/2 × {inputs['base']} × {inputs['height']}\n= {area:.2f}"
                
            elif shape_type == "Rectangle":
                area = inputs["length"] * inputs["width"]
                explanation = f"Area of Rectangle = length × width\n= {inputs['length']} × {inputs['width']}\n= {area:.2f}"
                
            elif shape_type == "Square":
                area = inputs["side"] ** 2
                explanation = f"Area of Square = side × side\n= {inputs['side']} × {inputs['side']}\n= {area:.2f}"
                
            elif shape_type == "Circle":
                area = math.pi * (inputs["radius"] ** 2)
                explanation = f"Area of Circle = π × radius²\n= π × {inputs['radius']}²\n= {area:.2f}"
                
            elif shape_type == "Parallelogram":
                area = inputs["base"] * inputs["height"]
                explanation = f"Area of Parallelogram = base × height\n= {inputs['base']} × {inputs['height']}\n= {area:.2f}"
                
            elif shape_type == "Trapezoid":
                area = 0.5 * (inputs["base1"] + inputs["base2"]) * inputs["height"]
                explanation = f"Area of Trapezoid = 1/2 × (base1 + base2) × height\n= 1/2 × ({inputs['base1']} + {inputs['base2']}) × {inputs['height']}\n= {area:.2f}"
                
            elif shape_type == "Rhombus":
                area = 0.5 * inputs["diagonal1"] * inputs["diagonal2"]
                explanation = f"Area of Rhombus = 1/2 × diagonal1 × diagonal2\n= 1/2 × {inputs['diagonal1']} × {inputs['diagonal2']}\n= {area:.2f}"
            
            # Display results
            self.result_label.config(text=f"Area of the {shape_type}: {area:.2f}")
            self.explanation_text.delete(1.0, tk.END)
            self.explanation_text.insert(tk.END, explanation)
            
            # Update ontology with this calculation
            self.update_ontology(shape_type, inputs, area)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def update_ontology(self, shape_type, inputs, area):
        # Create a new individual in the ontology for this calculation
        with onto:
            if shape_type == "Triangle":
                new_shape = onto.Triangle()
                new_shape.hasBaseValue = inputs["base"]
                new_shape.hasHeightValue = inputs["height"]
                new_shape.hasAreaValue = area
                
            elif shape_type == "Rectangle":
                new_shape = onto.Rectangle()
                new_shape.hasLengthValue = inputs["length"]
                new_shape.hasWidthValue = inputs["width"]
                new_shape.hasAreaValue = area
                
            elif shape_type == "Square":
                new_shape = onto.Square()
                new_shape.hasSideValue = inputs["side"]
                new_shape.hasAreaValue = area
                
            elif shape_type == "Circle":
                new_shape = onto.Circle()
                new_shape.hasRadiusValue = inputs["radius"]
                new_shape.hasAreaValue = area
                
            elif shape_type == "Parallelogram":
                new_shape = onto.Parallelogram()
                new_shape.hasBaseValue = inputs["base"]
                new_shape.hasHeightValue = inputs["height"]
                new_shape.hasAreaValue = area
                
            elif shape_type == "Trapezoid":
                new_shape = onto.Trapezoid()
                new_shape.hasBase1Value = inputs["base1"]
                new_shape.hasBase2Value = inputs["base2"]
                new_shape.hasHeightValue = inputs["height"]
                new_shape.hasAreaValue = area
                
            elif shape_type == "Rhombus":
                new_shape = onto.Rhombus()
                new_shape.hasDiagonal1Value = inputs["diagonal1"]
                new_shape.hasDiagonal2Value = inputs["diagonal2"]
                new_shape.hasAreaValue = area
            
            # Save the updated ontology
            onto.save(file="geometry_ontology.owl")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeometryTutor(root)
    root.mainloop()