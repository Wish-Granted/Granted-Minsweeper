from tkinter import *
from tkinter import messagebox

def get_dimensions(widget: Widget, string:bool = False) -> str:
    widget.winfo_toplevel().update()

    widget_height = widget.winfo_height()
    widget_width = widget.winfo_width()

    if string:
        return f"widget width: {widget_width}\nwidget height: {widget_height}"
    else:
        return widget_width, widget_height

def do_Use_Custom_Window_Title_Bar(root: Tk, text_colour: str, background_colour: str, font):
    root.overrideredirect(True)  # Remove the default title bar
    # Custom title bar
    title_bar = Frame(root, bg=background_colour, relief="raised", bd=0, height=30, border=2)
    title_bar.pack(fill=X)

    # Title text
    title_label = Label(title_bar, text=root.wm_title(), bg=background_colour, fg=text_colour) ######### make function stuff varible input stuff
    title_label.pack(side=LEFT, padx=10)

    # Close button
    close_button = Button(title_bar, text="X", bg="#aa0000", fg="white", command=root.destroy, bd=0)
    close_button.pack(side=RIGHT)

    # Dragging logic
    def start_move(event):
        root.x = event.x
        root.y = event.y

    def do_move(event):
        x = root.winfo_pointerx() - root.x
        y = root.winfo_pointery() - root.y
        root.geometry(f"+{x}+{y}")

    title_bar.bind("<Button-1>", start_move)
    title_bar.bind("<B1-Motion>", do_move)

    #print(get_dimensions(title_bar))
    
def get_inputs(*args):
    inputlist = []
    for input in args:
        if "text" in str(input):
            output = input.get(1.0, "end-1c")
        else:
            output = input.get()
        inputlist.append(output)
    return inputlist

def do_new_listbox(listbox: Listbox, new_list: list):
    listbox.delete(0, END)
    for item in new_list:
        listbox.insert(item)

if __name__ == "__main__":

    window_test = Tk()
    window_test.title("Test Window")
    window_test.geometry("400x300")
    label_test = Label(window_test, text="Elias is not a gooner", font="consolas")
    do_Use_Custom_Window_Title_Bar(window_test, text_colour="white", background_colour="#333333", font=("aptos", 11))

    label_test.pack()
    print(get_dimensions(label_test))

    window_test.mainloop()