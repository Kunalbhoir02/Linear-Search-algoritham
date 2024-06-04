# Import necessary libraries and modules
import customtkinter as ctk     # Customized tkinter library
import tkinter as tk        # Standard tkinter library for GUI
import time                     # For adding delays during visualization
from CTkMessagebox import CTkMessagebox # Custom message box module


# List to store user-entered lists
stored_user_lists = []

# Linear search algorithm
def linear_search(arr, target, canvas, index=0):
    if index == len(arr):
        return -1  # Element not found
    canvas.yview_moveto(-1)
    
    # Calculate arrow coordinates for visualization
    x1, y1, x2, y2 = canvas.coords(elements_rectangles[index])
    x_center = (x1 + x2) / 2
    y_center = y1 - 10
    
    # Create arrow for visualization
    if(ctk.get_appearance_mode()=='Light'):
        arrow = canvas.create_line(x_center, y_center, x_center, y_center - 20, fill="black", arrow=tk.FIRST, arrowshape=(20, 20, 10), tags="arrow")
    else:
        arrow = canvas.create_line(x_center, y_center, x_center, y_center - 20, fill="white", arrow=tk.FIRST, arrowshape=(20, 20, 10), tags="arrow")
    canvas.itemconfigure(elements_rectangles[index], fill="yellow")
    canvas.update()
    time.sleep(0.5)
    
    # Compare current element with target
    if arr[index] == target:
        canvas.itemconfigure(elements_rectangles[index], fill="green", width=2)
        if index < len(arr):
            result_text = f"{target} IS "
            if arr[index] == target:
                result_text += "EQUAL TO "
                result_text += f"{arr[index]}\n"
                result_text += f"TARGET {target} FOUND AT INDEX {index}!"
                step_label.configure(text=step_label.cget("text") + result_text)
            else:
                result_text += "NOT EQUAL TO "
                result_text += f"{arr[index]}\n"
                step_label.configure(text=step_label.cget("text") + result_text)
        return index # Element found at this index
    else:
        # Element not found, visualize unsuccessful search
        canvas.itemconfigure(elements_rectangles[index], fill="red", width=2)
        canvas.update()
        canvas.delete(arrow)
        if index < len(arr):
            result_text = f"{target} IS "
            if arr[index] == target:
                result_text += "EQUAL TO "
                result_text += f"{arr[index]}\n"
                result_text += f"Target {target} FOUND AT INDEX {index}!"
                step_label.configure(text=step_label.cget("text") + result_text)
            else:
                result_text += "NOT EQUAL TO "
                result_text += f"{arr[index]}\n"
                step_label.configure(text=step_label.cget("text") + result_text)
        time.sleep(0.5)
    
    # Recursively continue search
    return linear_search(arr, target, canvas, index + 1)

# Draw elements on canvas
def draw_elements(canvas, elements, target):
    max_element_length = max(len(str(element)) for element in elements)
    box_width = max(20 * max_element_length, 60)
    box_height = 60
    spacing = 20
    max_boxes_per_row = (canvas.winfo_width() - 20) // (box_width + spacing)
    total_rows = (len(elements) - 1) // max_boxes_per_row + 1
    total_width = max_boxes_per_row * (box_width + spacing) - spacing
    total_height = total_rows * (box_height + spacing) - spacing
    canvas.configure(scrollregion=(0, 0, total_width, total_height))
    elements_rectangles.clear()
    
    for i, element in enumerate(elements):
        row = i // max_boxes_per_row
        col = i % max_boxes_per_row
        x1, y1 = col * (box_width + spacing), row * (box_height + spacing)
        x2, y2 = x1 + box_width, y1 + box_height
        
        # Draw box for element
        rectangle = canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue", width=2)
        label_text = f"{element}"
        canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=label_text, anchor="center", fill="black", font=("Arial", 20, "bold"))
        elements_rectangles.append(rectangle)
        
        # Draw index label at bottom of the box
        if(ctk.get_appearance_mode()=='Light'):
            index_text = f"Index:{i}"
            canvas.create_text((x1 + x2) // 2, y2 + 10, text=index_text, anchor="center", fill="black", font=("Arial", 13, "bold"))
        else:    
            index_text = f"Index:{i}"
            canvas.create_text((x1 + x2) // 2, y2 + 10, text=index_text, anchor="center", fill="white", font=("Arial", 13, "bold"))

#themes
def set_light_theme():
    ctk.set_appearance_mode("Light")# Customize this for your light theme
    update_ui()

def set_dark_theme():
    ctk.set_appearance_mode("Dark")# Customize this for your dark theme
    update_ui()

def toggle_theme():
    global dark_mode
    if dark_mode:
        set_light_theme()
    else:
        set_dark_theme()
    dark_mode = not dark_mode

def update_ui():
    # Update UI elements when the theme changes
    if dark_mode:
        canvas.configure(bg="white")# Customize other UI elements for dark theme
    else:
        canvas.configure(bg="#242424")# Customize other UI elements for light theme

dark_mode = False

# Search button click handler
def search_button_click():
    
    # Disable all buttons
    search_button.configure(state=ctk.DISABLED)
    clear_button.configure(state=ctk.DISABLED)
    stored_list_button.configure(state=ctk.DISABLED)
    theme_button.configure(state=ctk.DISABLED)
    step_label.configure(text="")
    global stored_user_lists
    try:
        elements_text = entry_elements.get("1.0", tk.END).strip()
        elements = elements_text.splitlines()
        elements = [element.strip() for element in elements]
        
        # Store the user-entered list
        stored_user_lists.append(elements)
        
        elements_no_duplicates = []
        for element in elements:
            if element not in elements_no_duplicates:
                elements_no_duplicates.append(element)
        
        target = entry_target.get()
        entered_list_label.configure(text=f" ENTERED LIST: [{', '.join(elements_no_duplicates)}] ", fg_color="black",text_color="white",font=("Arial", 16, "bold"))
        canvas.delete("all")
        draw_elements(canvas, elements_no_duplicates, target)
        
        result = linear_search(elements_no_duplicates, target, canvas)
        if result != -1:
            result_label.configure(text=f" TARGET {target} FOUND AT INDEX: {result} ", fg_color="green",text_color="white",font=("Arial", 16, "bold"))
            CTkMessagebox(title=" Target Found", message=f"Target found at index: {result} ")
        else:
            result_label.configure(text=f" TARGET {target} NOT FOUND IN THE LIST ", fg_color="red",text_color="white",font=("Arial", 16, "bold"))
            CTkMessagebox(title=" Target Not Found", message=f"Target {target} not found in the list ", icon="warning", option_1="Close")
    except ValueError:
        result_label.configure(text=" PLEASE ENTER VALID ELEMENT AND TARGET ", fg_color="red",text_color="white",font=("Arial", 16, "bold"))
        CTkMessagebox(title="Error", message=" Invalid input. Please enter valid elements and target. ", icon="cancel")
    finally:
        # Enable all buttons after the search is finished
        search_button.configure(state=ctk.NORMAL)
        clear_button.configure(state=ctk.NORMAL)
        stored_list_button.configure(state=ctk.NORMAL)
        theme_button.configure(state=ctk.NORMAL)
# Clear button click handler
def clear_button_click():
    entry_elements.delete("1.0", tk.END)
    entry_target.delete(0, tk.END)
    canvas.delete("all")
    entered_list_label.configure(text="", fg_color = "transparent")
    result_label.configure(text="", fg_color = "transparent")
    step_label.configure(text="")

# Update canvas size when window is resized
def update_canvas_size(event):
    canvas_width = max(root.winfo_reqwidth(), 500)
    canvas_height = max(root.winfo_reqheight(), 200)
    canvas.configure(width=canvas_width, height=canvas_height)
    
    if stored_user_lists:
        draw_elements(canvas, stored_user_lists[-1], entry_target.get())

# Show stored lists in a new window
def show_stored_list():
    stored_list_window = ctk.CTkToplevel(root)
    stored_list_window.title("ENTERED LIST HISTORY")
    stored_list_window.geometry("400x300")
    stored_list_label = ctk.CTkLabel(stored_list_window, text="ENTERED LIST HISTORY:",  font=("Arial", 25, "bold"))
    stored_list_label.pack(pady=10)
    for i, elements in enumerate(stored_user_lists, start=1):
        elements_text = ", ".join(elements)
        elements_label = ctk.CTkLabel(stored_list_window, text=f"List {i}: [{elements_text}]",  font=("Arial", 20))
        elements_label.pack()
    stored_list_window.after(100, stored_list_window.lift)

# Create the main application window
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Linear Search Algoritham")
    root.geometry("1026x750")
    ctk.set_appearance_mode("Dark")  #Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  #Themes: "blue" (standard), "green", "dark-blue"
    
    #entry frame and buttons
    entry_frame = ctk.CTkFrame(root)
    entry_frame.pack(padx=20, pady=5)
    
    entry_frame2 = ctk.CTkFrame(root)#theme button frame
    entry_frame2.place(x=0, y=0)

    label_elements = ctk.CTkLabel(entry_frame, text="Enter elements (one per line):",font=("Arial", 17,"bold"))
    label_elements.pack(pady=10)
    
    entry_elements = ctk.CTkTextbox(entry_frame, height=60, width=240, border_width=2, font=("Arial", 14))#element entry
    entry_elements.pack(padx=10)

    label_target = ctk.CTkLabel(entry_frame, text="Enter the target element:",font=("Arial", 17,"bold"))
    label_target.pack(pady=10)
    
    entry_target = ctk.CTkEntry(entry_frame, font=("Arial", 14))#target entry
    entry_target.pack()

    search_button = ctk.CTkButton(entry_frame, text="SEARCH", command=search_button_click)#search button
    search_button.pack(pady=10)

    clear_button = ctk.CTkButton(entry_frame, text="CLEAR", command=clear_button_click)#clear button
    clear_button.pack(pady=5)

    stored_list_button = ctk.CTkButton(entry_frame, text="ENTERED LISTS HISTORY", command=show_stored_list)#entered element history
    stored_list_button.pack(pady=10)

    entered_list_label = ctk.CTkLabel(root, text="", font=("Arial", 14))#entered list label
    entered_list_label.pack(pady=5)

    result_label = ctk.CTkLabel(root, text="", font=("Arial", 14))#result lable
    result_label.pack(pady=5)
    
    step_label = ctk.CTkLabel(root, text="", font=("Arial", 19))#step label
    step_label.place(x=900, y=10)

    theme_button = ctk.CTkButton(entry_frame2, text="Theme", command=toggle_theme)#theme button
    theme_button.pack(side="left")

    #canvas
    canvas_frame = ctk.CTkFrame(root)
    canvas_frame.pack(fill=tk.BOTH, expand=True)
    canvas_scrollbar = ctk.CTkScrollbar(canvas_frame)
    canvas_scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)
    canvas = tk.Canvas(canvas_frame, bg="#242424", yscrollcommand=canvas_scrollbar.set)
    canvas.pack( side = tk.LEFT,fill=tk.BOTH, expand=True)
    canvas_scrollbar.configure(command=canvas.yview)
    canvas.bind("<Configure>", update_canvas_size)
    elements_rectangles = []
    root.mainloop()
