
# Simple script to open a window and display a square using tkinter
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Square Display")
    canvas = tk.Canvas(root, width=300, height=300)
    canvas.pack()
    # Draw a square (x1, y1, x2, y2)
    canvas.create_rectangle(100, 100, 200, 200, fill="blue")
    root.mainloop()

if __name__ == "__main__":
    main()
