"""
This stylesheet provides a modern, dark theme for the Azan Reminder App.
It uses a darker color palette, rounded corners, and subtle animations
to create a professional and clean user interface.
"""

def get_dark_theme_stylesheet():
    """
    Returns a string containing the complete stylesheet for the dark theme.
    """
    return """
    /* Main Window and General App Styling */
    QMainWindow {
        background-color: #000000;
    }

    QWidget#centralWidget {
        background-color: #000000;
    }
    
    /* Style for the new Codenix logo next to the close button */
    QLabel#codenixLogo {
        min-width: 40px;
        min-height: 40px;
        qproperty-alignment: 'AlignHCenter | AlignVCenter';
    }
    
    /* Labels for Prayer Times */
    QLabel {
        color: #e0e0e0;
        font-size: 14px;
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* Input Fields for Time */
    QTimeEdit {
        background-color: #1a1a1a;
        border: 1px solid #333333;
        border-radius: 6px;
        padding: 8px;
        color: #e0e0e0;
        font-size: 16px;
    }
    
    QTimeEdit:hover {
        border: 1px solid #555555;
    }

    /* ComboBox for Actions */
    QComboBox {
        background-color: #1a1a1a;
        border: 1px solid #333333;
        border-radius: 6px;
        padding: 8px;
        color: #e0e0e0;
        font-size: 16px;
    }

    QComboBox::drop-down {
        border: 0px;
        width: 20px;
    }

    QComboBox::down-arrow {
        image: url(resources/icons/dropdown_arrow.svg);
        width: 12px;
        height: 12px;
        right: 5px;
    }

    /* Animated "Set Reminders" Button */
    QPushButton {
        background-color: #0059b3;
        color: #ffffff;
        font-size: 16px;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    QPushButton:hover {
        background-color: #00478f;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }

    QPushButton:pressed {
        background-color: #003366;
        padding-top: 13px;
        padding-bottom: 11px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    /* Styles for the "Close" button */
    QPushButton#closeButton {
        background-color: #8c0000;
        color: #ffffff;
        font-size: 14px;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    QPushButton#closeButton:hover {
        background-color: #730000;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }

    QPushButton#closeButton:pressed {
        background-color: #5c0000;
        padding-top: 11px;
        padding-bottom: 9px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Status Label with sunken frame */
    QLabel#status_label {
        background-color: #1a1a1a;
        border: 1px inset #333333;
        border-radius: 8px;
        color: #a9b7c6;
        padding: 10px;
        margin-top: 10px;
        font-size: 14px;
        min-height: 40px;
    }

    /* Set the object names for widgets to be able to style them individually */
    #action_dropdown {
        margin-top: 10px;
        margin-bottom: 10px;
    }
    """
