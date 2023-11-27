# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 07:12:58 2023

@author: Enea
"""

from PyQt5.QtWidgets import QAction, QMenu
    
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

    onedim_menu = QMenu('1D Linear Chains', main_window)
    model_menu.addMenu(onedim_menu)
    # Add actions to the Model menu...
    Fermi_Hubbard_nospin = QAction('Fermi-Hubbard Spinless', main_window)
    onedim_menu.addAction(Fermi_Hubbard_nospin)
    Fermi_Hubbard_spin = QAction('Fermi-Hubbard with Spin', main_window)
    onedim_menu.addAction(Fermi_Hubbard_spin)
    Bose_Hubbard = QAction('Bose-Hubbard', main_window)
    onedim_menu.addAction(Bose_Hubbard)
    Heisenberg = QAction('Full Heisenberg model', main_window)
    onedim_menu.addAction(Heisenberg)
    XXX = QAction('XXX model with Z interaction', main_window)
    onedim_menu.addAction(XXX)
    AndersonImp = QAction('Single-Impurity Anderson', main_window)
    onedim_menu.addAction(AndersonImp)
    tJ = QAction('t-J model', main_window)
    onedim_menu.addAction(tJ)
    # Molecular stuff
    HF_menu = QMenu('Hartree-Fock', main_window)
    model_menu.addMenu(HF_menu)
    # Add actions
    # . . .
    DFT_menu = QMenu('Density Functional Theory', main_window)
    model_menu.addMenu(DFT_menu)


def create_edit_menu(main_window):
    edit_menu = main_window.menuBar().addMenu('Edit')
    # Add actions to the Edit menu...
    


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