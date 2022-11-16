import tkinter
from tkinter import ttk
from tkinter import simpledialog
from tkinter import filedialog
import sqlite3
from types import NoneType
import Cards

import sys
import subprocess
import os

#Define menu items
def CreateNewTable():

    if (interfaceTable.sql3 == NoneType):
        interfaceTable.connect
        interfaceTable.sql3.saveTable()
        interfaceTable.disconnect()

    files = [('Table', '*.mem')]
    newTablePath = tkinter.filedialog.asksaveasfile(
        filetypes = files, defaultextension = files        
        )

    tablePathDef = newTablePath.name
    tablePath = tablePathDef.replace("/", "\\")
    tName = tablePath[tablePath.rfind("\\")+1:tablePath.rfind(".mem")]

    interfaceTable.CleanTable(tName, tablePath)

    handleTable(interfaceTable)
    
def OpenTable():

    if (interfaceTable.sql3 == NoneType):
        interfaceTable.connect()
        interfaceTable.sql3.saveTable()
        interfaceTable.disconnect()

    files = [('Table', '*.mem')]
    newTablePath = tkinter.filedialog.askopenfilename(
        filetypes = files, defaultextension = files        
        )


    tablePath = newTablePath.replace("/", "\\")
    tName = tablePath[tablePath.rfind("\\")+1:tablePath.rfind(".mem")]

    interfaceTable.CleanTable(tName, tablePath)

    handleTable(interfaceTable)

def SaveTable():

    if (interfaceTable.sql3 == NoneType):
        interfaceTable.connect()
        interfaceTable.sql3.saveTable()
        interfaceTable.disconnect()

#define button activation/disactivation
def ActiveBut(button):
    button.config(state = 'normal')
def deActiveBut(button):
    button.config(state = 'disabled')

#define hierarchy events
def itemSelect(event):
    ActiveBut(DelCat)

    if (len(Hierarchy.selection())==0):
        deActiveBut(DelCat)

#Update hierarchy Table
def hierUpdate():

    for i in Hierarchy.get_children():
        Hierarchy.delete(i)

    indHierarchy = -1
    for cat in interfaceTable.cats:
        indHierarchy += 1
        Hierarchy.insert('', tkinter.END, text = cat, iid = indHierarchy, open = False)
        for d, deck in interfaceTable.cats[cat].decks:
            indHierarchy += 1
            Hierarchy.insert('', tkinter.END, text = deck, iid = indHierarchy, open = False)
            Hierarchy.move(indHierarchy, indHierarchy-(d+1), d)

    

#Define button functions
def newCategory():

    nameCategory = tkinter.simpledialog.askstring("Input", 'Category name:', parent = window)

    if (nameCategory != ""):
        Cards.Category(nameCategory, interfaceTable)
        hierUpdate()


def deleteCategory():
    for selectedItem in Hierarchy.selection():
        item = Hierarchy.item(selectedItem)
        SelectedCatName = item['text']
        interfaceTable.deleteCat(interfaceTable.cats[SelectedCatName])

    hierUpdate()
    deActiveBut(DelCat)

#Define frames
def SetHierarchyFrame():

    #create hierarchy frame
    frameHierarchy = tkinter.Frame(window)
    frameHierarchy.pack(side='left', fill = 'y')

    #Create table hierarchy
    hierarchy = tkinter.ttk.Treeview(frameHierarchy)
    hierarchy.pack(side = 'top')

    #Create hiearchy buttons frame
    frameHiearchyButtons = tkinter.Frame(frameHierarchy)
    frameHiearchyButtons.pack(side = 'top')

    #New category button
    butLeftHierarchy = tkinter.Button(frameHiearchyButtons, text = 'New Category', command = newCategory, state = 'disabled')
    butLeftHierarchy.pack(side = 'left')

    #Delete category button
    butRightHierarchy = tkinter.Button(frameHiearchyButtons, text = 'Delete Category', command = deleteCategory, state = 'disabled')
    butRightHierarchy.pack(side = 'right')

    return hierarchy, butLeftHierarchy, butRightHierarchy


def handleTable(table):

    #set the heading of the hieararchy table
    Hierarchy.heading('#0', text=table, anchor = tkinter.W)


    table.connect()

    #fetch the existing cards in the table
    resCats = table.sql3.curs.execute("SELECT categoryCol FROM cats").fetchall()

    if len(resCats) != 0:

        for result in resCats:
            cards.update({result[0].nameCat : result})

    table.disconnect()

    ActiveBut(NewCat)
    hierUpdate()

#Set main window

window = tkinter.Tk()

#get home directory and temporary directory
homeDir = os.path.expanduser('~')
dirTemp = homeDir + fr'\AppData\Roaming\MemoryCards\temp'

Hierarchy, NewCat, DelCat = SetHierarchyFrame()

menubar = tkinter.Menu(window)
file_menu = tkinter.Menu(menubar, tearoff = False)

cards = dict()
decks = dict()
categories = dict()

k=1

FPath = dirTemp + str(k) + '.mem'
tName = FPath[FPath.rfind("\\")+1:FPath.rfind(".mem")]

interfaceTable = Cards.Table(tName, FPath)
handleTable(interfaceTable)

"""
#set the temporary file and get the connection
i = 0
k = 1
while i < 1:

    try:
        FPath = sys.argv[1]
        tName = FPath[FPath.rfind("\\")+1:FPath.rfind(".mem")]
        interfaceTable = Cards.Table(tName, sys.argv[1])
        handleTable(interfaceTable)
        i += 1
    except:
        FPath = dirTemp + str(k) + '.mem'
        tName = FPath[FPath.rfind("\\")+1:FPath.rfind(".mem")]
        interfaceTable = Cards.Table(tName, FPath)
        handleTable(interfaceTable)
        k += 1
        i += 1
    else:
        pass

print ("temporary file: " + tName + " at: " + FPath)

"""

file_menu.add_command(
    label = 'New Table',
    command = CreateNewTable
)

file_menu.add_command(
    label = 'Open Table',
    command = OpenTable
)

file_menu.add_command(
    label = 'Save Table',
    command = SaveTable
)

menubar.add_cascade(
    label = 'File',
    menu = file_menu,
    underline = 0
)

window.config(menu = menubar)
window.geometry('500x500')
window.title('Memory Cards')


Hierarchy.bind('<<TreeviewSelect>>', itemSelect)

window.mainloop()