import tkinter as tk

lives = 3
root = tk.Tk()
frame = tk.Frame(root)              # first argument indicates the widget/child container
canvas = tk.Canvas(frame, width=600, height=400, bg='#aaaaff')
frame.pack()
canvas.pack()
root.title('Hello, pong!')
root.mainloop()
