import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout

from interface.Unit4InterfaceConnector import EnvironmentManagementMenu, Tools


class UI(QtWidgets.QWidget):
    MAIN_MENU_TITLE = "Unit4 Manager"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tools = None
        self.menu = None
        self.widgets = None
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        self.setMinimumWidth(350)
        self.setMinimumHeight(400)
        self.load_main_menu()

    def __clear_layout(self, item=None):
        layout = None
        widget = None

        if item is None:
            item = self

        if hasattr(item, "layout"):
            if callable(item.layout):
                layout = item.layout()
        else:
            layout = None

        if hasattr(item, "widget"):
            if callable(item.widget):
                widget = item.widget()
        else:
            widget = None

        if widget:
            widget.setParent(None)
        elif layout:
            for i in reversed(range(layout.count())):
                self.__clear_layout(layout.itemAt(i))

    def __new_button(self, btn_text: str, btn_method, parameters=None):
        button = QtWidgets.QPushButton(btn_text, self)
        button.clicked.connect(btn_method if parameters is None else lambda: btn_method(parameters))
        return button

    def __new_label(self, lbl_text: str):
        label = QtWidgets.QLabel(lbl_text, self)
        return label

    def __new_text_box(self, text: str = ""):
        text_box = QtWidgets.QTextEdit(text, self)
        return text_box

    def __change_window(self, window_title: str, widgets):
        self.widgets = widgets
        self.__clear_layout()
        self.setWindowTitle(window_title)
        self.__add_widgets()
        if window_title != self.MAIN_MENU_TITLE:
            self.layout().addWidget(self.__get_btn_back_to_main_menu())

    def __add_widgets(self):
        for widget in self.widgets:
            self.layout().addWidget(widget)

    def __get_btn_back_to_main_menu(self):
        return self.__new_button("Back to main menu", self.load_main_menu)

    # Menus
    def load_main_menu(self):
        widgets = [
            self.__new_button("Environment Management Menu", self.load_environment_management_menu),
            self.__new_button("Tools Menu", self.load_tools_menu)
        ]
        self.__change_window(self.MAIN_MENU_TITLE, widgets)

    def load_environment_management_menu(self):
        self.menu = EnvironmentManagementMenu()
        widgets = [
            self.__new_button("Run all", self.menu.run_all),
            self.__new_button("Generate Bookmarks", self.menu.generate_bookmarks),
            self.__new_button("Generate Insomnia Collections", self.menu.build_insomnia_collection),
            self.__new_button("Distribute Bookmarks across browsers", self.menu.distribute_bookmarks_across_browsers)
        ]
        self.__change_window("Environment Management", widgets)

    def load_tools_menu(self):
        widgets = [
            self.__new_button("CSV Header Into Liquid Variables",
                              self.load_csv_header_to_liquid_variables_screen)
        ]
        self.__change_window("Tools", widgets)

    def load_csv_header_to_liquid_variables_screen(self):
        text_box1 = self.__new_text_box(
            "Account No;Cardholder;Place;Invoice No;Invoice Date;Gross Amount;Item No;Type;Ticket "
            "No;Name;Routing;Merchant;Sales Date;Travel Date;Booking Class;Airline Code;Sales Currency;Net Amount ("
            "SC);Tax(SC);Billing Currency;Gross Amount (BC);Details;Employee No;Department;Cost Centre;Accounting "
            "Unit;Internal Account;DBI Date;Project No;Order No;Action No;Final Destination;Customer "
            "Reference;0-Invoice No;IATA No;VAT Rate;Fee Tag;Service code;Domestic Tag;Due Date;Additional "
            "Insurance;Service line1;Service line2;Service line3;Fees (Tax);A.I.D.A. Number;VAT Type")
        text_box2 = self.__new_text_box("CurrentItem")
        self.tools = Tools(text_box1, text_box2)
        widgets = [
            self.__new_label("Header string"),
            text_box1,
            self.__new_label("Variable that holds the header string"),
            text_box2,
            self.__new_button("Convert",
                              self.tools.convert_csv_header_to_liquid_variables)
        ]
        self.__change_window("Tools", widgets)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())
