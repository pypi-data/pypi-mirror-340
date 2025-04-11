from tkinter import filedialog
import tkinter as tk


def browse(text, filetypes):
    """Opens a file dialog to browse and select a file.

    Args:
        text (tk.Entry): The Tkinter entry widget to update with the selected file path.
        filetypes (list): A list of tuples specifying the allowed file types in the dialog.

    Returns:
        None
    """
    file_path = filedialog.askopenfilename(filetypes=filetypes)
    if file_path:
        text.delete(0, tk.END)
        text.insert(0, file_path)
        text.xview(tk.END)


def java_browse(text, display, unbind, bind):
    """Opens a file dialog to browse and select a Java file.

    This function also updates a text display with the file's content and rebinds UI events.

    Args:
        text (tk.Entry): The Tkinter entry widget to update with the selected file path.
        display (tk.Text): The Tkinter text widget to display the Java source code.
        unbind (function): A function to unbind previous events.
        bind (function): A function to rebind events after selection.

    Returns:
        None
    """
    file_path = filedialog.askopenfilename(filetypes=[("Java files", "*.java")])
    if file_path:
        unbind()
        fill_java_src_window(file_path, display)

        text.delete(0, tk.END)
        text.insert(0, file_path)
        text.xview(tk.END)

        bind()


def fill_java_src_window(path, display):
    """Fills the Tkinter text widget with the contents of a Java source file.

    Args:
        path (str): Path to the Java source file.
        display (tk.Text): The Tkinter text widget to display the file content.

    Returns:
        None
    """
    try:
        with open(path, "r") as file:
            data = file.read()

        display.delete("0.0", "end")
        display.insert("0.0", data)
    except Exception as e:
        return
