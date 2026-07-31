"""
Custom stylesheets for the application windows
Current list of things used that need to be included in each style
QWidget (important for background)
QLabel
QPushButton
QSpinBox
QToolTip (set indirectly)
QComboBox

"""

#Dark Mode
DARK_THEME="""
QWidget {
    background-color: #121212;
    color: #ffffff;
    font-size: 12px;
}

QLabel {
    color: #ffffff;
}

QPushButton {
    background-color: #3c3c3c;
    border: 1px solid #555555;
    border-radius: 5px;
    padding: 6px 12px;
}

QPushButton:hover {
    background-color: #505050;
}

QPushButton:pressed {
    background-color: #606060;
}

QPushButton:disabled {
    background-color: #333333;
    color: #777777;
}

QSpinBox, QLineEdit {
    background-color: #3c3c3c;
    color: white;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 4px;
}

QSpinBox:focus, QLineEdit:focus {
    border: 1px solid #888888;
}

QCheckBox {
    color: white;
}

QToolTip {
background-color: #252525;
    color: #ffffff;
    border: 1px solid #555555;
    padding: 6px;
    border-radius: 4px;
}

QComboBox {
    background-color: #3c3c3c;
    color: #ffffff;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 4px 8px;
}

QComboBox:hover {
    border: 1px solid #777777;
}

"""

# default theme (nothing changed currently)
LIGHT_THEME=""" """