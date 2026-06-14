import sys
from PyQt5.QtWidgets import QApplication,QLabel,QWidget,QGridLayout,QPushButton,QSizePolicy
from PyQt5.QtCore import Qt



class Calculators(QWidget):
    def __init__(self):
        super().__init__()
        self.result=0
        self.grid=QGridLayout()
        self.num_label=QLabel(self)
        self.button_num={}
        self.button_operator={}
        self.button_spec_op={}
        self.reset_label=False
        self.buffer = ""
        self.setFocusPolicy(Qt.StrongFocus)
        self.history_list = []
        self.history_index = 0
        for i in range(10):
            self.button_num[str(i)]=QPushButton(str(i),self)
        operators=["+","-","×","÷","=","."]
        for op in operators:
            self.button_operator[op]=QPushButton(op,self)
        special_operators=["C","ANS","⌫"]
        for spec_op in special_operators:
            self.button_spec_op[spec_op]=QPushButton(spec_op,self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Calculator")
        self.setGeometry(600,400,400,400)
        self.grid.addWidget(self.num_label,0,0,1,5)
        self.grid.addWidget(self.button_spec_op["C"],1,0)
        self.grid.addWidget(self.button_spec_op["ANS"], 1, 1,1,3)
        self.grid.addWidget(self.button_spec_op["⌫"],1,4)
        self.grid.addWidget(self.button_num["7"],2,0)
        self.grid.addWidget(self.button_num["8"],2,1)
        self.grid.addWidget(self.button_num["9"],2,2)
        self.grid.addWidget(self.button_operator["+"],2,3)
        self.grid.addWidget(self.button_num["4"],3,0)
        self.grid.addWidget(self.button_num["5"],3,1)
        self.grid.addWidget(self.button_num["6"],3,2)
        self.grid.addWidget(self.button_operator["-"],3,3)
        self.grid.addWidget(self.button_num["1"],4,0)
        self.grid.addWidget(self.button_num["2"],4,1)
        self.grid.addWidget(self.button_num["3"],4,2)
        self.grid.addWidget(self.button_operator["×"],4,3)
        self.grid.addWidget(self.button_num["0"],5,1,)
        self.grid.addWidget(self.button_operator["."],5,2)
        self.grid.addWidget(self.button_operator["÷"],5,3)
        self.grid.addWidget(self.button_operator["="],2,4,4,1)
        self.num_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.num_label.setFixedHeight(50)
        total_buttons=[]
        for i in range(len(self.button_num)):
            total_buttons.append(self.button_num[str(i)])
        for op in self.button_operator:
            total_buttons.append(self.button_operator[op])
        for i in range(len(total_buttons)):
            total_buttons[i].setSizePolicy(QSizePolicy.Expanding,
                                 QSizePolicy.Expanding)

        self.setStyleSheet("""
                QWidget {
                background-color:hsl(217, 4%, 24%);
                }
                
                QLabel {
                background-color:hsl(217, 4%, 24%);
                color:hsl(216, 1%, 87%);
                font-weight:bold;
                font-size :40px;
                padding-right: 1px;
                border: 5px solid hsl(217, 4%, 10%);
                border-radius: 5px;
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
                """)
        self.setLayout(self.grid)
        for num in self.button_num:
            self.button_num[num].clicked.connect(self.button_clicked)

        for op in self.button_operator:
            if not op =="=":
                self.button_operator[op].clicked.connect(self.button_clicked)
            else:
                self.button_operator[op].clicked.connect(self.print_result)

        for spec_op in self.button_spec_op:
            self.button_spec_op[spec_op].clicked.connect(self.spec_button_clicked)

    def button_clicked(self):
        button_pressed=self.sender()
        assert isinstance(button_pressed, QPushButton)
        self.handle_input_normal(button_pressed.text())

    def keyPressEvent(self,event):
        keybind_pressed = event.text()
        if keybind_pressed.isdigit() or keybind_pressed in (".","+","-") :
            self.handle_input_normal(keybind_pressed)
        elif keybind_pressed == "*":
            self.handle_input_normal("×")
        elif keybind_pressed == "/" :
            self.handle_input_normal("÷")
        elif keybind_pressed == "=" or event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.print_result()
        elif event.key() == Qt.Key_Backspace:
            self.handle_input_spec("⌫")
        elif event.key() == Qt.Key_Left:
            self.history_index -= 1
            self.display_history()
        elif event.key() == Qt.Key_Right:
            self.history_index+=1
            self.display_history()
        elif keybind_pressed.isalpha() :
            self.buffer += keybind_pressed
            if self.buffer.capitalize() == "C" :
                self.handle_input_spec("C")
                self.buffer=""
            elif self.buffer.upper() == "ANS":
                self.handle_input_spec("ANS")
                self.buffer=""




    def calc_operations(self,list_nums ,list_operators):
        i=0
        while i <len(list_operators) :
            if list_operators[i] in ("×","÷") :
                number1=list_nums[i]
                number2=list_nums[i+1]
                math_op = list_operators[i]
                if math_op == "×":
                    result = number1 * number2
                else :
                    try :
                        result = number1 / number2

                    except ZeroDivisionError :
                        self.num_label.setText("Division by zero")
                        self.reset_label = True
                        return None
                list_nums[i+1] = result
                list_nums.pop(i)
                list_operators.pop(i)
            else :
                i+=1
        for i in range(len(list_operators)) :
            number1=list_nums[i]
            number2=list_nums[i+1]
            math_op = list_operators[i]
            if math_op =="+":
                result = number1 + number2
            else :
                result = number1 - number2
            list_nums[i+1] =result
        self.result=list_nums[-1]
        return self.result

    def get_num_result(self,string):
        if not string:
            return None
        num_list=[]
        op_list=[]
        num_to_append=""
        is_dot_encountered = False
        is_first_num_negative=False
        is_negative_num=False
        updated_string = string
        if string[0] == "-" :
            is_first_num_negative=True
            updated_string = string[1:]
        for char in updated_string:
            if char.isdigit() and not is_dot_encountered:
                num_to_append+= char
            elif char == '.':
                is_dot_encountered =True
                num_to_append+="."
            elif char.isdigit() and is_dot_encountered:
                num_to_append += char
            elif char.isalpha() :
                num_to_append += char
            elif char in "+-×÷" :
                if op_list and op_list[-1] in ("+","-","×","÷")  and char == '-':
                    is_negative_num=True
                else:
                    op_list.append(char)
                    if num_to_append == "ANS":
                        num_list.append(self.result)
                    elif is_dot_encountered:
                        num_list.append(float(num_to_append))
                    elif not is_dot_encountered:
                        num_list.append(int(num_to_append))
                    if is_negative_num :
                        num_list[-1] = num_list[-1] * (-1)
                        is_negative_num = False
                    num_to_append=""
                    is_dot_encountered = False

        if num_to_append :
            if num_to_append == "ANS":
                num_list.append(self.result)
            elif not is_dot_encountered:
                num_list.append(int(num_to_append))
            elif is_dot_encountered:
                num_list.append(float(num_to_append))
        if is_negative_num :
            num_list[-1] = -num_list[-1]
        if is_first_num_negative :
            if not num_list :
                return None
            num_list[0] = num_list[0] * (-1)
        if len(num_list) == len(op_list) + 1 :
            no_error=self.calc_operations(num_list,op_list)
            if  no_error is not None:
                return self.result
            else:
                return None
        else:
            return None


    def isDot_inNum(self,string):
        reversed_str = reversed(string)
        for r_str in reversed_str :
            if r_str =='.':
                return True
            elif r_str in "+-×÷":
                return False
        return False

    def spec_button_clicked(self):
        spec_button_pressed= self.sender()
        assert isinstance(spec_button_pressed, QPushButton)
        self.handle_input_spec(spec_button_pressed.text())


    def handle_input_normal(self,string_passed):
        new_str = string_passed
        current_label = self.num_label.text()
        new_label = ""
        is_dot_used = self.isDot_inNum(current_label)
        if self.reset_label:
            if new_str in self.button_num:
                self.num_label.setText(new_str)
                self.reset_label = False
                return
            elif new_str == '.':
                self.num_label.setText("0.")
                self.reset_label = False
                return
            elif new_str in "+-×÷":
                if current_label != "Division by zero" and current_label:
                    self.reset_label = False
                    self.num_label.setText("ANS")
                    current_label = self.num_label.text()
                else:
                    self.num_label.setText("")
        if not current_label:
            if new_str in self.button_num or new_str == '-':
                new_label = str(new_str)
            elif new_str == '.':
                new_label = str("0.")
        elif not current_label == "ANS":
            last_str = current_label[-1]
            if last_str in self.button_operator:
                if new_str in self.button_operator:
                    if new_str == '-' and last_str in ("+", "-", "×", "÷"):
                        new_label = current_label + str(new_str)
                    elif not new_str == '.':
                        new_label = current_label[:-1] + str(new_str)
                    else:
                        if is_dot_used:
                            new_label = current_label
                        else:
                            new_label = current_label + "0."
                elif new_str in self.button_num:
                    new_label = current_label + str(new_str)
            elif last_str in self.button_num:
                if is_dot_used:
                    if not new_str == '.':
                        new_label = current_label + str(new_str)
                    else:
                        new_label = current_label
                else:
                    new_label = current_label + str(new_str)
        elif current_label == "ANS":
            if new_str in "+-×÷":
                new_label = current_label + new_str
            else:
                new_label = current_label
        self.num_label.setText(new_label)

    def handle_input_spec(self , spec_input_passed):
        spec_Bpressed = spec_input_passed
        new_label = ""
        if spec_Bpressed == "C":
            self.num_label.setText("")
        elif spec_Bpressed == "ANS":
            text_str = self.num_label.text()
            if not text_str or self.reset_label:
                self.num_label.setText("ANS")
            elif text_str[-1] in "+-×÷":
                new_label = text_str + "ANS"
                self.num_label.setText(new_label)
        elif spec_Bpressed == "⌫":
            text_to_red = self.num_label.text()
            if text_to_red == "Division by zero":
                self.num_label.setText(text_to_red)
            elif text_to_red == "ANS":
                self.num_label.setText("")
            else:
                self.num_label.setText(text_to_red[:-1])
    def print_result(self):
        current_text = self.num_label.text()

        if current_text == "ANS":
            self.num_label.setText(str(self.result))
            self.reset_label = True

            return

        check_res = self.get_num_result(current_text)
        if check_res is not None:
            self.num_label.setText(str(self.result))
            self.reset_label = True
            self.history_list.append(current_text)
            self.history_index = len(self.history_list)
        print(self.history_list , self.history_index)


    def display_history(self):
        if self.history_list:
             if self.history_index <0 :
                 self.history_index = 0
             elif self.history_index > len(self.history_list):
                 self.history_index = len(self.history_list)
             if self.history_index == len(self.history_list):
                 self.num_label.setText("")
             else:
                 self.num_label.setText(str(self.history_list[self.history_index]))


if __name__=="__main__":
    app=QApplication(sys.argv)
    calculator=Calculators()
    calculator.show()
    calculator.setFocus()
    sys.exit(app.exec_())
