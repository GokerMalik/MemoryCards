from asyncio.windows_events import NULL
from sre_parse import State
import tkinter
from tkinter import BooleanVar, IntVar, ttk
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

#menu Open Table    
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

#menu Save Table
def SaveTable():

    if (interfaceTable.sql3 == NoneType):
        interfaceTable.connect()
        interfaceTable.sql3.saveTable()
        interfaceTable.disconnect()

#define item activation/disactivation
def ActiveItem(button):
    button.config(state = 'normal')
def deActiveItem(button):
    button.config(state = 'disabled')

#define hierarchy events
def itemSelect(event):

    #Always strart by setting all to back their defaults.
    deActiveItem(DelCat)
    deActiveItem(CreateDeck)

    DeckNameInfo.config(text = "No deck is selected")
    DeckNameBox.config(state = 'disabled')
    CardNumLabel.config(state = 'disabled', text = '*')
    CardNum.config(state = 'disabled')
    AskFrontBox.config(state = 'disabled')
    AskBackBox.config(state = 'disabled')

    #Get the recent list of the selection
    selectedCats, selectedDecks = collectHierarchy()

    #work through scenarios

    ##  NoCat NoDeck -- Keep default

    ##  OneCat noDeck -- Only one selection and it is a category
    if (len(selectedCats) == 1 and len(selectedDecks) == 0):
        ActiveItem(DelCat)
        ActiveItem(CreateDeck)

    ##  MultiCat NoDeck -- Multiple categories but no deck selected
    if (len(selectedCats) > 1 and len(selectedDecks) == 0):
        ActiveItem(DelCat)

    ##  NoCat OneDeck -- Not possible, selecting a deck automatically calls its cat

    ##  OneCat OneDeck -- Only when the deck belongs to the category.
    if (len(selectedCats) == 1 and len(selectedDecks) == 1):
        ActiveItem(DelCat)


    ##MultiCat OneDeck -- Multiple categories are selected, also one deck belongs one of them



    ##NoCat MultiDeck -- Not possibble

    ##OneCat MultiDeck -- All the decks belongs to the same cateogry.

    ##MultiCat MultiDeck -- decks in different categories or decks in the same + at least one category diffrent than their parent.



    if (len(selectedCats)!=0):
        ActiveItem(DelCat)
        ActiveItem(CreateDeck)

    if len(selectedDecks) == 1:
        selDeckList = list(selectedDecks.items())
        CardNum.config(text = selDeckList[0][1].cardNum)
        DeckNameInfo.config(text = "Deck Name")

    if len(strDeckName.get()) != 0:
        ActiveItem(CreateDeck)
     
#Update hierarchy Table
def hierUpdate():

    for i in Hierarchy.get_children():
        Hierarchy.delete(i)

    catInd = 1
    for cat in interfaceTable.cats:
        Hierarchy.insert('', tkinter.END, text = cat, iid = catInd, open = True)
        deckInd = catInd*100
        for deck in interfaceTable.cats[cat].decks:
            Hierarchy.insert('', tkinter.END, text = deck, iid = deckInd, open = False)
            Hierarchy.move(deckInd, catInd, deckInd)
            deckInd += 1
        catInd +=1

#collect from hierarchy table
def collectHierarchy():

    #create two dictionaries to make it sure that registering all items for once.
    selectedCategories = dict()
    selectedDecks = dict()

    #find a way to differentiate between cats and decks, check the function above.
    for selectedItem in Hierarchy.selection():

        item = Hierarchy.item(selectedItem)
        parent_iid = Hierarchy.parent(selectedItem)

        #If it has a parent ID, then it is a deck. Otherwise, category
        if parent_iid:
            #Scan the memory to find what category matches with the deck's parent
            for cat in interfaceTable.cats:
                if Hierarchy.item(parent_iid)['text'] == interfaceTable.cats[cat].nameCat:
                    #If the deck is selected, automatically count its parent.
                    selectedCategories.update({interfaceTable.cats[cat].nameCat:interfaceTable.cats[cat]})
                    #scan the memory to see what which deck in the category makes a match with the selection
                    for deck in interfaceTable.cats[cat].decks:
                        if item['text'] == interfaceTable.cats[cat].decks[deck].nameDeck:
                            #register the deck
                            selectedDecks.update({item['text']:interfaceTable.cats[cat].decks[deck]})
                            break
                    break
        #if it doesn't have a parent ID, then it must be a category. Register the selection.
        else:
            for cat in interfaceTable.cats:
                if item['text'] == interfaceTable.cats[cat].nameCat:
                    selectedCategories.update({item['text']:interfaceTable.cats[cat]})
                    break

    return selectedCategories, selectedDecks

#define deckNameBox events
def DeckNameChange(deckName):

    ActiveItem(CreateDeck)
    activate = False

    if len(deckName.get()) != 0:
        selectedCats, d = collectHierarchy()
        if len(selectedCats) == 1:
            activate = True

    if activate:
        pass
    else:
        deActiveItem(CreateDeck)

#Define button functions
def newCategory():

    nameCategory = tkinter.simpledialog.askstring("Input", 'Category name:', parent = window)

    if nameCategory:
        Cards.Category(nameCategory, interfaceTable)
        hierUpdate()

#command deleteCategory
def deleteCategory():

    selectedCats, d= collectHierarchy()

    for cat in selectedCats:
        interfaceTable.deleteCat(selectedCats[cat])

    hierUpdate()
    deActiveItem(DelCat)

#command modifyCategory
def modifyCategory():
    pass

#command newDeck
def newDeck():

    selectedCats, selectedDecks = collectHierarchy()

    if len (selectedCats == 1):

        askFr = BooleanVar(value = aFR)
        askBc = BooleanVar(value = aBC)

        Cards.Deck(selectedCats[0], strDeckName.get(), askFr, askBc)
        hierUpdate()

#command modifyDeck
def modifyDeck():
    pass

#command deleteDeck
def deleteDeck():
    pass

#LeftFrame
def setLeftFrame():
    frameLeft = tkinter.Frame(window)
    frameLeft.pack(side = 'left', fill = 'y')

    return frameLeft

#hierarchyFrame
def SetHierarchyFrame():

    #create hierarchy frame
    frameHierarchy = tkinter.Frame(leftFrame)
    frameHierarchy.pack(side='top', fill = 'y')

    #Create table hierarchy
    hierarchy = tkinter.ttk.Treeview(frameHierarchy)
    hierarchy.pack(side = 'top', fill = 'y')

    #Create label frame
    labCatsFrame = tkinter.Frame(frameHierarchy)
    labCatsFrame.pack(side = 'top', fill = 'x')

    #Label cateogr buttons
    labCategories = tkinter.Label(labCatsFrame, text = 'Categories:')
    labCategories.pack(side = 'left')

    #Create hiearchy buttons frame
    frameHiearchyButtons = tkinter.Frame(frameHierarchy)
    frameHiearchyButtons.pack(side = 'top', fill = 'x')

    #New category button
    butNewCat = tkinter.Button(frameHiearchyButtons, text = 'Category', command = newCategory, state = 'disabled')
    butNewCat.pack(side = 'left', pady = 10, padx = 3)

    #Delete category button
    butDelCat = tkinter.Button(frameHiearchyButtons, text = 'Delete', command = deleteCategory, state = 'disabled')
    butDelCat.pack(side = 'left', pady = 8, padx = 3)

    #Modify category button
    butModCat = tkinter.Button(frameHiearchyButtons, text = 'Modify', command = modifyCategory, state = 'disabled')
    butModCat.pack(side = 'left', pady = 8, padx = 3)

    return hierarchy, butNewCat, butDelCat, butModCat

#deck info frame
def setDeckInfoFrame():

    #Set deckinfLab frame
    FrDeckInfLab = tkinter.Frame(leftFrame)
    FrDeckInfLab.pack(side = 'top', fill = 'x')

    #set decks label
    DeckInfLab = tkinter.Label(FrDeckInfLab, text = 'Decks:')
    DeckInfLab.pack(side = 'left')

    #Set deck info frame
    frDeckInf = tkinter.Frame(leftFrame, widt = 200, height = 500, borderwidth= 3, relief= 'sunken')
    frDeckInf.pack(side = 'top', pady = 3, fill = 'x' )

    #set the nameLabelFrame
    frDeckNamLab = tkinter.Frame(frDeckInf)
    frDeckNamLab.pack(side = 'top', fill = 'x')

    #set the name label
    labelDeckName = tkinter.Label(frDeckNamLab, text = "No deck is selected")
    labelDeckName.pack(side = 'left', padx = 8, pady = 3, fill = 'x')

    #set the name input
    entryDeckName = tkinter.Entry(frDeckInf, textvariable = strDeckName, state = 'disabled')
    entryDeckName.pack(side = 'top', padx = 8, pady = 3, fill = 'x')

    ############################
    #DeckNumber#

    frDeckNum = tkinter.Frame(frDeckInf)
    frDeckNum.pack(side = 'top', fill = 'x')

    labelCardNum = tkinter.Label(frDeckNum, text = "Number of cards:", state = 'disabled')
    labelCardNum.pack(side = 'left', padx = 8, pady = 3, fill = 'x')

    numCardNum = tkinter.Label(frDeckNum, text = "*", state = 'disabled')
    numCardNum.pack(side = 'right', padx = 10)

    ############################
    #CheckBox#

    #set front ask front frame
    frameAskFront = tkinter.Frame(frDeckInf)
    frameAskFront.pack(side = 'top', fill = 'x')

    #set ask front checkbox
    checkAskFront = tkinter.Checkbutton(frameAskFront, text = 'Ask Front', variable = aFR, onvalue=1, offvalue=0, state = 'disabled')
    checkAskFront.pack(side = 'left', fill = 'x', padx = 5)

    #set front ask front frame
    frameAskBack = tkinter.Frame(frDeckInf)
    frameAskBack.pack(side = 'top', fill = 'x')

    #set ask back checkbox
    checkAskBack = tkinter.Checkbutton(frameAskBack, text = 'Ask Back', variable = aBC, onvalue=1, offvalue=0, state = 'disabled')
    checkAskBack.pack(side = 'left', fill = 'x', padx = 5)
    
    return labelDeckName, entryDeckName, labelCardNum, numCardNum, checkAskFront, checkAskBack

#Deck buttons Frame
def setDeckControlFrame():

    #Deck Control Frame
    frDeckCont = tkinter.Frame(leftFrame)
    frDeckCont.pack(side = 'top', fill = 'x')

    #newDeck button
    newDeckButton = tkinter.Button(frDeckCont, text = "Create Deck", command = newDeck, state = 'disabled')
    newDeckButton.pack(side = 'left')

    #ModfiyDeck Button
    modifyDeckButton = tkinter.Button(frDeckCont, text = "Modify Deck", command = modifyDeck, state = 'disabled')
    modifyDeckButton.pack(side = 'left')

    return newDeckButton, modifyDeck

#handleTable
def handleTable(table):

    #set the heading of the hieararchy table
    Hierarchy.heading('#0', text=table, anchor = tkinter.W)


    table.connect()

    #fetch the existing decks in the table

    resCats = table.sql3.curs.execute("SELECT categoryCol FROM cats").fetchall()
    resDecks = table.sql3.curs.execute("SELECT deckCol from decks").fetchall()

    table.disconnect()

    ActiveItem(NewCat)
    hierUpdate()

#Set main window
window = tkinter.Tk()

#Set entry box
strDeckName = tkinter.StringVar()
strDeckName.trace("w", lambda *args: DeckNameChange(strDeckName))

#get home directory and temporary directory
homeDir = os.path.expanduser('~')
dirTemp = homeDir + fr'\AppData\Roaming\MemoryCards\temp'

#get frames and widgets
aFR = IntVar(value = 0)
aBC = IntVar(value = 1)

leftFrame = setLeftFrame()

Hierarchy, NewCat, DelCat, ModCat = SetHierarchyFrame()
DeckNameInfo, DeckNameBox, CardNumLabel, CardNum, AskFrontBox, AskBackBox = setDeckInfoFrame()
CreateDeck, EditDeck = setDeckControlFrame()

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
window.geometry('600x550')
window.title('Memory Cards')

#Hieararchy Event
Hierarchy.bind('<<TreeviewSelect>>', itemSelect)

window.mainloop()