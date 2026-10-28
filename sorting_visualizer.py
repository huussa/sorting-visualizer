
import tkinter as tk
from tkinter import ttk, messagebox
import random
import inspect
import ast
import importlib
import time
import sort


class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer")
        self.root.geometry("900x600")
        self.root.minsize(600, 400)

        self.arr = []
        self.original_arr = []
        self.steps = None
        self.running = False
        self.after_id = None
        self.timer_after_id = None
        self.timer_started_at = None
        self.algorithms = {}

        # =========================
        # Algorithm controls
        # =========================
        controls = ttk.Frame(root, padding=10)
        controls.pack(fill="x")

        ttk.Label(
            controls, text="Algorithm:"
        ).pack(side="left", padx=5)

        self.algorithm = ttk.Combobox(
            controls,
            state="readonly",
            width=18
        )
        self.algorithm.pack(side="left", padx=5)

        ttk.Button(
            controls,
            text="Refresh Algorithms",
            command=self.load_algorithms
        ).pack(side="left", padx=5)

        ttk.Button(
            controls,
            text="New Array",
            command=self.new_array
        ).pack(side="left", padx=5)

        self.start_button = ttk.Button(
            controls,
            text="Start Sorting",
            command=self.start_sort
        )
        self.start_button.pack(side="left", padx=5)

        self.stop_button = ttk.Button(
            controls,
            text="Stop",
            command=self.stop_sort,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=5)

        # =========================
        # Manual array input
        # =========================
        array_frame = ttk.Frame(
            root, padding=(10, 0, 10, 5)
        )
        array_frame.pack(fill="x")

        ttk.Label(
            array_frame, text="Array:"
        ).pack(side="left", padx=5)

        self.array_input = ttk.Entry(array_frame)
        self.array_input.pack(
            side="left", fill="x", expand=True, padx=5
        )

        self.array_input.insert(
            0, "[64, 34, 25, 12, 22, 11, 90]"
        )

        ttk.Button(
            array_frame,
            text="Load Array",
            command=self.load_array
        ).pack(side="left", padx=5)

        # =========================
        # Random array length
        # =========================
        length_frame = ttk.Frame(
            root, padding=(10, 0, 10, 5)
        )
        length_frame.pack(fill="x")

        ttk.Label(
            length_frame,
            text="Array Length:"
        ).pack(side="left", padx=5)

        self.array_length = tk.IntVar(value=30)

        ttk.Spinbox(
            length_frame,
            from_=2,
            to=10000,
            textvariable=self.array_length,
            width=8
        ).pack(side="left", padx=5)

        ttk.Button(
            length_frame,
            text="Generate Random Array",
            command=self.generate_random_array
        ).pack(side="left", padx=5)

        # =========================
        # Animation speed
        # =========================
        speed_frame = ttk.Frame(
            root, padding=(10, 0, 10, 5)
        )
        speed_frame.pack(fill="x")

        ttk.Label(
            speed_frame, text="Speed:"
        ).pack(side="left", padx=5)

        self.speed = tk.IntVar(value=1)

        ttk.Label(
            speed_frame,
            text="Faster"
        ).pack(side="left", padx=5)

        ttk.Scale(
            speed_frame,
            from_=10,
            to=500,
            variable=self.speed,
            orient="horizontal",
            length=180
        ).pack(side="left", padx=5)

        ttk.Label(
            speed_frame,
            text="Slower",
        ).pack(side="left", padx=5)

        # =========================
        # Status
        # =========================
        self.status = ttk.Label(
            root, text="Ready"
        )
        self.status.pack(pady=5)

        self.timer = ttk.Label(
            root,
            text="Time: 00:00.00",
            font=("TkDefaultFont", 14, "bold")
        )
        self.timer.pack(pady=(0, 5))

        # =========================
        # Drawing canvas
        # =========================
        self.canvas = tk.Canvas(
            root,
            background="#151923",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both", expand=True, padx=10, pady=10
        )

        self.load_algorithms()
        self.load_array()

        self.canvas.bind("<Configure>", self.draw)

    # =========================
    # Load algorithms from sort.py
    # =========================
    def load_algorithms(self):
        if self.running:
            messagebox.showinfo(
                "Sorting in Progress",
                "Stop the current sorting process first."
            )
            return

        try:
            importlib.invalidate_caches()
            importlib.reload(sort)

            self.algorithms = {
                name.replace("_", " ").replace("steps", "").title(): function
                for name, function in inspect.getmembers(
                    sort, inspect.isfunction
                )
                if function.__module__ == sort.__name__
                and name.endswith("_steps")
            }

            names = list(self.algorithms.keys())
            previous = self.algorithm.get()

            self.algorithm["values"] = names

            if previous in names:
                self.algorithm.set(previous)
            elif names:
                self.algorithm.set(names[0])
            else:
                self.algorithm.set("")

            if names:
                self.status.config(
                    text=f"{len(names)} algorithms loaded"
                )
            else:
                self.status.config(
                    text="No *_steps algorithms found"
                )

        except Exception as error:
            messagebox.showerror(
                "Import Error",
                f"Could not load sort.py:\n{error}"
            )

    # =========================
    # Load a manually entered array
    # =========================
    def load_array(self):
        if self.running:
            return False

        try:
            values = ast.literal_eval(
                self.array_input.get()
            )

            if not isinstance(values, (list, tuple)):
                raise ValueError(
                    "Enter a list of numbers."
                )

            if not all(
                isinstance(x, (int, float))
                and not isinstance(x, bool)
                for x in values
            ):
                raise ValueError(
                    "All elements must be numbers."
                )

            if not values:
                raise ValueError(
                    "Array cannot be empty."
                )

            self.arr = list(values)
            self.original_arr = self.arr.copy()

            self.array_length.set(len(self.arr))

            self.status.config(
                text=f"Loaded {len(self.arr)} elements"
            )

            self.draw()
            return True

        except (ValueError, SyntaxError, TypeError) as error:
            messagebox.showerror(
                "Invalid Array",
                f"Please enter a valid list of numbers.\n{error}"
            )
            return False

    # =========================
    # Generate a random array
    # =========================
    def generate_random_array(self):
        if self.running:
            return

        try:
            length = self.array_length.get()

            if not 2 <= length <= 10000:
                raise ValueError

            self.arr = [
                random.randint(1, 100)
                for _ in range(length)
            ]

            self.original_arr = self.arr.copy()

            self.array_input.delete(0, tk.END)
            self.array_input.insert(
                0, repr(self.arr)
            )

            self.status.config(
                text=f"Generated {length} elements"
            )

            self.draw()

        except (ValueError, tk.TclError):
            messagebox.showerror(
                "Invalid Length",
                "Enter an integer between 2 and 10000."
            )

    # =========================
    # Generate a new random array
    # =========================
    def new_array(self):
        if self.running:
            return

        self.generate_random_array()

    # =========================
    # Draw array bars
    # =========================
    def draw(self, event=None, active=()):
        self.canvas.delete("all")

        if not self.arr:
            return

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        maximum = max(abs(x) for x in self.arr)
        maximum = maximum or 1

        count = len(self.arr)
        bar_width = width / count

        for i, value in enumerate(self.arr):
            bar_height = (
                abs(value) / maximum
            ) * (height - 35)

            x1 = i * bar_width + 1
            x2 = (i + 1) * bar_width - 1
            y1 = height - bar_height
            y2 = height

            color = (
                "#ff9f43"
                if i in active
                else "#55b8f5"
            )

            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline=""
            )

    # =========================
    # Start sorting
    # =========================
    def start_sort(self):
        if self.running:
            return

        if not self.load_array():
            return

        name = self.algorithm.get()

        if name not in self.algorithms:
            messagebox.showerror(
                "No Algorithm",
                "Add a *_steps function to sort.py first."
            )
            return

        try:
            self.original_arr = self.arr.copy()

            self.steps = iter(
                self.algorithms[name](self.arr.copy())
            )

            self.running = True
            self.start_timer()

            self.start_button.config(
                state="disabled"
            )
            self.stop_button.config(
                state="normal"
            )

            self.status.config(
                text=f"Running {name}..."
            )

            self.animate()

        except Exception as error:
            self.running = False
            self.stop_timer()
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")

            messagebox.showerror(
                "Algorithm Error", str(error)
            )

    # =========================
    # Elapsed-time counter
    # =========================
    def start_timer(self):
        self.stop_timer()
        self.timer_started_at = time.perf_counter()
        self.update_timer()

    def update_timer(self):
        if not self.running or self.timer_started_at is None:
            return

        elapsed = time.perf_counter() - self.timer_started_at
        minutes, seconds = divmod(elapsed, 60)
        self.timer.config(
            text=f"Time: {int(minutes):02d}:{seconds:05.2f}"
        )
        self.timer_after_id = self.root.after(50, self.update_timer)

    def stop_timer(self):
        if self.timer_after_id is not None:
            self.root.after_cancel(self.timer_after_id)
            self.timer_after_id = None

        if self.timer_started_at is not None:
            elapsed = time.perf_counter() - self.timer_started_at
            minutes, seconds = divmod(elapsed, 60)
            self.timer.config(
                text=f"Time: {int(minutes):02d}:{seconds:05.2f}"
            )

        self.timer_started_at = None

    # =========================
    # Animate sorting steps
    # =========================
    def animate(self):
        if not self.running:
            return

        self.after_id = None

        try:
            current_arr, active = next(self.steps)

            if len(current_arr) != len(self.arr):
                raise ValueError(
                    "The algorithm changed the array length."
                )

            self.arr = list(current_arr)

            self.draw(active=active)

            delay = int(self.speed.get())

            self.after_id = self.root.after(
                delay, self.animate
            )

        except StopIteration:
            self.running = False
            self.steps = None
            self.stop_timer()

            self.start_button.config(
                state="normal"
            )
            self.stop_button.config(
                state="disabled"
            )

            self.status.config(text="Sorted!")
            self.draw()

        except Exception as error:
            self.running = False
            self.steps = None
            self.after_id = None
            self.stop_timer()

            self.start_button.config(
                state="normal"
            )
            self.stop_button.config(
                state="disabled"
            )

            messagebox.showerror(
                "Animation Error", str(error)
            )

    # =========================
    # Stop sorting
    # =========================
    def stop_sort(self):
        if not self.running:
            return

        self.running = False
        self.stop_timer()

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.steps = None

        self.start_button.config(
            state="normal"
        )
        self.stop_button.config(
            state="disabled"
        )

        self.status.config(text="Stopped")
        self.draw()

    # =========================
    # Run the application
    # =========================


if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
