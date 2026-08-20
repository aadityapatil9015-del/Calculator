import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt


class Calculators(QWidget):
    def __init__(self):
        super().__init__()
        self.result = 0
        self.grid = QGridLayout()
        self.num_label = QLabel(self)
        self.button_num = {}
        self.button_operator = {}
        self.button_miscellaneous = {}
        self.button_spec_op = {}
        self.button_equal = {}
        self.reset_label = False
        self.buffer = ""
        self.setFocusPolicy(Qt.StrongFocus)
        self.history_list = []
        self.open_bracket = 0
        self.closed_bracket = 0
        self.history_index = 0
        self.op_limit = 0
        self.final_result = 0
        self.Theme = QPushButton("☀️ Light", self)
        self.theme_counter = 0
        self.op_lt = []
        self.spec_lt = []
        self.Theme.setObjectName("ThemeButton")
        self.black_ui = """
                QWidget {
                background-color:hsl(217, 4%, 24%);
                }

                QLabel {
                background-color:hsl(217, 4%, 24%);
                color:hsl(216, 1%, 87%);
                font-weight:bold;
                font-size :40px;
                padding-right: 0px 8px 0px 0px;
                border: 5px solid hsl(217, 4%, 10%);
                border-radius: 10px;
                }

                QPushButton {
                background-color:hsl(217, 4%, 34%);
                font-size: 35px;
                color: hsl(216, 1%, 87%);
                font-weight:bold;
                border-radius:10px;
                }

                QPushButton:hover {
                background-color:hsl(217, 4%, 44%);
                }

                QPushButton:pressed {
                background-color:hsl(217, 4%, 64%);
                }

                QPushButton#ThemeButton{
                font-size: 10px;
                background-color: hsl(217,4%,30%);
                color: hsl(216,1%,80%);
                padding: 0px 8px;
                border: 5px solid hsl(217,4%,15%);
                border-radius: 10px;
                }
                QPushButton#ThemeButton:hover {
                background-color: hsl(217,4%,40%)
                }
                QPushButton#ThemeButton:pressed {
                background-color: hsl(217,4%,35%)
                }
                """
        self.white_ui = """
                QWidget {
                background-color:hsl(217, 24%, 74%);
                }

                QLabel {
                background-color:hsl(217, 22%, 74%);
                color:hsl(216, 1%, 13%);
                font-weight:bold;
                font-size :40px;
                padding-right: 0px 8px 0px 0px;
                border: 5px solid hsl(200, 34%, 55%);
                border-radius: 10px;
                }

                QPushButton {
                background-color:hsl(217, 4%, 66%);
                font-size: 35px;
                color: hsl(216, 1%, 13%);
                font-weight:bold;
                border-radius:10px;
                }

                QPushButton:hover {
                background-color:hsl(217, 4%, 56%);
                }

                QPushButton:pressed {
                background-color:hsl(217, 4%, 46%);
                }

                QPushButton#ThemeButton{
                font-size: 10px;
                background-color: hsl(217,4%,65%);
                color: hsl(216,1%,25%);
                padding: 0px 8px;
                border: 5px solid hsl(217,4%,50%);
                border-radius: 10px;
                }
                QPushButton#ThemeButton:hover {
                background-color: hsl(217,4%,80%)
                }
                QPushButton#ThemeButton:pressed {
                background-color: hsl(217,4%,55%)
                }
                """

        for i in range(10):
            self.button_num[str(i)] = QPushButton(str(i), self)
        operators = ["+", "-", "×", "÷", "=", ".", "(", ")"]
        for op in operators:
            if op in ("+", "-", "×", "÷"):
                self.button_operator[op] = QPushButton(op, self)
                self.op_lt.append(op)
            elif op == "=":
                self.button_equal[op] = QPushButton(op, self)
            else:
                self.button_spec_op[op] = QPushButton(op, self)
                self.spec_lt.append(op)

        special_operators = ["C", "ANS", "⌫", "AC"]
        for spec_op in special_operators:
            self.button_miscellaneous[spec_op] = QPushButton(spec_op, self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Calculator")
        self.setGeometry(600, 400, 400, 400)
        self.grid.addWidget(self.num_label, 1, 0, 1, 5)
        self.grid.addWidget(self.button_miscellaneous["AC"], 2, 0)
        self.grid.addWidget(self.button_miscellaneous["C"], 2, 1)
        self.grid.addWidget(self.button_spec_op["("], 2, 2)
        self.grid.addWidget(self.button_spec_op[")"], 2, 3)
        self.grid.addWidget(self.button_miscellaneous["⌫"], 2, 4)
        self.grid.addWidget(self.button_num["7"], 3, 0)
        self.grid.addWidget(self.button_num["8"], 3, 1)
        self.grid.addWidget(self.button_num["9"], 3, 2)
        self.grid.addWidget(self.button_operator["+"], 3, 3)
        self.grid.addWidget(self.button_num["4"], 4, 0)
        self.grid.addWidget(self.button_num["5"], 4, 1)
        self.grid.addWidget(self.button_num["6"], 4, 2)
        self.grid.addWidget(self.button_operator["-"], 4, 3)
        self.grid.addWidget(self.button_num["1"], 5, 0)
        self.grid.addWidget(self.button_num["2"], 5, 1)
        self.grid.addWidget(self.button_num["3"], 5, 2)
        self.grid.addWidget(self.button_operator["×"], 5, 3)
        self.grid.addWidget(self.button_miscellaneous["ANS"], 6, 0)
        self.grid.addWidget(self.button_num["0"], 6, 1, )
        self.grid.addWidget(self.button_spec_op["."], 6, 2)
        self.grid.addWidget(self.button_operator["÷"], 6, 3)
        self.grid.addWidget(self.button_equal["="], 3, 4, 4, 1)
        self.grid.addWidget(self.Theme, 0, 4)
        self.num_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.num_label.setFixedHeight(60)
        total_buttons = []
        for i in range(len(self.button_num)):
            total_buttons.append(self.button_num[str(i)])
        for op in self.button_operator:
            total_buttons.append(self.button_operator[op])
        for miss in self.button_miscellaneous:
            total_buttons.append(self.button_miscellaneous[miss])
        for spec_op in self.button_spec_op:
            total_buttons.append(self.button_spec_op[spec_op])
        total_buttons.append(self.button_equal["="])
        for button in total_buttons:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setFocusPolicy(Qt.NoFocus)

        self.setStyleSheet(self.black_ui)
        self.setLayout(self.grid)
        for num in self.button_num:
            self.button_num[num].clicked.connect(self.button_clicked)

        for op in self.button_operator:
            self.button_operator[op].clicked.connect(self.button_clicked)

        self.button_equal["="].clicked.connect(self.print_result)

        self.Theme.clicked.connect(self.change_theme)

        for spec_op in self.button_spec_op:
            self.button_spec_op[spec_op].clicked.connect(self.button_clicked)
        for miss in self.button_miscellaneous:
            self.button_miscellaneous[miss].clicked.connect(self.spec_button_clicked)

    def button_clicked(self):
        button_pressed = self.sender()
        assert isinstance(button_pressed, QPushButton)
        self.handle_input_normal(button_pressed.text())

    def keyPressEvent(self, event):
        keybind_pressed = event.text()
        if keybind_pressed.isdigit() or keybind_pressed in ("+", "-"):
            self.handle_input_normal(keybind_pressed)
        elif keybind_pressed == "*":
            self.handle_input_normal("×")
        elif keybind_pressed == "/":
            self.handle_input_normal("÷")
        elif keybind_pressed == '.':
            self.handle_input_normal(".")
        elif keybind_pressed == "=" or event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.print_result()
        elif event.key() == Qt.Key_Backspace:
            self.handle_input_spec("⌫")
        elif event.key() == Qt.Key_Left:
            self.history_index -= 1
            self.display_history()
        elif event.key() == Qt.Key_Right:
            self.history_index += 1
            self.display_history()
        elif keybind_pressed.isalpha():
            self.buffer += keybind_pressed
            if self.buffer.capitalize() == "C":
                self.handle_input_spec("C")
                self.buffer = ""
            elif self.buffer.upper() == "ANS":
                self.handle_input_spec("ANS")
                self.buffer = ""
        elif event.key() == Qt.Key_ParenLeft:
            self.handle_input_normal("(")
            self.buffer = ""
        elif event.key() == Qt.Key_ParenRight:
            self.handle_input_normal(")")
            self.buffer = ""

    def calc_operations(self, list_nums, list_operators):
        i = 0
        while i < len(list_operators):
            if list_operators[i] in ("×", "÷"):
                number1 = list_nums[i]
                number2 = list_nums[i + 1]
                math_op = list_operators[i]
                if math_op == "×":
                    result = number1 * number2
                else:
                    try:
                        result = number1 / number2

                    except ZeroDivisionError:
                        self.num_label.setText("Division by zero")
                        self.reset_label = True
                        return None
                list_nums[i + 1] = result
                list_nums.pop(i)
                list_operators.pop(i)
            else:
                i += 1
        for i in range(len(list_operators)):
            number1 = list_nums[i]
            number2 = list_nums[i + 1]
            math_op = list_operators[i]
            if math_op == "+":
                result = number1 + number2
            elif math_op == "-":
                result = number1 - number2
            else:
                print("Invalid math operation/ bug occurred")
            list_nums[i + 1] = result
        self.result = list_nums[-1]
        return self.result

    def get_num_result(self, string):
        if not string:
            return None
        num_list = []
        op_list = []
        num_to_append = ""
        is_dot_encountered = False
        is_first_num_negative = False
        is_negative_num = False
        updated_string = string
        string_index = 0
        if string[0] == "-":
            is_first_num_negative = True
            updated_string = string[1:]
            string_index = 1
        for char in updated_string:
            if char.isdigit() and not is_dot_encountered:
                num_to_append += char
            elif char == '.':
                is_dot_encountered = True
                num_to_append += "."
            elif char.isdigit() and is_dot_encountered:
                num_to_append += char
            elif char.isalpha():
                num_to_append += char
            elif char in self.op_lt:
                if char == "-" and self.check_unary_minus(updated_string, string_index):
                    is_negative_num = True
                else:
                    op_list.append(char)
                    if num_to_append == "ANS":
                        num_list.append(self.final_result)

                    elif is_dot_encountered:
                        num_list.append(float(num_to_append))
                    elif not is_dot_encountered:
                        num_list.append(int(num_to_append))
                    if is_negative_num:
                        num_list[-1] = num_list[-1] * (-1)
                        is_negative_num = False
                    num_to_append = ""
                    is_dot_encountered = False
            string_index += 1

        if num_to_append:
            if num_to_append == "ANS":
                num_list.append(self.final_result)
            elif not is_dot_encountered:
                num_list.append(int(num_to_append))
            elif is_dot_encountered:
                num_list.append(float(num_to_append))

        if is_negative_num:
            num_list[-1] = -num_list[-1]
        if is_first_num_negative:
            if not num_list:
                return None
            num_list[0] = num_list[0] * (-1)
        if len(num_list) == len(op_list) + 1:
            no_error = self.calc_operations(num_list, op_list)
            if no_error is not None:
                return self.result
            else:
                return None
        else:
            return None

    def isDot_inNum(self, string):
        for r_str in reversed(string):
            if r_str == '.':
                return True
            elif r_str in "+-×÷":
                return False
        return False

    def spec_button_clicked(self):
        spec_button_pressed = self.sender()
        assert isinstance(spec_button_pressed, QPushButton)
        self.handle_input_spec(spec_button_pressed.text())

    def handle_input_normal(self, string_passed):
        new_string = string_passed
        current_label = self.num_label.text()
        new_label = ""
        is_dot_used = self.isDot_inNum(current_label)

        if self.reset_label:
            self.clear_label(new_string, current_label)
            return

        if not current_label:  # label is empty
            if new_string.isdigit():
                new_label = new_string
            elif new_string == "-":
                new_label = new_string
                self.op_limit += 1
            elif new_string in self.spec_lt:
                if new_string == "(":
                    self.open_bracket += 1
                    new_label = new_string
                elif new_string == ".":
                    new_label = str("0.")
                else:
                    new_label = ""
            else:
                new_label = ""
        elif current_label == "ANS":
            if new_string in self.op_lt:
                if self.can_add_ops(new_string):
                    new_label = current_label + new_string
                    self.op_limit += 1
                else:
                    new_label = current_label
            elif new_string == "(":
                new_label = current_label + "×" + new_string
                self.open_bracket += 1
                self.op_limit = 0
            elif new_string.isdigit():
                new_label = current_label + "×" + new_string
                self.op_limit = 0
            else:
                new_label = current_label

        else:
            last_string = current_label[-1]

            if last_string == ".":
                if new_string.isdigit():
                    new_label = current_label + new_string
                elif new_string in self.op_lt:
                    new_label = current_label[:-1] + new_string
                    self.op_limit += 1
                elif new_string == "(":
                    new_label = current_label + "×("
                else:
                    new_label = current_label

            elif last_string == "(":
                if new_string.isdigit():
                    new_label = current_label + new_string
                    self.op_limit = 0
                elif new_string == '.':
                    new_label = current_label + str("0.")
                    self.op_limit = 0
                elif new_string in self.op_lt:
                    if new_string == "-":
                        new_label = current_label + new_string
                        self.op_limit += 1
                    else:
                        new_label = current_label
                elif new_string == "(":
                    new_label = current_label + '('
                    self.open_bracket += 1
                    self.op_limit = 0
                else:
                    new_label = current_label

            elif last_string in self.op_lt:

                if not self.has_previous_value(current_label):
                    if new_string.isdigit():
                        new_label = current_label + new_string
                        self.op_limit = 0
                    elif new_string == "(":
                        new_label = current_label + str("(")
                        self.open_bracket += 1
                        self.op_limit = 0
                    elif new_string == '.':
                        if not is_dot_used:
                            new_label = current_label + str('0.')
                            self.op_limit = 0
                        elif is_dot_used:
                            new_label = current_label
                    elif new_string in self.op_lt:
                        if self.can_add_ops(new_string):
                            new_label = current_label + new_string
                            self.op_limit += 1
                        elif self.op_limit ==1 :
                            new_label = current_label[:-1] + new_string
                        else:
                            new_label = current_label

                else:
                    new_label = current_label

            elif last_string == ")":
                if self.has_previous_value(current_label):

                    if new_string.isdigit():
                        new_label = current_label + "×" + new_string
                        self.op_limit = 0

                    elif new_string == ".":
                        new_label = current_label + "×0."
                        self.op_limit = 0

                    elif new_string in self.op_lt:
                        if self.can_add_ops(new_string):
                            new_label = current_label + new_string
                            self.op_limit += 1
                        else:
                            new_label = current_label

                    elif new_string == "(":
                        new_label = current_label + "×("
                        self.open_bracket += 1
                        self.op_limit = 0

                    elif new_string == ")":
                        if self.open_bracket > self.closed_bracket:
                            new_label = current_label + ")"
                            self.closed_bracket += 1
                        else:
                            new_label = current_label

                    else:
                        new_label = current_label

                else:
                    new_label = current_label

            elif last_string.isdigit():
                if new_string in self.op_lt:
                    if self.can_add_ops(new_string):
                        new_label = current_label + new_string
                        self.op_limit += 1
                    else:
                        new_label = current_label

                elif new_string == ".":
                    if is_dot_used:
                        new_label = current_label
                    else:
                        new_label = current_label + str(".")

                elif new_string == "(":
                    new_label = current_label + str("×(")
                    self.open_bracket += 1
                elif new_string == ")":
                    if self.open_bracket > self.closed_bracket:
                        new_label = current_label + new_string
                        self.closed_bracket += 1
                    else:
                        new_label = current_label
                elif new_string.isdigit():
                    new_label = current_label + new_string
                    self.op_limit = 0

        self.num_label.setText(new_label)

    def handle_input_spec(self, spec_input_passed):
        spec_Bpressed = spec_input_passed
        if spec_Bpressed == "C":
            self.num_label.setText("")
            self.closed_bracket = 0
            self.open_bracket = 0
            self.reset_label = False
        elif spec_Bpressed == "AC":
            self.num_label.setText("")
            self.history_index = 0
            self.history_list = []
            self.open_bracket = 0
            self.closed_bracket = 0
            self.reset_label = False
            self.result = 0
        elif spec_Bpressed == "ANS":
            text_str = self.num_label.text()
            if not text_str or self.reset_label:
                self.num_label.setText("ANS")
            elif text_str[-1] in self.op_lt or text_str[-1] == "(":
                new_label = text_str + "ANS"
                self.num_label.setText(new_label)
            elif text_str[-1] == ")":
                new_label = text_str + "×ANS"
                self.num_label.setText(new_label)
            elif text_str[-1].isdigit():
                new_label = text_str + "×ANS"
                self.num_label.setText(new_label)

        elif spec_Bpressed == "⌫":
            text_to_red = self.num_label.text()
            if text_to_red == "Division by zero":
                self.num_label.clear()
                self.reset_label = True
            elif text_to_red.endswith("ANS"):
                self.num_label.setText(text_to_red[:-3])
            else:
                self.num_label.setText(text_to_red[:-1])
                self.open_bracket = text_to_red.count("(")
                self.closed_bracket = text_to_red.count(")")
                self.op_limit = text_to_red.count("+-×÷")

    def print_result(self):
        current_text = self.num_label.text()
        if current_text.count("(") != current_text.count(")"):
            self.num_label.setText(current_text)
        else:
            if current_text == "ANS":
                self.num_label.setText(str(self.final_result))

                self.reset_label = True

                return
            elif current_text == "Division by zero":
                self.reset_label = True
                self.clear_label("", current_text)

                return

            check_res = self.sol_brac_iterative(current_text)
            if check_res is not None:
                self.num_label.setText(str(self.result))
                self.reset_label = True
                self.history_list.append(current_text)
                self.history_index = len(self.history_list)

    def display_history(self):
        if self.history_list:
            if self.history_index < 0:
                self.history_index = 0
            elif self.history_index > len(self.history_list):
                self.history_index = len(self.history_list)
            if self.history_index == len(self.history_list):
                self.num_label.setText("")
            else:
                self.num_label.setText(str(self.history_list[self.history_index]))

    def change_theme(self):
        self.theme_counter += 1
        if self.theme_counter % 2:
            self.setStyleSheet(self.white_ui)
            self.Theme.setText("🌙 Dark")
        else:
            self.setStyleSheet(self.black_ui)
            self.Theme.setText("☀️ Light")

    def clear_label(self, char, current_label):
        if char in self.button_num:
            self.num_label.setText(char)
        elif char == ".":
            self.num_label.setText("0.")
        elif char in self.op_lt:
            if current_label != "Division by zero" and current_label and self.history_index > 0:
                self.num_label.setText("ANS" + char)
            else:
                self.num_label.setText("")
        elif char == "(":
            if current_label != "Division by zero" and current_label and self.history_index > 0:
                self.num_label.setText("ANS×" + char)
                self.open_bracket += 1
            else:
                self.num_label.setText("")
        elif char == "":
            if current_label == "Division by zero":
                self.num_label.setText("")
        self.reset_label = False

    def sol_brac_iterative(self, string):
        while True:
            is_found = False
            for i in range(len(string)):
                if string[i] == ')':
                    close_index = i
                    for j in reversed(range(i)):
                        if string[j] == '(':
                            open_index = j
                            inside = self.get_num_result(string[open_index + 1:close_index])
                            if inside is None:
                                return None
                            string = string[:open_index] + str(inside) + string[close_index + 1:]
                            is_found = True
                            break
                if is_found:
                    break
            if not is_found:
                self.final_result = self.get_num_result(string)
                return self.final_result

    def has_previous_value(self, string):
        if not string:
            return False
        if string[-1].isdigit():
            return True
        if string.endswith("ANS"):
            return True
        if string[-1] == ')':
            return True
        return False

    def check_unary_minus(self, string, index):
        if index == 0:
            return True

        return string[index - 1] in self.op_lt

    def can_add_ops(self, new_string):
        if self.op_limit >= 2:
            return False

        if self.op_limit == 1:
            return new_string == '-'

        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculators()
    calculator.show()
    calculator.setFocus()
    sys.exit(app.exec_())
