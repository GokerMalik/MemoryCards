import random
import os
import tkinter
import tkinter.messagebox
import csv

###########################################################

###################CONFIGURATIONS##########################

main_dir = os.getcwd()[0:os.getcwd().rfind("MemoryCards")]
data_dir = main_dir + "data.csv"

decks = {"Default"}

selectedDeck = ''

#create a window instance
window = tkinter.Tk()
window.geometry("500x500")
window.title("Memory")

#create data file if doesn't exist
SetFile = open(data_dir, 'a', encoding = 'UTF-8', newline='')
SetFile.close()

CheckFile = open(data_dir, 'r', encoding = 'UTF-8', newline='')
reader = csv.reader(CheckFile)
rows = list(reader)
rowNum = len(rows)

#Write the heading if the file is newly created.
if (rowNum==0):
    CheckFile.close()
    OptimiseFile = open(data_dir, 'a', encoding = 'UTF-8', newline='')
    newline = csv.writer(OptimiseFile)
    newline.writerows([['Front Side','Back Side','Deck']])
    OptimiseFile.close()

#Update the local Decks variable with the existing file content
else:
    for item in rows[1:]:   #exclude the heading
        new_key = {item[2]}
        decks.update(new_key)
    CheckFile.close()

#check the existing decks and turn them into tk variable
deckList = list(decks)
tkDecks = tkinter.StringVar(value = deckList)


#define the cards
class cards:
    def __init__(self, frontSide, backSide, Deck):
        self.frontSide = frontSide
        self.backSide = backSide
        self.Deck = Deck



#define frames
ListLocation = tkinter.Frame(window, bg = 'blue')
ListFrame = tkinter.Frame(ListLocation, height = 300, width = 200, bg = 'red')
FrontFrame = tkinter.Frame(ListLocation, height = 300, width = 200, bg = 'red')
InputFrame = tkinter.Frame(window, bg = 'red')
CheckFrame = tkinter.Frame(window)
ShowHideFrame = tkinter.Frame(ListLocation, width = 200)

### define what buttuons do ####

#function to save the new card
def newcard(side1, side2, deck):

    #check entries
    if (len(side2)==0 and len(deck)==0):
        tkinter.messagebox.showinfo(window, message = "At least one side of the card must have an entry")
        return 1

    #create the card
    card = cards(side1, side2, deck)

    #get the deck information
    if (len(card.Deck)) == 0:
        card.Deck = 'Default'

    #update the file
    GetExisting = open(data_dir, 'r', encoding = 'UTF-8', newline='')
    existing = csv.reader(GetExisting)
    ExistingEntries = []

    for line in existing:
        ExistingEntries.append(list)
        if (line[2] == card.Deck and (line[0] == card.frontSide or line[1] == card.backSide)):
            tkinter.messagebox.showinfo(window, message = "At least one side of the card already exist in the desk")
            GetExisting.close()
            return 1

    #update the deck dictionary
    new_key = {card.Deck}
    decks.update(new_key)

    #update the file
    WriteFile = open(data_dir, 'a', encoding = 'UTF-8', newline='')
    newline = csv.writer(WriteFile)
    newline.writerows([[card.frontSide, card.backSide, card.Deck]])
    WriteFile.close()
    tkinter.messagebox.showinfo(window, message = "Saved")

    #updare the decklist
    current_list = deckList.get(0, 'end')
    for CURRENT in current_list:
        if (CURRENT == card.Deck):
            return 0
    deckList.insert('end', card.Deck)

    return 0

#Define show fronts
def showFronts():
    selected = deckList.curselection()

    if (len(selected) == 0):
        tkinter.messagebox.showinfo("No selection", message = "Please select a desk from the menu above")
        return 1
    else:
        global selectedDeck
        selectedDeck = deckList.get(selected)
        FrontList.delete(0, 'end')
        GetCards = open(data_dir, 'r', encoding = 'UTF-8', newline='')
        reader = csv.reader(GetCards)
        AllCards = list(reader)
        GetCards.close()

        for card in AllCards:
            if (card[2] == selectedDeck):
                FrontList.insert('end', card[0])
        return 0

#Define hide fronts
def HideFronts():
    FrontList.delete(0, 'end')

#Define remove card
def RemoveCard():

    chosenCard = FrontList.curselection()

    if (len(chosenCard) == 0):
        tkinter.messagebox.showinfo("Please Select a Card, first")
        return 1
    else:

        GetCards = open(data_dir, 'r', encoding = 'UTF-8', newline='')
        reader = csv.reader(GetCards)
        FindCards = list(reader)
        GetCards.close()

        new_cards = []

        for curnCard in FindCards:
            if ((curnCard[2] != selectedDeck) or (curnCard[0] != FrontList.get(chosenCard))):
                new_cards.append(curnCard)

        file = open(data_dir, 'w', encoding = 'UTF-8', newline='')
        new_line = csv.writer(file)
        new_line.writerows(new_cards)
        file.close()

        FrontList.delete(chosenCard)

        return 0

#submit button
def submit():
    side1 = Entry1.get()
    side2 = Entry2.get()
    deck = Entry3.get()
    newcard(side1, side2, deck)

#check button
def check():
    print(AnswerBox.get() + " checked")


### creater entry box ####

#Answer Box
AnswerBox = tkinter.Entry(CheckFrame, font = ("Arial", 10))

#Front Side
Entry1 = tkinter.Entry(InputFrame)

#Back Side
Entry2 = tkinter.Entry(InputFrame)

#Deck
Entry3 = tkinter.Entry(InputFrame)

### create buttons ####

#Submit button
SubmitButton = tkinter.Button(InputFrame,
                   text = "Submit!",
                   command = submit
                   )

#check button
CheckButton = tkinter.Button(CheckFrame,
                   text = "Check!",
                   command = check
                   )

#ShowFronts button
ShowFronts = tkinter.Button(ShowHideFrame, text = "Show Cards", command = showFronts)

#HideFronts button
HideFronts = tkinter.Button(ShowHideFrame, text = "Hide Cards", command = HideFronts)

#RemoveCard button
RemoveCard = tkinter.Button(ListLocation, text = "Remove Card", command = RemoveCard)

#deck list
### Create listbox and scrollbar

deckList = tkinter.Listbox(ListFrame, listvariable=tkDecks, selectmode = 'Browse')
yScroll = tkinter.Scrollbar(ListFrame, orient = 'vertical', width = 16)

deckList.config(yscrollcommand=yScroll.set)
yScroll.config(command = deckList.yview)

### Create frontbox and scrollbar

FrontList = tkinter.Listbox(FrontFrame, selectmode = 'Browse')
FrontScroll = tkinter.Scrollbar(FrontFrame, orient = 'vertical', width = 16)

FrontList.config(yscrollcommand=FrontScroll.set)
FrontScroll.config(command = deckList.yview)

### locate items ####

#locate the lists, scroolbars
yScroll.pack(side='right', fill='y')
deckList.pack(side = 'right')

FrontScroll.pack(side='right', fill='y')
FrontList.pack(side = 'right')

#locate the answer box and the check button
AnswerBox.pack(side = 'left')
CheckButton.pack(side = 'right')

#Locate front and back labels
tkinter.Label(InputFrame,text = "Front").grid(row=1,column=0)
tkinter.Label(InputFrame,text = "Back").grid(row=2,column=0)
tkinter.Label(InputFrame,text = "Deck").grid(row=3,column=0)

#locate entry box
Entry1.grid(row=1,column=1)
Entry2.grid(row=2,column=1)
Entry3.grid(row=3,column=1)

#locate buttons
SubmitButton.grid(row=4, column=1)
ShowFronts.pack(side = 'left')
HideFronts.pack(side = 'right')

#locate frames
ListLocation.pack(side = 'right', fill = 'y')
ListFrame.pack(side = 'top')
InputFrame.place(x = 0, y= 0)
CheckFrame.pack(side = 'bottom', pady = 50)
ShowHideFrame.pack(side = 'top')

#locate front frame
FrontFrame.pack(side = 'top')

#locate remove button
RemoveCard.pack(side = 'top')

window.mainloop()