import tkinter as tk
import math

LARGE_FONT_STYLE = ("Great Vibes", 30, "bold")
SMALL_FONT_STYLE = ("Great Vibes", 16)
DIGITS_FONT_STYLE = ("Great Vibes", 24, "bold")
DEFAULT_FONT_STYLE = ("Great Vibes", 20)

BLACK = '#000000'
OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"


class Calculator:
    def __init__(self) -> None:
        self.window = tk.Tk()  # conventional syntax
        self.window.title("Calculator")
        self.window.geometry("400x600")  # window size
        self.window.resizable(0, 0)  # cant resize the window anymore

        self.curr = ""
        self.total = ""

        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for i in range(1, 5):
            self.buttons_frame.rowconfigure(i, weight=1)
            self.buttons_frame.columnconfigure(i, weight=1)

        self.total_label, self.curr_label = self.create_display_labels()
        #self.curr_label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),         # -----------> row
            4: (2, 1), 5: (2, 2), 6: (2, 3),         # |
            1: (3, 1), 2: (3, 2), 3: (3, 3),         # |
            0: (4, 2), '.': (4, 1)                   # column
        }

        self.operations = {
            "/": "\u00F7",
            "*": "\u00D7",
            "-": "-",
            "+": "+"
        }

        self.create_buttons()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event,
                             digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event,
                             operator=key: self.append_operator(operator))

    def create_display_frame(self):
        ''' FRAME FUNCTION SYNTAX (frame and pack)
        ---------------------------------------------
        Frame(master, options)
        master = parent window
        options include: bg, bd(boder size), cursor (cursor changes pattern when it hovers),
        height, highlightbackground, highlightcolor, highlightthickness, relief, width

        FRAME.PACK()
        ----------------------------------
        arguments: expand, fill, side
        expand: When set to true, widget expands to fill any space not used in widget's parent
        fill: Determines whether widget fills any extra space allocated to it by the packer, or keeps its own minimal dimensions:
              NONE (default), X (fill only horizontally), Y (fill only vertically), or BOTH (fill both horizontally and vertically)'''

        frame = tk.Frame(self.window, height=221, bg=BLACK)
        frame.pack(expand=True, fill='both')
        return frame

    def create_buttons_frame(self):  # same syntax as
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill='both')
        return frame

    def create_display_labels(self):
        ''' LABEL FUNCTION SYNTAX 
        ---------------------------------------------
        Label(master, options)
        master = parent window
        options include: anchor(east, west, n, s directions thing), bg, bitmap(used to display a graphic),
                         bd, cursor, font, fg(specifices color of text(font) or bitmap), height,
                         image(used to display a static image), justify(left, right, center), 
                         padx(Extra space added to the left and right of the text within the widget. Default is 1),
                         pady(same as padx but above and below), relief(realtes to appearance of decorative boders), 
                         text(used to display 1+ lines of text), textvariable, underline, width, wraplength'''

        total_label = tk.Label(self.display_frame, text=self.total,
                               anchor=tk.E, bg=BLACK, fg=WHITE, padx=24, font=SMALL_FONT_STYLE)  # tk.E = east
        total_label.pack(expand=True, fill='both')

        curr_label = tk.Label(self.display_frame, text=self.total,
                              anchor=tk.E, bg=BLACK, fg=WHITE, padx=24, font=LARGE_FONT_STYLE)  # tk.E = east
        curr_label.pack(expand=True, fill='both')

        return total_label, curr_label

    def add_to_expression(self, val):
        self.curr += str(val)
        self.update_curr_label()

    def create_digit_buttons(self):
        ''' BUTTON FUNCTION SYNTAX (button and grid)
        ---------------------------------------------
        Label(master, options)
        master = parent window
        options include: column, columnspan, ipadx, ipady, padx, pady, row, rowspan, sticky'''
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(
                digit), bg=LABEL_COLOR, fg=WHITE, font=DIGITS_FONT_STYLE, borderwidth=2, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0],
                        column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.curr += operator
        self.total += self.curr
        self.curr = ""
        self.update_total_label()
        self.update_curr_label()

    def create_operator_buttons(self):
        i = 1
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=2, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.curr = ""
        self.total = ""
        self.update_curr_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text='C', bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=2, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.curr = str(math.pow(eval(self.curr), 2))
        self.update_curr_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=2, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def square_root(self):
        self.curr = str(math.sqrt(eval(self.curr)))
        self.update_curr_label()

    def create_square_root_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=2, command=self.square_root)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def pi(self):
        self.curr = str(eval(self.curr) * math.pi)
        self.update_curr_label()

    def create_pi_button(self):
        button = tk.Button(self.buttons_frame, text="\u03C0", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=2, command=self.pi)
        button.grid(row=0, column=4, sticky=tk.NSEW)

    def evaluate(self):
        self.total += self.curr
        self.update_total_label()

        try:
            self.curr = str(eval(self.total))
            self.total = ""

        except Exception as ex:
            self.curr = "Error"
        finally:
            self.update_curr_label()

    def create_equal_button(self):
        button = tk.Button(self.buttons_frame, text='=', bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=2, command=self.evaluate)
        button.grid(row=4, column=3, sticky=tk.NSEW)

    def create_buttons(self):
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_clear_button()
        self.create_equal_button()
        self.create_square_button()
        self.create_square_root_button()
        self.create_pi_button()

    def update_total_label(self):
        expression = self.total
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=self.total)

    def update_curr_label(self):
        self.curr_label.config(text=self.curr[:20])

    def run(self):  # program wont run w/o mainloop
        self.window.mainloop()


if __name__ == "__main__":  # when running python file as a script, __name__ is always __main__
    calc = Calculator()  # run program using classes syntax
    calc.run()
