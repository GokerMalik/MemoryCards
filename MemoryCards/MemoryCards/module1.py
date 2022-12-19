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


######################################################

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

######################################################

#define hierarchy events
def itemSelect(event):

    #Always strart by setting all to back their defaults.
    deActiveItem(DelCat)
    deActiveItem(ModCat)

    deActiveItem(CreateDeck)
    deActiveItem(DeleteDeck)
    deActiveItem(ModifyDeck)

    DeckNameInfo.config(text = "No deck is selected")
    strDeckName.set("")
    DeckNameBox.config(state = 'disabled')
    CardNumLabel.config(state = 'disabled', text = 'Number of cards:')
    CardNum.config(state = 'disabled', text = "*")
    AskFrontBox.config(state = 'disabled')
    AskBackBox.config(state = 'disabled')

    #also clean the cards in the card table
    for i in CardList.get_children():
        CardList.delete(i)
    CardList.heading('#0', text='', anchor = tkinter.W)

    #Get the recent list of the selection
    selectedCats, calledCats, selectedDecks = collectHierarchy()

    #work through scenarios

    ##  NoCatSelection - NoCatCall - NoDeck
    #Keep default

    ##  OneCatSelection - NoCatCall - noDeck ::
    if (len(selectedCats) == 1 and len(calledCats) == 0 and len(selectedDecks) == 0):
        ActiveItem(DelCat)
        ActiveItem(ModCat)

        ActiveItem(CreateDeck)

        
        DeckNameInfo.config(text = "Create a deck?")

        DeckNameBox.config(state = 'normal')

        AskFrontBox.config(state = 'normal')
        AskBackBox.config(state = 'normal')
        

    ##  MultiCatSelection - NoCatCall - NoDeck ::
    if (len(selectedCats) > 1 and len(calledCats) == 0 and len(selectedDecks) == 0):
        ActiveItem(DelCat)

        DeckNameInfo.config(text = "*")

    ####################################################

    ##  NoCatSelection - OneCatCall - OneDeck ::
    if (len(selectedCats) == 0 and len(calledCats) == 1 and len(selectedDecks) == 1):
        ActiveItem(CreateDeck)
        ActiveItem(DeleteDeck)
        ActiveItem(ModifyDeck)

        DeckNameInfo.config(text = "Deck Name:")
        strDeckName.set(list(selectedDecks.values())[0].nameDeck)
        DeckNameBox.config(state = 'normal')
        CardNumLabel.config(state = 'normal')
        CardNum.config(state = 'normal', text = list(selectedDecks.values())[0].cardNum )
        AskFrontBox.config(state = 'normal')
        AskBackBox.config(state = 'normal')

        deck = list(selectedDecks.values())[0]
        updateCards(deck)



    ##  OneCatSelection - OneCatCall - OneDeck ::
    if (len(selectedCats) == 1 and len(calledCats) == 1 and len(selectedDecks) == 1):

        ###What if the selected cat is the parent of the selected deck

        ActiveItem(ModCat)
        ActiveItem(DelCat)

        if list(calledCats.values())[0] == list(calledCats.values())[0]:
            ActiveItem(CreateDeck)

        ActiveItem(DeleteDeck)
        ActiveItem(ModifyDeck)

        DeckNameInfo.config(text = "Deck Name:")
        strDeckName.set(list(selectedDecks.values())[0].nameDeck)
        DeckNameBox.config(state = 'normal')
        CardNumLabel.config(state = 'normal')
        CardNum.config(state = 'normal', text = list(selectedDecks.values())[0].cardNum )
        AskFrontBox.config(state = 'normal')
        AskBackBox.config(state = 'normal')

        deck = list(selectedDecks.values())[0]
        updateCards(deck)

    ##  MultiCatSelection - OneCatCall - OneDeck ::

    if (len(selectedCats) > 1 and len(calledCats) == 1 and len(selectedDecks) == 1):

        ActiveItem(DelCat)

        ActiveItem(DeleteDeck)
        ActiveItem(ModifyDeck)

        DeckNameInfo.config(text = "Deck Name:")
        strDeckName.set(list(selectedDecks.values())[0].nameDeck)
        DeckNameBox.config(state = 'normal')
        CardNumLabel.config(state = 'normal')
        CardNum.config(state = 'normal', text = list(selectedDecks.values())[0].cardNum )
        AskFrontBox.config(state = 'normal')
        AskBackBox.config(state = 'normal')

        deck = list(selectedDecks.values())[0]
        updateCards(deck)

    #####################################################

    ##  NoCatSelection - OneCatCall - MultiDeck ::

    if (len(selectedCats) == 0 and len(calledCats) == 1 and len(selectedDecks) > 1):

        ActiveItem(CreateDeck)
        ActiveItem(DeleteDeck)
        ActiveItem(ModifyDeck)

        DeckNameInfo.config(text = "Deck Name:")
        strDeckName.set("Multiple")
        CardNum.config(text = "Multiple")
   
    ##  OneCatSelection - OneCatCall - MultiDeck ::
    if len(selectedCats) == 1 and len(calledCats) == 1 and len(selectedDecks)>1:

        ActiveItem(ModCat)
        ActiveItem(DelCat)

        ###What if the selected cat is the parent of the selected decks
        if list(calledCats.values())[0] == list(calledCats.values())[0]:
            ActiveItem(CreateDeck)

        ActiveItem(DeleteDeck)

        DeckNameInfo.config(text = "Deck Name:")
        strDeckName.set("Multiple")
        CardNum.config(text = "Multiple")

    ##  MultiCatSelection - OneCatCall - MultiDeck ::


    if len(selectedCats) >1 and len(calledCats) == 1 and len(selectedDecks) >1:

        ActiveItem(DelCat)
        ActiveItem(DeleteDeck)

        DeckNameInfo.config(text = "Deck Name:")
        strDeckName.set("Multiple")
        CardNum.config(text = "Multiple")

    ##  NoCatSelection - MultiCatCall - MultiDeck ::

    if len(selectedCats) == 0 and len(calledCats) > 1 and len(selectedDecks) > 1:

        ActiveItem(DeleteDeck)

        DeckNameInfo.config(text = "Deck Name:")
        strDeckName.set("Multiple")
        CardNum.config(text = "Multiple")

    ##  OneCatSelection - MultiCatCall - MultiDeck ::

    if len(selectedCats) == 1 and len(calledCats) > 1 and len(selectedDecks) > 1:

        ActiveItem(DelCat)
        ActiveItem(ModCat)

        ActiveItem(DeleteDeck)

        DeckNameInfo.config(text = "Deck Name")
        strDeckName.set("Multiple")
        CardNum.config(text = "Multiple")

    ##  MultiCatSelection - MultiCatCall - MultiDeck ::

    if len(selectedCats) > 1 and len(calledCats) > 1 and len(selectedDecks)>1:
        ActiveItem(DelCat)
        ActiveItem(DeleteDeck)

        DeckNameInfo.config(text = "Deck Name:")
        strDeckName.set("Multiple")

        CardNum.config(text = "Multiple")

    if len(strDeckName.get()) != 0:
        ActiveItem(CreateDeck)
     

#define cardlist events
def cardSelect(event):

    pass

    

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

#Update card table
def updateCards(deck):
    
    for i in CardList.get_children():
        CardList.delete(i)

    CardList.heading('#0', text=deck, anchor = tkinter.W)

    if len(deck.cards) != 0:

        CardList.insert('', tkinter.END, text = 'Fronts', iid = 1, open = False)
        CardList.insert('', tkinter.END, text = 'Backs', iid = 2, open = False)

        cardFrInd = 101
        cardBcInd = 201

        for card in deck.cards:
            CardList.insert('',tkinter.END, text = deck.cards[card].front, iid = cardFrInd, open = False)
            CardList.move(cardFrInd, 1, cardFrInd)

            CardList.insert('',tkinter.END, text = deck.cards[card].back, iid = cardBcInd, open = False)
            CardList.move(cardBcInd, 2, cardBcInd)

            cardFrInd += 1
            cardBcInd += 1


#collect from hierarchy table
def collectHierarchy():

    #create three dictionaries to make it sure that registering all items for once.
    selectedCategories = dict()
    calledCategories = dict()
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
                    #If the deck is selected, call its parent.
                    calledCategories.update({interfaceTable.cats[cat].nameCat:interfaceTable.cats[cat]})
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

    return selectedCategories, calledCategories, selectedDecks

#collect cards
def collectCards(deck):

    #Create a dictionary to register all the items for once.
    selectedCards = dict()

    for selectedItem in CardList.selection():

        item = CardList.item(selectedItem)
        parent_iid = CardList.parent(selectedItem)

        if parent_iid == 1:
            for card in deck.cards:
                if item['text'] == deck.cards[card].front:
                    selectedCards.update({item['text']:deck.cards[card]})
                    break
        elif parent_iid == 2:
            for card in deck.cards:
                if item['text'] == deck.cards[card].back:
                    selectedCards.update({item['text']:deck.cards[card]})
                    break
        else:
            pass

    return selectedCards

#define deckNameBox events
def DeckNameChange(deckName):

    ActiveItem(CreateDeck)
    activate = False

    totalCats = dict()

    if len(deckName.get()) != 0:
        selectedCats, calledCats, d = collectHierarchy()
        totalCats.update(selectedCats)
        totalCats.update(calledCats)

        if len(totalCats) == 1:
            activate = True

    if activate:
        pass
    else:
        deActiveItem(CreateDeck)

    return deckName

########################################################

#command newCategory
def newCategory():

    nameCategory = tkinter.simpledialog.askstring("Input", 'Category name:', parent = window)

    if nameCategory:
        Cards.Category(nameCategory, interfaceTable)
        hierUpdate()

#command deleteCategory
def deleteCategory():

    selectedCats, cc, d= collectHierarchy()

    for cat in selectedCats:
        selectedCats[cat].release()

    hierUpdate()
    deActiveItem(DelCat)

#command modifyCategory
def modifyCategory():

    nameCategory = tkinter.simpledialog.askstring("Input", 'Category name:', parent = window)

    if len(nameCategory) > 0:

        selectedCats, cc, d = collectHierarchy()

        cat = list(selectedCats.values())[0]
        cat.UpdateCat(nameCategory)

    hierUpdate()

#command newDeck
def newDeck():

    selectedCats, calledCats, selectedDecks = collectHierarchy()
    totalCats = dict()
    totalCats.update(selectedCats)
    totalCats.update(calledCats)

    askFr = BooleanVar(value = aFR.get())
    askBc = BooleanVar(value = aBC.get())

    Cards.Deck(list(totalCats.values())[0], strDeckName.get(), askFr, askBc)
    hierUpdate()

#command modifyDeck
def modifyDeck():

    sc, cc, selectedDecks = collectHierarchy()

    askFr = BooleanVar(value = aFR.get())
    askBc = BooleanVar(value = aBC.get())

    deck = list(selectedDecks.values())[0]
    deck.updateDeck(deck.category, strDeckName.get(), askFr, askBc)

#command deleteDeck
def deleteDeck():
    
    sc, cc, selectedDecks = collectHierarchy()

    for deck in selectedDecks:
        selectedDecks[deck].release()

    hierUpdate()

#command newCard
def newCard():
    sc, cc, selectedDecks = collectHierarchy()

    deck = list(selectedDecks.values())[0]
    Cards.Card(deck, cardFront.get('1.0', 'end'), cardBack.get('1.0', 'end'))

    updateCards(deck)

#command deleteCard
def deleteCard():

    pass

#command modifyCard
def modifyCard():

    pass

#########################################################

#LeftFrame
def setLeftFrame():
    frameLeft = tkinter.Frame(window)
    frameLeft.pack(side = 'left', fill = 'y')

    return frameLeft

#RightFrame
def setRightFrame():
    frameRight = tkinter.Frame(window)
    frameRight.pack(side = 'right', fill = 'y')

    return frameRight

#MidFrame
def setMidFrame():
    frameMid = tkinter.Frame(window)
    frameMid.pack(side = 'top', fill = 'both')

    return frameMid

#hierarchyFrame
def SetHierarchyFrame():

    #create hierarchy frame
    frameHierarchy = tkinter.Frame(leftFrame)
    frameHierarchy.pack(side='top', fill = 'y')

    #Create label frame
    labCatsFrame = tkinter.Frame(frameHierarchy)
    labCatsFrame.pack(side = 'top', fill = 'x')

    #Label category buttons
    labCategories = tkinter.Label(labCatsFrame, text = 'Categories:')
    labCategories.pack(side = 'left')

    #Create table hierarchy
    hierarchy = tkinter.ttk.Treeview(frameHierarchy)
    hierarchy.pack(side = 'top', fill = 'y')

    #Create hiearchy buttons frame
    frameHiearchyButtons = tkinter.Frame(frameHierarchy)
    frameHiearchyButtons.pack(side = 'top', fill = 'x')

    #New category button
    butNewCat = tkinter.Button(frameHiearchyButtons, text = 'Create', command = newCategory, state = 'disabled')
    butNewCat.pack(side = 'left', pady = 5, padx = 3)

    #Delete category button
    butDelCat = tkinter.Button(frameHiearchyButtons, text = 'Delete', command = deleteCategory, state = 'disabled')
    butDelCat.pack(side = 'left', pady = 5, padx = 3)

    #Modify category button
    butModCat = tkinter.Button(frameHiearchyButtons, text = 'Modify', command = modifyCategory, state = 'disabled')
    butModCat.pack(side = 'left', pady = 5, padx = 3)

    return hierarchy, butNewCat, butDelCat, butModCat

#deck info frame
def setDeckInfoFrame():

    #Set deckinfLab frame
    FrDeckInfLab = tkinter.Frame(leftFrame)
    FrDeckInfLab.pack(side = 'top', fill = 'x')

    #set decks label
    DeckInfLab = tkinter.Label(FrDeckInfLab, text = 'Deck Info:')
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
    newDeckButton = tkinter.Button(frDeckCont, text = "Create", command = newDeck, state = 'disabled')
    newDeckButton.pack(side = 'left', padx = 3, pady = 5)

    #DeleteDeck button
    deleteDeckButton = tkinter.Button(frDeckCont, text = "Delete", command = deleteDeck, state = 'disabled')
    deleteDeckButton.pack(side = 'left', padx = 3, pady = 5)

    #ModfiyDeck Button
    modifyDeckButton = tkinter.Button(frDeckCont, text = "Modify", command = modifyDeck, state = 'disabled')
    modifyDeckButton.pack(side = 'left', padx = 3, pady = 5)

    return newDeckButton, deleteDeckButton, modifyDeckButton

#Card Frame
def setCardFrame():

    labCardsFrame = tkinter.Frame(rightFrame)
    labCardsFrame.pack(side = 'top', fill = 'x')

    frameCards = tkinter.Frame(rightFrame)
    frameCards.pack(side = 'top', fill = 'y')

    labelCards = tkinter.Label(labCardsFrame, text = 'Cards:')
    labelCards.pack(side = 'left')

    CardList = tkinter.ttk.Treeview(frameCards)
    CardList.pack(side = 'top', fill = 'y')

    return CardList

#card info frame
def setCardInfoFrame():
    #Set cardinfLab frame
    FrCardInfLab = tkinter.Frame(rightFrame)
    FrCardInfLab.pack(side = 'top', fill = 'x')

    #set cards label
    CardInfLab = tkinter.Label(FrCardInfLab, text = 'Card Info:')
    CardInfLab.pack(side = 'left')

    #Set cards info frame
    frCardInf = tkinter.Frame(rightFrame, widt = 200, height = 500, borderwidth= 3, relief= 'sunken')
    frCardInf.pack(side = 'top', pady = 3, fill = 'x' )

    #set the frame for front labels
    frCardFrontLabel = tkinter.Frame(frCardInf)
    frCardFrontLabel.pack(side = 'top', fill = 'x')

    labelCardFront = tkinter.Label(frCardFrontLabel, text = "Card Front:")
    labelCardFront.pack(side = 'left', padx = 8, pady = 3)

    #set the frame for front entries
    frCardFrontEntry = tkinter.Frame(frCardInf)
    frCardFrontEntry.pack(side = 'top', fill = 'x')

    entryCardFront = tkinter.Text(frCardFrontEntry, state = 'normal', height = 2, width = 20)
    entryCardFront.pack(side = 'left', padx = 8, pady = 3)

    #set the name label
    frCardBackLabel = tkinter.Frame(frCardInf)
    frCardBackLabel.pack(side = 'top', fill = 'x')

    entryCardBack = tkinter.Label(frCardBackLabel, text = "Card Back:")
    entryCardBack.pack(side = 'left', padx = 8, pady = 3, fill = 'x')

    #set the name input
    frCardBackEntry = tkinter.Frame(frCardInf)
    frCardBackEntry.pack(side = 'top', fill = 'x')

    entryCardBack = tkinter.Text(frCardBackEntry, state = 'normal', height = 2, width = 20)
    entryCardBack.pack(side = 'left', padx = 8, pady = 3)

    #########################################

    frCardTogs = tkinter.Frame(frCardInf)
    frCardTogs.pack(side = 'top', fill = 'x')

    #ShowFronts
    FrontTogBut = tkinter.Button(frCardTogs, text = 'Show Fronts')
    FrontTogBut.pack(side = 'left', padx = 3, pady = 5)

    #ShowBacks
    BackTogBut = tkinter.Button(frCardTogs, text = 'Show Backs')
    BackTogBut.pack(side = 'left', padx = 3, pady = 5)

    #########################################

    frCardBut = tkinter.Frame(rightFrame)
    frCardBut.pack(side = 'top', fill = 'x')

    CreateBut = tkinter.Button(frCardBut, text = 'Create', command = newCard)
    CreateBut.pack(side = 'left', fill = 'x', pady = 5, padx = 3)

    DelBut = tkinter.Button(frCardBut, text = 'Delete')
    DelBut.pack(side = 'left', fill = 'x', pady = 5, padx = 3)

    ModBut = tkinter.Button(frCardBut, text = 'Modify')
    ModBut.pack(side = 'left', fill = 'x', pady = 5, padx = 3)

    return labelCardFront, entryCardFront, entryCardBack

#sessionFrame
def setSessionFrame():
    Question = tkinter.Canvas(midFrame, bg = '#aee1e5', height = 200, width = 300)
    Question.pack(side = 'top', padx = 20, pady = 15)

#handleTable
def handleTable(table):

    #set the heading of the hieararchy table
    Hierarchy.heading('#0', text=table, anchor = tkinter.W)


    table.connect()

    #fetch the existing decks in the table

    resCats = table.sql3.curs.execute("SELECT categoryCol FROM cats").fetchall()
    resDecks = table.sql3.curs.execute("SELECT deckCol from decks").fetchall()
    resCards = table.sql3.curs.execute("SELECT cardCol from cards").fetchall()

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

#set left frame
leftFrame = setLeftFrame()

Hierarchy, NewCat, DelCat, ModCat = SetHierarchyFrame()
DeckNameInfo, DeckNameBox, CardNumLabel, CardNum, AskFrontBox, AskBackBox = setDeckInfoFrame()
CreateDeck, DeleteDeck, ModifyDeck = setDeckControlFrame()

#set right framwe
rightFrame = setRightFrame()

CardList = setCardFrame()
CardNameInfo, cardFront, cardBack = setCardInfoFrame()

#setMidFrame
midFrame = setMidFrame()

setSessionFrame()

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
window.geometry('800x550')
window.title('Memory Cards')

#Hieararchy Event
Hierarchy.bind('<<TreeviewSelect>>', itemSelect)
CardList.bind('<<TreeviewSelect>>', cardSelect)

window.mainloop()