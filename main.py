# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 18:50:23 2023

@author: Enea
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, \
    QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QDockWidget, QTextEdit, QOpenGLWidget
from PyQt5.QtGui import QIcon  # Import QIcon from QtGui module
import moderngl
#from PyQt5.QtOpenGL import QOpenGLWidget
from gui_elements.main_menu import *





starting_text = "Welcome! \nQuantum Many-Body Theory Calculator\
\nCurrent Ver: development 1.0\nAuthor: E.Ç\nCurrent \
release date: 25 October 2023\nEnjoy bois :0 !\n.   .   .   .   .   .\n.   .   .   .   .   .\n~~~~~~~~~~\n"


def create_output_prompt(main_window):
    output_prompt_panel = QDockWidget("Output Prompt", main_window)

    output_prompt = QTextEdit()
    output_prompt.setReadOnly(True)
    output_prompt.append(starting_text)  # Initial welcome message
    output_prompt.setStyleSheet("color: white; background-color: black;")

    output_prompt_panel.setWidget(output_prompt)
    output_prompt_panel.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
    output_prompt_panel.setMinimumWidth(300)  # Set the initial width to 300 pixels
    main_window.addDockWidget(2, output_prompt_panel)  # Add dock widget to the main window, 4 represents bottom dock area

# Function to create the central OpenGL widget
def create_opengl_widget(main_window):
    opengl_functions = {
        'initializeGL': lambda: None,  # Placeholder initialization function
        'paintGL': lambda: None,  # Placeholder paint function
        'resizeGL': lambda w, h: None  # Placeholder resize function
    }

    def initializeGL():
        opengl_functions['initializeGL']()

    def paintGL():
        opengl_functions['paintGL']()

    def resizeGL(w, h):
        opengl_functions['resizeGL'](w, h)

    opengl_widget = QOpenGLWidget()
    opengl_widget.initializeGL = initializeGL
    opengl_widget.paintGL = paintGL
    opengl_widget.resizeGL = resizeGL

    return opengl_widget

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

    #create_left_panel(main_window)
    create_output_prompt(main_window)
    opengl_widget = create_opengl_widget(main_window)
    main_window.setCentralWidget(opengl_widget)

    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    create_window()


