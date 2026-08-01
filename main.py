import sys
import os


from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QHeaderView,
    QFileDialog
)

from PyQt6.QtCore import Qt, QSettings


from property_search import search_properties
from parcel_mapper import generate_parcel_maps



class ParcelSearch(QWidget):


    def __init__(self):

        super().__init__()


        self.setWindowTitle(
            "Hamilton County Parcel Search"
        )


        self.resize(
            1000,
            600
        )


        self.csv_file = "res/properties.csv"

        self.matches = []


        self.settings = QSettings(
            "ParcelSearch",
            "HamiltonCounty"
        )


        self.output_directory = self.settings.value(
            "output_directory",
            os.getcwd()
        )


        layout = QVBoxLayout()



        controls = QHBoxLayout()


        self.search_box = QLineEdit()

        self.search_box.setPlaceholderText(
            "Search..."
        )


        self.type_box = QComboBox()

        self.type_box.addItems(
            [
                "owner",
                "mailing",
                "property"
            ]
        )


        self.search_button = QPushButton(
            "Search"
        )


        self.search_button.clicked.connect(
            self.search
        )


        controls.addWidget(
            self.search_box
        )


        controls.addWidget(
            self.type_box
        )


        controls.addWidget(
            self.search_button
        )


        layout.addLayout(
            controls
        )



        self.table = QTableWidget()


        self.table.setColumnCount(
            5
        )


        self.table.setHorizontalHeaderLabels(
            [
                "",
                "Parcel",
                "Owner",
                "Property",
                "City",
            ]
        )


        header = self.table.horizontalHeader()


        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft
        )


        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.ResizeToContents
        )


        for col in range(1,5):

            header.setSectionResizeMode(
                col,
                QHeaderView.ResizeMode.Stretch
            )


        layout.addWidget(
            self.table
        )



        selection_buttons = QHBoxLayout()


        self.select_all_button = QPushButton(
            "Select All"
        )


        self.select_all_button.clicked.connect(
            self.select_all
        )


        self.deselect_all_button = QPushButton(
            "Deselect All"
        )


        self.deselect_all_button.clicked.connect(
            self.deselect_all
        )


        selection_buttons.addWidget(
            self.select_all_button
        )


        selection_buttons.addWidget(
            self.deselect_all_button
        )


        layout.addLayout(
            selection_buttons
        )



        self.folder_button = QPushButton(
            "Choose KML Output Folder"
        )


        self.folder_button.clicked.connect(
            self.choose_output_folder
        )


        layout.addWidget(
            self.folder_button
        )



        self.map_button = QPushButton(
            "Generate Map"
        )


        self.map_button.clicked.connect(
            self.generate_map
        )


        layout.addWidget(
            self.map_button
        )



        self.status = QLabel(
            "Searching..."
        )


        layout.addWidget(
            self.status
        )


        self.setLayout(
            layout
        )



    def choose_output_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select KML Output Folder",
            self.output_directory
        )


        if folder:

            self.output_directory = folder

            self.settings.setValue(
                "output_directory",
                folder
            )

            self.status.setText(
                f"Output: {folder}"
            )



    def search(self):

        self.status.setText(
            "Searching CSV..."
        )


        self.matches = search_properties(
            self.csv_file,
            self.search_box.text(),
            self.type_box.currentText()
        )


        self.table.setRowCount(
            len(self.matches)
        )


        for row, parcel in enumerate(self.matches):


            checkbox = QTableWidgetItem()


            checkbox.setFlags(
                checkbox.flags()
                |
                Qt.ItemFlag.ItemIsUserCheckable
            )


            checkbox.setCheckState(
                Qt.CheckState.Checked
            )


            self.table.setItem(
                row,
                0,
                checkbox
            )


            address = " ".join(
                filter(
                    None,
                    [
                        parcel.get("location_house_number",""),
                        parcel.get("location_street_name",""),
                        parcel.get("location_street_suffix","")
                    ]
                )
            )


            values = [

                parcel.get(
                    "parcel_number",
                    ""
                ),

                parcel.get(
                    "owner_name_1",
                    ""
                ),

                address,

                parcel.get(
                    "owner_city",
                    ""
                )

            ]


            for col, value in enumerate(
                values,
                start=1
            ):

                self.table.setItem(
                    row,
                    col,
                    QTableWidgetItem(
                        str(value)
                    )
                )


        self.status.setText(
            f"Found {len(self.matches)} parcels"
        )



    def select_all(self):

        for row in range(
            self.table.rowCount()
        ):

            item = self.table.item(
                row,
                0
            )


            if item:

                item.setCheckState(
                    Qt.CheckState.Checked
                )



    def deselect_all(self):

        for row in range(
            self.table.rowCount()
        ):

            item = self.table.item(
                row,
                0
            )


            if item:

                item.setCheckState(
                    Qt.CheckState.Unchecked
                )



    def generate_map(self):

        selected_ids = []


        for row in range(
            self.table.rowCount()
        ):


            checkbox = self.table.item(
                row,
                0
            )


            if checkbox.checkState() == Qt.CheckState.Checked:


                parcel = self.table.item(
                    row,
                    1
                )


                if parcel:

                    selected_ids.append(
                        parcel.text()
                    )



        if not selected_ids:

            self.status.setText(
                "No parcels selected"
            )

            return



        self.status.setText(
            f"Generating map for {len(selected_ids)} parcels..."
        )


        generate_parcel_maps(
            selected_ids,
            self.update_status,
            self.output_directory
        )



    def update_status(
        self,
        message
    ):

        self.status.setText(
            message
        )

        QApplication.processEvents()



if __name__ == "__main__":


    app = QApplication(
        sys.argv
    )


    font = app.font()

    font.setPointSize(
        14
    )

    app.setFont(
        font
    )


    window = ParcelSearch()

    window.show()


    sys.exit(
        app.exec()
    )
