"""
COS202 - Mathematical Calculator (MC)
Author: [Your Name]
Description: An interactive GUI-based mathematical calculator built with Python's Tkinter library.
             Supports addition, subtraction, multiplication, division, integer division,
             exponentiation, modulus, clear, and off operations.
"""

import tkinter as tk
from tkinter import messagebox


# ──────────────────────────────────────────────
#  Colour & font constants
# ──────────────────────────────────────────────
BG_MAIN       = "#1e1e2e"   # deep navy – main window background
BG_DISPLAY    = "#181825"   # slightly darker for the display panel
FG_DISPLAY    = "#cdd6f4"   # soft white text on display

BTN_NUM_BG    = "#313244"   # number buttons
BTN_NUM_FG    = "#cdd6f4"
BTN_NUM_HOVER = "#45475a"

BTN_OP_BG     = "#fab387"   # operator buttons (orange accent)
BTN_OP_FG     = "#1e1e2e"
BTN_OP_HOVER  = "#fe8019"

BTN_SPEC_BG   = "#a6e3a1"   # special: C / OFF (green accent)
BTN_SPEC_FG   = "#1e1e2e"
BTN_SPEC_HOVER= "#40a02b"

BTN_EQ_BG     = "#89b4fa"   # equals (blue accent)
BTN_EQ_FG     = "#1e1e2e"
BTN_EQ_HOVER  = "#74c7ec"

FONT_DISPLAY  = ("Consolas", 26, "bold")
FONT_EXPR     = ("Consolas", 13)
FONT_BTN      = ("Segoe UI", 15, "bold")
FONT_SMALL_BTN= ("Segoe UI", 13, "bold")


# ──────────────────────────────────────────────
#  Calculator Logic
# ──────────────────────────────────────────────
class Calculator:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("MC – Mathematical Calculator")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_MAIN)

        self.expression = ""   # full expression string
        self.just_evaluated = False  # flag: did we just press '='?

        self._build_display()
        self._build_buttons()

    # ── Display panel ──────────────────────────
    def _build_display(self):
        display_frame = tk.Frame(self.root, bg=BG_DISPLAY, padx=12, pady=10)
        display_frame.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=10, pady=(10, 4))

        # Small expression label (shows what was typed)
        self.expr_var = tk.StringVar(value="")
        self.expr_label = tk.Label(
            display_frame, textvariable=self.expr_var,
            font=FONT_EXPR, bg=BG_DISPLAY, fg="#6c7086",
            anchor="e", width=22
        )
        self.expr_label.pack(fill="x")

        # Main result / current number display
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Label(
            display_frame, textvariable=self.display_var,
            font=FONT_DISPLAY, bg=BG_DISPLAY, fg=FG_DISPLAY,
            anchor="e", width=22
        )
        self.display.pack(fill="x")

    # ── Button grid ────────────────────────────
    def _build_buttons(self):
        """
        Layout (row x col):
          Row 1: C   OFF  ^   %
          Row 2: 7   8    9   /    \\
          Row 3: 4   5    6   *    =
          Row 4: 1   2    3   -    =  (= spans rows 3-4 col 4)
          Row 5: 0(wide)  .   +
        """
        btn_frame = tk.Frame(self.root, bg=BG_MAIN)
        btn_frame.grid(row=1, column=0, padx=10, pady=(4, 10))

        # Helper to make a styled button
        def make_btn(parent, text, bg, fg, hover, cmd, **grid_kw):
            b = tk.Button(
                parent, text=text, font=FONT_BTN,
                bg=bg, fg=fg, activebackground=hover, activeforeground=fg,
                relief="flat", bd=0, cursor="hand2",
                width=4, height=2,
                command=cmd
            )
            b.bind("<Enter>", lambda e: b.config(bg=hover))
            b.bind("<Leave>", lambda e: b.config(bg=bg))
            b.grid(padx=4, pady=4, **grid_kw)
            return b

        # ── Row 1: Special / Operator row ──────
        make_btn(btn_frame, "C",   BTN_SPEC_BG, BTN_SPEC_FG, BTN_SPEC_HOVER, self.clear,       row=0, column=0)
        make_btn(btn_frame, "OFF", BTN_SPEC_BG, BTN_SPEC_FG, BTN_SPEC_HOVER, self.turn_off,    row=0, column=1)
        make_btn(btn_frame, "^",   BTN_OP_BG,   BTN_OP_FG,   BTN_OP_HOVER,   lambda: self.append_op("**"), row=0, column=2)
        make_btn(btn_frame, "%",   BTN_OP_BG,   BTN_OP_FG,   BTN_OP_HOVER,   lambda: self.append_op("%"),  row=0, column=3)
        make_btn(btn_frame, "⌫",  BTN_NUM_BG,  BTN_NUM_FG,  BTN_NUM_HOVER,  self.backspace,   row=0, column=4)

        # ── Row 2 ──────────────────────────────
        make_btn(btn_frame, "7", BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER, lambda: self.append_digit("7"), row=1, column=0)
        make_btn(btn_frame, "8", BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER, lambda: self.append_digit("8"), row=1, column=1)
        make_btn(btn_frame, "9", BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER, lambda: self.append_digit("9"), row=1, column=2)
        make_btn(btn_frame, "/", BTN_OP_BG,  BTN_OP_FG,  BTN_OP_HOVER,  lambda: self.append_op("/"),   row=1, column=3)
        make_btn(btn_frame, "\\",BTN_OP_BG,  BTN_OP_FG,  BTN_OP_HOVER,  lambda: self.append_op("//"),  row=1, column=4)

        # ── Row 3 ──────────────────────────────
        make_btn(btn_frame, "4", BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER, lambda: self.append_digit("4"), row=2, column=0)
        make_btn(btn_frame, "5", BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER, lambda: self.append_digit("5"), row=2, column=1)
        make_btn(btn_frame, "6", BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER, lambda: self.append_digit("6"), row=2, column=2)
        make_btn(btn_frame, "*", BTN_OP_BG,  BTN_OP_FG,  BTN_OP_HOVER,  lambda: self.append_op("*"),   row=2, column=3)

        # '=' button spans 2 rows
        eq_btn = tk.Button(
            btn_frame, text="=", font=FONT_BTN,
            bg=BTN_EQ_BG, fg=BTN_EQ_FG,
            activebackground=BTN_EQ_HOVER, activeforeground=BTN_EQ_FG,
            relief="flat", bd=0, cursor="hand2",
            width=4,
            command=self.evaluate
        )
        eq_btn.bind("<Enter>", lambda e: eq_btn.config(bg=BTN_EQ_HOVER))
        eq_btn.bind("<Leave>", lambda e: eq_btn.config(bg=BTN_EQ_BG))
        eq_btn.grid(row=2, column=4, rowspan=2, padx=4, pady=4, sticky="ns")

        # ── Row 4 ──────────────────────────────
        make_btn(btn_frame, "1", BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER, lambda: self.append_digit("1"), row=3, column=0)
        make_btn(btn_frame, "2", BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER, lambda: self.append_digit("2"), row=3, column=1)
        make_btn(btn_frame, "3", BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER, lambda: self.append_digit("3"), row=3, column=2)
        make_btn(btn_frame, "-", BTN_OP_BG,  BTN_OP_FG,  BTN_OP_HOVER,  lambda: self.append_op("-"),   row=3, column=3)

        # ── Row 5 ──────────────────────────────
        # 0 spans 2 columns
        zero_btn = tk.Button(
            btn_frame, text="0", font=FONT_BTN,
            bg=BTN_NUM_BG, fg=BTN_NUM_FG,
            activebackground=BTN_NUM_HOVER, activeforeground=BTN_NUM_FG,
            relief="flat", bd=0, cursor="hand2",
            height=2,
            command=lambda: self.append_digit("0")
        )
        zero_btn.bind("<Enter>", lambda e: zero_btn.config(bg=BTN_NUM_HOVER))
        zero_btn.bind("<Leave>", lambda e: zero_btn.config(bg=BTN_NUM_BG))
        zero_btn.grid(row=4, column=0, columnspan=2, padx=4, pady=4, sticky="ew")

        make_btn(btn_frame, ".", BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER, lambda: self.append_digit("."), row=4, column=2)
        make_btn(btn_frame, "+", BTN_OP_BG,  BTN_OP_FG,  BTN_OP_HOVER,  lambda: self.append_op("+"),   row=4, column=3)

        # Keyboard bindings
        self.root.bind("<Key>", self._on_key)

    # ── Actions ────────────────────────────────
    def _refresh_display(self, text: str):
        """Update the main display; trim very long strings."""
        text = str(text)
        if len(text) > 18:
            text = text[:18] + "…"
        self.display_var.set(text)

    def _display_expression(self, expr: str):
        """Update the small expression label, showing ^ and \\ instead of ** and //."""
        friendly = expr.replace("**", "^").replace("//", "\\")
        if len(friendly) > 28:
            friendly = "…" + friendly[-27:]
        self.expr_var.set(friendly)

    def append_digit(self, digit: str):
        if self.just_evaluated:
            # Start fresh after an evaluation
            self.expression = ""
            self.just_evaluated = False
        self.expression += digit
        self._refresh_display(self.expression.replace("**", "^").replace("//", "\\"))
        self._display_expression(self.expression)

    def append_op(self, op: str):
        self.just_evaluated = False
        if self.expression and self.expression[-1] in "+-*/%\\":
            # Replace last operator instead of doubling up
            self.expression = self.expression[:-1]
        # Handle ** and // trailing chars
        if self.expression.endswith("*") or self.expression.endswith("/"):
            self.expression = self.expression[:-1]
        self.expression += op
        self._refresh_display(self.expression.replace("**", "^").replace("//", "\\"))
        self._display_expression(self.expression)

    def evaluate(self):
        if not self.expression:
            return
        try:
            # Safety: only allow mathematical characters
            safe_expr = self.expression
            result = eval(safe_expr)   # evaluate the expression

            # Format nicely: avoid trailing .0 for whole numbers
            if isinstance(result, float) and result.is_integer():
                result_str = str(int(result))
            else:
                result_str = str(round(result, 10)).rstrip("0").rstrip(".")

            self._display_expression(self.expression + " =")
            self._refresh_display(result_str)
            self.expression = result_str
            self.just_evaluated = True

        except ZeroDivisionError:
            self._refresh_display("Div by 0!")
            self.expression = ""
        except Exception:
            self._refresh_display("Error")
            self.expression = ""

    def clear(self):
        self.expression = ""
        self.just_evaluated = False
        self._refresh_display("0")
        self.expr_var.set("")

    def backspace(self):
        if self.just_evaluated:
            self.clear()
            return
        # Handle multi-char operators (** and //)
        if self.expression.endswith("**") or self.expression.endswith("//"):
            self.expression = self.expression[:-2]
        else:
            self.expression = self.expression[:-1]
        display = self.expression.replace("**", "^").replace("//", "\\")
        self._refresh_display(display if display else "0")
        self._display_expression(self.expression)

    def turn_off(self):
        self.root.destroy()

    def _on_key(self, event):
        """Allow keyboard input."""
        key = event.char
        if key in "0123456789.":
            self.append_digit(key)
        elif key in "+-*/%":
            self.append_op(key)
        elif key == "^":
            self.append_op("**")
        elif key in ("\r", "\n", "="):
            self.evaluate()
        elif event.keysym == "BackSpace":
            self.backspace()
        elif key.lower() == "c":
            self.clear()


# ──────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
