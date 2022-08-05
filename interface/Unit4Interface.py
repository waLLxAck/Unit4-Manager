import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout

from Unit4InterfaceConnector import EnvironmentManagementMenu, Tools, ProjectEntryScreen


class UI(QtWidgets.QWidget):
    MAIN_MENU_TITLE = "Unit4 Manager"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.NEW_PROJECT_ENTRY_TITLE = "New Project Entry"
        self.environments = None
        self.tools = None
        self.menu = None
        self.pes = None
        self.widgets = None
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        self.load_main_menu()
        self.urls = []

    def __clear_layout(self, item=None):
        if item is None:
            for i in reversed(range(self.layout().count())):
                self.layout().itemAt(i).widget().setParent(None)
                self.layout().removeItem(self.layout().itemAt(i))
        else:
            self.layout().removeItem(item)
            item.widget().setParent(None)
            item.widget().deleteLater()
            item.deleteLater()

    def __new_button(self, btn_text: str, btn_method, parameters=None):
        button = QtWidgets.QPushButton(btn_text, self)
        button.clicked.connect(btn_method if parameters is None else lambda: btn_method(parameters))
        return button

    def __new_label(self, lbl_text: str):
        label = QtWidgets.QLabel(lbl_text, self)
        return label

    def __new_text_box(self, text: str = ""):
        text_box = QtWidgets.QLineEdit(text, self)
        return text_box

    def __change_window(self, window_title: str, widgets):
        self.widgets = widgets
        self.__clear_layout()
        self.setWindowTitle(window_title)
        self.__add_widgets()
        if window_title != self.MAIN_MENU_TITLE:
            self.layout().addWidget(self.__get_btn_back_to_main_menu())
        self.make_widgets_fit_window()

    def __add_widgets(self):
        for widget in self.widgets:
            self.layout().addWidget(widget)
            widget.resize(widget.sizeHint())

    def __get_btn_back_to_main_menu(self):
        return self.__new_button("Back to Main Menu", self.load_main_menu)

    # Menus
    def load_main_menu(self):
        widgets = [
            self.__new_button("New Project Entry", self.load_new_project_entry_screen),
            self.__new_button("Environment Management Menu", self.load_environment_management_menu),
            self.__new_button("Tools Menu", self.load_tools_menu),
            self.__new_button("Exit", sys.exit)
        ]
        self.__change_window(self.MAIN_MENU_TITLE, widgets)

    def load_new_project_entry_screen(self):
        # TODO: should include a label and a text box for each of the following json fields:
        # {
        #     "project_name": "",
        #     "swagger_api": "",
        #     "urls": [
        #         {
        #             "name": "",
        #             "url": ""
        #         }
        #     ],
        #     "environments": [
        #         {
        #             "name": "prev",
        #             "extension_kit": "",
        #             "erp_lab": "",
        #             "swagger_api": "",
        #             "authorization": {
        #                 "company_id": "",
        #                 "access_token_url": "",
        #                 "client_id": "",
        #                 "client_secret": ""
        #             }
        #         },
        #         {
        #             "name": "acpt",
        #             "extension_kit": "",
        #             "erp_lab": "",
        #             "swagger_api": "",
        #             "authorization": {
        #                 "company_id": "",
        #                 "access_token_url": "",
        #                 "client_id": "",
        #                 "client_secret": ""
        #             }
        #         },
        #         {
        #             "name": "prod",
        #             "extension_kit": "",
        #             "erp_lab": "",
        #             "swagger_api": "",
        #             "authorization": {
        #                 "company_id": "",
        #                 "access_token_url": "",
        #                 "client_id": "",
        #                 "client_secret": ""
        #             }
        #         }
        #     ]
        # }

        # Resize window
        lbl_project_name = self.__new_label("Project Name")
        txt_box_project_name = self.__new_text_box("Sandbox Environment")
        lbl_swagger_api = self.__new_label("Swagger API")
        txt_box_swagger_api = self.__new_text_box(
            "https://au01-npe.erpx-api.unit4cloud.com/swagger/?tenant=30713278-9cce-43c9-8816-e59c34e8e5c4")
        # add a text box upon button click to add a new url
        btn_add_url = self.__new_button("Add URL", self.__add_url_text_box)

        environment_buttons = []
        # add a button to add a new environment
        for environment_name in ["prev", "acpt", "prod"]:
            btn_add_environment = self.__new_button(f"Add Environment - {environment_name.upper()}",
                                                    self.__add_environment_text_box, environment_name)
            environment_buttons.append(btn_add_environment)
            self.layout().addWidget(btn_add_environment)

        self.pes = ProjectEntryScreen(txt_box_project_name, txt_box_swagger_api, self.urls, environment_buttons)
        widgets = [
            lbl_project_name,
            txt_box_project_name,
            lbl_swagger_api,
            txt_box_swagger_api,
            btn_add_url,
            self.__new_button("Save", self.pes.save_new_project_entry)
        ]
        for btn in environment_buttons:
            widgets.append(btn)
        self.__change_window(self.NEW_PROJECT_ENTRY_TITLE, widgets)

    def __add_environment_text_box(self, environment_name):
        txt_box_environment_name = self.__new_text_box(environment_name)
        txt_box_extension_kit = self.__new_text_box("Extension Kit")
        txt_box_erp_lab = self.__new_text_box("ERP Lab")
        txt_box_swagger_api = self.__new_text_box("Swagger API")
        txt_box_authorization = self.__new_text_box("Authorization")
        widgets = [
            txt_box_environment_name,
            txt_box_extension_kit,
            txt_box_erp_lab,
            txt_box_swagger_api,
            txt_box_authorization,
        ]
        btn_remove_environment = self.__new_button(f"Remove environment - {environment_name}",
                                                   self.__remove_environment_widgets,
                                                   [environment_name, txt_box_environment_name, txt_box_extension_kit,
                                                    txt_box_erp_lab,
                                                    txt_box_swagger_api, txt_box_authorization])
        widgets.append(btn_remove_environment)
        height_increase = 0
        for widget in widgets:
            self.layout().addWidget(widget)
            widget.resize(widget.sizeHint())
            height_increase += widget.sizeHint().height()
        self.setFixedHeight(self.height() + height_increase)

    def __remove_environment_widgets(self, parameters):
        height_decrease = 0
        for widget in parameters[1:]:
            height_decrease += widget.sizeHint().height()
            self.layout().removeWidget(widget)
            widget.deleteLater()
            widget.setParent(None)
        self.layout().removeWidget(self.sender())
        self.setFixedHeight(self.height() - height_decrease)

    def __add_url_text_box(self):
        # create label 'URL Name'
        lbl_url_name = self.__new_label("URL Name")
        # add label to layout above 'Add URL' button
        self.layout().insertWidget(self.layout().indexOf(self.sender()), lbl_url_name)
        txt_box_url = self.__new_text_box("EventForce Documentation")
        # add text box to layout above 'Add URL' button and below 'URL Name' label
        self.layout().insertWidget(self.layout().indexOf(self.sender()), txt_box_url)

        self.urls.append(txt_box_url)
        # add a button to remove the text box and label created above the 'Add URL' button and below the text box
        btn_remove_url = self.__new_button("Remove URL", self.__remove_url_widgets, [txt_box_url, lbl_url_name])
        self.layout().insertWidget(self.layout().indexOf(self.sender()), btn_remove_url)
        # resize the window to fit the new widgets
        self.setFixedHeight(self.height() + txt_box_url.sizeHint().height() + btn_remove_url.sizeHint().height())

    def __remove_url_widgets(self, items_to_remove):
        for item in items_to_remove:
            self.layout().removeWidget(item)
            item.setParent(None)
            if item in self.urls:
                self.urls.remove(item)
        # remove the button from the menu
        self.layout().removeWidget(self.sender())

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
        text_box3 = self.__new_text_box(";")
        self.tools = Tools(text_box1, text_box2, text_box3)
        widgets = [
            self.__new_label("Header string"),
            text_box1,
            self.__new_label("Variable that holds the header string"),
            text_box2,
            self.__new_label("Delimiter"),
            text_box3,
            self.__new_button("Convert",
                              self.tools.convert_csv_header_to_liquid_variables)
        ]
        self.__change_window("Tools", widgets)

    def make_widgets_fit_window(self):
        for widget in self.widgets:
            widget.resize(widget.sizeHint())
        self.setMinimumHeight(self.height())
        self.setMinimumWidth(self.width())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())
