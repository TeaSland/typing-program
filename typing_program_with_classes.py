"""This program has 4 different levels for users who type at different levels.

All levels include space. Level 1 is only the home row, or the middle row.
Level 2 is all the letter keys with the apostrophe. Level 3 is the number keys
as well as the right hand side letters. Level 4 is using shift and caps lock
"""
import tkinter as tk
import tkinter.ttk as ttk
from random import randint
from keyboard import block_key
from stopwatch import Stopwatch

MAX_CHARS = 25


class Frame:
    """Creates a frame widget."""

    def __init__(self, root, hlbg, hlth, row, col, rspan, cspan, padx, pady):
        """Create the frame based on the parameter given."""
        self._root = root
        self._hlbg = hlbg

        self._hlthickness = hlth
        self._row = row
        self._col = col
        self._rspan = rspan
        self._cspan = cspan
        self._padx = padx
        self._pady = pady

        self.frm = tk.Frame(self._root, highlightbackground=self._hlbg,
                            highlightthickness=self._hlthickness)
        self.frm.grid(row=self._row, columnspan=self._cspan, column=self._col,
                      rowspan=self._rspan, pady=self._pady, padx=self._padx)


class Label:
    """Creates a label."""

    def __init__(self, frame, width, col, row, rspan, cspan, padx, pady, anch):
        """Create a label based on the parameters given."""
        self._frame = frame
        self._var = tk.StringVar()
        self._width = width
        self._anchor = anch
        self._col = col
        self._row = row
        self._rspan = rspan
        self._cspan = cspan
        self._padx = padx
        self._pady = pady

        self._label = ttk.Label(self._frame, textvariable=self._var,
                                width=self._width, anchor=self._anchor)
        self._grid()

    def _grid(self):
        """Grid the label."""
        self._label.grid(column=self._col, row=self._row,
                         rowspan=self._rspan, columnspan=self._cspan,
                         padx=self._padx, pady=self._pady)

    def get_var(self):
        """get the value of the variable."""
        return self._var.get()

    def set_var(self, text):
        """Set the textvariable."""
        self._var.set(text)

    def set_text(self, text):
        """attache text to a label."""
        self._label.destroy()
        self._label = ttk.Label(self._frame, text=text, width=self._width)
        self._grid()

    def set_wraplength(self, length):
        """If the label needs wraplength instead of width."""
        self._label.destroy()
        self._label = ttk.Label(self._frame, textvariable=self._var,
                                wraplength=length)
        self._grid()

    def set_font(self, font, size):
        """Set the font and font size of the label."""
        self._label.configure(font=(font, size))


class Button:
    """Creates a button widget."""

    def __init__(self, root, col, row, cspan, rspan, command):
        """Create a button based on the parameters given."""
        self._root = root
        self._col = col
        self._row = row
        self._cspan = cspan
        self._rspan = rspan
        self._command = command
        self._var = tk.StringVar()

        self.button = ttk.Button(self._root, textvariable=self._var,
                                 command=self._command)
        self.button.grid(row=self._row, column=self._col, rowspan=self._rspan,
                         columnspan=self._cspan)

    def get_var(self):
        """get the value of the variable."""
        return self._var.get()

    def set_text(self, text):
        """change textvariable to text."""
        self.button.destroy()
        self.button = ttk.Button(self._root, text=text, command=self._command)
        self.button.grid(row=self._row, column=self._col, rowspan=self._rspan,
                         columnspan=self._cspan)

    def set_var(self, text):
        """Set the text variable."""
        self._var.set(text)

    def set_state(self, state):
        """set the state of the button to normal or disabled."""
        self.button.configure(state=state)


class Text:
    """Creates a textwidget."""

    def __init__(self, root, height, width, bgcolor, wrap, row, col, rspan,
                 cspan, padx, pady):
        """Create a text widget based on the parameters given."""
        self._root = root
        self._height = height
        self._width = width
        self._bgcolor = bgcolor
        self._wrap = wrap
        self._row = row
        self._col = col
        self._rspan = rspan
        self._cspan = cspan
        self._padx = padx
        self._pady = pady

        self._text = tk.Text(self._root, height=self._height, bg=self._bgcolor,
                             wrap=self._wrap, width=self._width)
        self._text.grid(padx=self._padx, column=self._col, rowspan=self._rspan,
                        columnspan=self._cspan, row=self._row, pady=self._pady)

    def get_str(self, start, end):
        """Get the entry of the text box."""
        return self._text.get(start, end)

    def set_state(self, state):
        """Set the state of the widget."""
        self._text.configure(state=state)

    def set_focus(self):
        """Put the cursor into the text widget."""
        self._text.focus_set()

    def insert_text(self, where, what):
        """Add text to the text widget."""
        self._text.insert(where, what)

    def delete_text(self, start, end):
        """Delete the text within the window."""
        self._text.delete(start, end)

    def block_selecting(self):
        """Stop the user from selecting the text in the widget."""
        self._text.bindtags((str(self._text), str(self._root), "all"))

    def underline_character(self, char):
        """Underline the character char."""
        self._text.tag_add('underline', f"1.{char}", f"1.{char + 1}")
        self._text.tag_configure('underline', underline=1)

    def set_font(self, font, size):
        """Set the font and the font size."""
        self._text.configure(font=(font, size))

    def set_relief(self, relief):
        """Set the relief of the text widget."""
        self._text.configure(relief=relief)


class SettingUp:
    """Set up the widgets, get the username and set up the keycodes."""

    WELCOME = "Welcome to my typing program. Here you have 4 different " \
              "levels. Levels 2 to 4 include capitalizing 'i'. Level 1 is " \
              "only the middle row. The 2nd level is all the letter keys. " \
              "Level 3 is the right hand side keys as well as number keys. " \
              "Lastly, is level 4, which uses shift and caps lock. To " \
              "start you need to press the start button. This will start" \
              " the timer. The timer will only stop when you've got " \
              "everything correct. Note: if it starts underlining, it means" \
              " you've pressed a wrong character."
    LEVELS = ["1", "2", "3", "4"]

    def __init__(self):
        """Set everything up then starts the program."""
        self._root = tk.Tk()
        self._root.title("Typing Speed Test")

        self._name = self._getting_name()
        self._keycodes = self._inserting_chars()
        self._texts = self._getting_files('texts')

        self._correct = 0  # The amount that the user typed correctly
        self._total_typed = 0  # The total amount of characters typed
        self._level_chosen = None

        self._welcome_frame = Frame(self._root, "black", 1, 0, 0, 1, 4, 2, 2)
        self._level_frame = Frame(self._root, 'black', 1, 1, 0, 1, 2, 2, 2)
        self._time_frame = Frame(self._root, 'black', 1, 1, 2, 1, 2, 2, 2)
        self._text_frame = Frame(self._root, 'black', 1, 2, 0, 1, 4, 2, 2)
        self._results_frame = Frame(self._root, 'black', 1, 4, 0, 2, 2, 2, 2)
        self._show_frame = Frame(self._root, 'black', 1, 6, 0, 1, 4, 2, 2)

        # This is just a welcome to the program
        self._welcome_label = Label(self._welcome_frame.frm, 0, 0, 0, 1, 4, 0,
                                    0, tk.CENTER)
        self._welcome_label.set_wraplength(750)
        self._welcome_label.set_var(f"Hello. {SettingUp.WELCOME}")
        self._welcome_label.set_font("Courier", 10)

        # Label with menu to make it clear that I'm asking for the level
        self._level_label = Label(self._level_frame.frm, '10c', 0, 0, 1, 1, 0,
                                  0, tk.CENTER)
        self._level_label.set_var("Which level?")

        # Is where the user can choose which level he/she wants
        self._chosen_level = tk.StringVar()
        self._level_menu = tk.OptionMenu(self._level_frame.frm,
                                         self._chosen_level, *SettingUp.LEVELS)
        self._level_menu.grid(row=0, column=1)
        self._chosen_level.set(1)

        # Is the button that will start the time and gets a text
        self._start_button = Button(self._time_frame.frm, 0, 0, 1, 1,
                                    self.resetting)
        self._start_button.set_text("Start")

        # Sets up the timer label
        self._timer_label = Label(self._time_frame.frm, 20, 1, 0, 1, 1, 0, 0,
                                  'e')

        # Setting up the text label
        self._show_text = Text(self._text_frame.frm, 9, 88, '#f0f0ed', 'word',
                               0, 0, 1, 4, 0, 0)
        self._show_text.set_font("Courier", 10)
        self._show_text.set_relief('flat')
        self._show_text.block_selecting()

        # Sets up the text widget for user input.
        self._user_text = Text(self._root, 8, 90, 'white', 'word', 3, 0, 1, 4,
                               5, 5)
        self._user_text.insert_text(tk.END, "Type here when you press Start")
        self._user_text.set_state("disabled")

        # Here are the results and show_highscore button set up
        self._results_label = Label(self._results_frame.frm, 10, 0, 0, 2, 1,
                                    0, 0, tk.CENTER)
        self._results_label.set_var("Results: ")

        self._wpm_label = Label(self._results_frame.frm, 20, 1, 0, 1, 1, 0, 0,
                                tk.CENTER)
        self._wpm_label.set_var("WPM: ")

        self._accuracy_label = Label(self._results_frame.frm, 20, 1, 1, 1, 1,
                                     0, 0, tk.CENTER)
        self._accuracy_label.set_var("Accuracy: ")

        self._hs_button = Button(self._root, 3, 4, 1, 2, self._show_scores)
        self._hs_button.set_var("Show High Scores")

        # Blocks keys that crash the program or allows the user to cheat
        block_key('control')
        block_key('enter')
        block_key('alt')

        # Ensures that the label is on 0 upon starting the program
        self._stopwatch = Stopwatch()
        self._stopwatch.stop()
        self._stopwatch.reset()

        self._root.bind("<KeyPress>", self._key_pressed)

        self._update_time()

        self._root.lift()
        self._root.mainloop()

    def _getting_name(self):
        """Ask for a username and returns the value."""
        name = ""

        while name == "" or len(name) > MAX_CHARS:
            name = input("What would is your username to be? It has to be "
                         "something but shorter than 25 character: ").strip()
            if len(name) > MAX_CHARS:
                print('Please enter a username with less than 26 characters.')
            elif name == "":
                print("Please enter a username with characters.")

        return name.capitalize()

    def _inserting_chars(self):
        """These are the numbers for the chars the user will type."""
        keycodes = [32]  # Is space

        for i in range(48, 58):  # Keycodes for the numbers and their symbols
            keycodes.append(i)

        for i in range(65, 91):  # Keycodes for the letters a to z
            keycodes.append(i)

        for i in range(96, 112):  # Keycodes on the number pad.
            keycodes.append(i)

        for i in range(186, 223):  # Keycodes right of all the letters i.e [
            keycodes.append(i)

        return keycodes

    def _getting_files(self, file):
        """Get a file that then splits it into 2D lists."""
        with open(file) as f:
            data = f.read()
            data = list(data.split('\n\n'))

        for i in range(len(data)):
            data[i] = list(data[i].split('\n'))

        return data

    def resetting(self):
        """Button function. Start timer + clear labels + display the text."""
        self._stopwatch.restart()

        # Resets the textbox and focuses on it
        self._user_text.set_state('normal')
        self._user_text.delete_text(1.0, tk.END)
        self._user_text.set_focus()

        # Resetting variables and results
        self._total_typed = 0
        self._correct = 0
        self._wpm_label.set_var("WPM: ")
        self._accuracy_label.set_var("Accuracy: ")

        # Resetting the high score window and button
        self._hs_button.set_var("Show High Scores")
        self._hs_button.set_state('disabled')
        self._show_frame.frm.destroy()
        self._show_frame = Frame(self._root, 'black', 1, 7, 0, 1, 5, 2, 2)

        # Gets the chosen level and displays it.
        self._level_chosen = int(self._chosen_level.get())
        self._show_text.delete_text(1.0, tk.END)
        self._show_text.insert_text(tk.END, self._texts[self._level_chosen - 1]
                                                       [randint(0, 2)])

    def _key_pressed(self, event):
        """Register if key pressed is part of program + checks for mistakes."""
        chars = list(self._show_text.get_str(1.0, 'end-1c'))
        user = list(self._user_text.get_str(1.0, 'end-1c'))
        num_char = len(user) - 1  # indexing

        if event.keycode in self._keycodes:
            self._total_typed += 1
            try:
                if event.char != chars[num_char]:
                    self._show_text.underline_character(num_char)
                elif event.char == chars[num_char]:
                    self._correct += 1
            except IndexError:  # If the user types too much.
                pass

    def _results(self, typed, text, time):
        """It will calculate the wpm and accuracy."""
        words = len(text) / 5  # Calculates the average amount of words
        wpm = round(words / (time / 60),
                    2)  # time into min from sec then round
        wpm = f'{wpm} wpm'
        self._wpm_label.set_var(f"WPM: {wpm}")

        accuracy = round(self._correct / typed * 100, 2)
        accuracy = f"{accuracy}%"
        self._accuracy_label.set_var(f"Accuracy: {accuracy}")

        return wpm, accuracy

    def _update_scores(self, wpm, accuracy):
        """It will import a file and check for accuracy and wpm."""
        scores = self._getting_files("high_scores")
        not_on = True

        for i in range(len(scores)):
            # Ignores first line. Than it checks for the accuracy and the wpm.
            if i != 0 and not_on and (accuracy > scores[i][2] or
                                      (wpm > (scores[i][3]) and
                                       accuracy == scores[i][2])):
                scores.insert(i, [f"{i+1}", self._name, str(accuracy),
                                  str(wpm), str(self._level_chosen)])
                del scores[-1]  # deletes the last item
                not_on = False

        for i in range(len(scores)):
            if i != 0:
                scores[i][0] = f'{i}.'  # first item is the right number
            scores[i] = "\n".join(scores[i])

        scores = "\n\n".join(scores)

        with open("high_scores", "w") as f:
            f.write(scores)

    def _show_scores(self):
        """Make the high scores appear."""
        if self._hs_button.get_var() == "Show High Scores":
            self._hs_button.set_var("Hide High Scores")
            high_scores = self._getting_files('high_scores')
            for i in range(len(high_scores)):
                for j in range(len(high_scores[i])):
                    frame = Frame(self._show_frame.frm, 'black', 1, i, j, 1,
                                  1, 0, 0)
                    label = Label(frame.frm, 20, 0, 0, 1, 1, 0, 0, tk.CENTER)
                    label.set_text(high_scores[i][j])

        else:
            self._hs_button.set_var("Show High Scores")
            self._show_frame.frm.destroy()
            self._show_frame = Frame(self._root, 'black', 1, 6, 0, 1, 5, 2, 2)

    def _update_time(self):
        """Keep updating the time."""
        if self._user_text.get_str(1.0, 'end-1c') == \
                self._show_text.get_str(1.0, 'end-1c'):
            self._stopwatch.stop()
            wpm, accuracy = self._results(self._total_typed, self._user_text.
                                          get_str(1.0, 'end-1c'),
                                          self._stopwatch.duration)
            self._update_scores(wpm, accuracy)
            self._hs_button.set_state('normal')

            # Ensures that the results don't keep updating
            self._user_text.insert_text(tk.END, " ")
            self._user_text.set_state("disabled")

        self._timer_label.set_var(self._stopwatch)
        self._root.after(10, self._update_time)


typing_program = SettingUp()
