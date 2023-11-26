# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 18:50:23 2023

@author: Enea
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu
from PyQt5.QtGui import QIcon  # Import QIcon from QtGui module


def create_file_menu(main_window):
    file_menu = main_window.menuBar().addMenu('File')
    #
    open_action = QAction('Open', main_window)
    file_menu.addAction(open_action)
    #
    save_action = QAction('Save', main_window)
    file_menu.addAction(save_action)
    #
    save_as_action = QAction('Save As', main_window)
    file_menu.addAction(save_as_action)
    #
    export_action = QAction('Export', main_window)
    file_menu.addAction(export_action)
    #
    import_action = QAction('Import', main_window)
    file_menu.addAction(import_action)
    
    
    
def create_model_menu(main_window):
    model_menu = main_window.menuBar().addMenu('Model')

    # Add actions to the Model menu...
    # ...

def create_edit_menu(main_window):
    edit_menu = main_window.menuBar().addMenu('Edit')

    # Add actions to the Edit menu...
    # ...

def create_search_menu(main_window):
    search_menu = main_window.menuBar().addMenu('Search')

    # Add actions to the Search menu...
    # ...

def create_simulation_menu(main_window):
    simulation_menu = main_window.menuBar().addMenu('Simulation')

    # Add actions to the Simulation menu...
    # ...

def create_projects_menu(main_window):
    projects_menu = main_window.menuBar().addMenu('Projects')

    # Add actions to the Projects menu...
    # ...

def create_console_menu(main_window):
    console_menu = main_window.menuBar().addMenu('Console')

    # Add actions to the Console menu...
    # ...

def create_tools_menu(main_window):
    tools_menu = main_window.menuBar().addMenu('Tools')

    # Add actions to the Tools menu...
    # ...

def create_settings_menu(main_window):
    settings_menu = main_window.menuBar().addMenu('Settings')

    # Add actions to the Settings menu...
    # ...

def create_help_menu(main_window):
    help_menu = main_window.menuBar().addMenu('Help')

    # Add actions to the Help menu...
    # ...

def create_window():
    app = QApplication(sys.argv)

    main_window = QMainWindow()
    main_window.setWindowTitle("Quantum Sail")
    main_window.setGeometry(100, 100, 1920, 1080)
    #
    # Set the icon for the window
    icon_path = 'main_icon3.ico'  # Replace with the path to your .ico file
    app_icon = QIcon(icon_path)
    main_window.setWindowIcon(app_icon)
    #
    create_file_menu(main_window)
    create_model_menu(main_window)
    create_edit_menu(main_window)
    create_search_menu(main_window)
    create_simulation_menu(main_window)
    create_projects_menu(main_window)
    create_console_menu(main_window)
    create_tools_menu(main_window)
    create_settings_menu(main_window)
    create_help_menu(main_window)

    main_window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    create_window()

