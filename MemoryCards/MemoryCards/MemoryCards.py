##THIS FILE IS TO BE REPLACED WITH Module1


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

### Set global variables
selectedDeckInd = []
selectedDeck = ''
sessionStatus = 0
checkMessage = 0
Response = ''
questions = []
correctAnswer = ''
QuestionNum = -1
sides = [0,1]


encoding = 'utf-8'

#create a window instance
window = tkinter.Tk()
window.geometry("500x500")
window.title("Memory")

#create data file if doesn't exist
SetFile = open(data_dir, 'a', encoding = encoding, newline='')
SetFile.close()

CheckFile = open(data_dir, 'r', encoding = encoding, newline='')
reader = csv.reader(CheckFile)
rows = list(reader)
rowNum = len(rows)

#Write the heading if the file is newly created.
if (rowNum==0):
    CheckFile.close()
    OptimiseFile = open(data_dir, 'a', encoding = encoding, newline='')
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


#define the cards   #I did not really had an object oriented approach, tbf. This part maybe can be optimised later.
class cards:
    def __init__(self, frontSide, backSide, Deck):
        self.frontSide = frontSide
        self.backSide = backSide
        self.Deck = Deck



#define frames
ListLocation = tkinter.Frame(window)
ListFrame = tkinter.Frame(ListLocation, height = 300, width = 200)
FrontFrame = tkinter.Frame(ListLocation, height = 300, width = 200)
InputFrame = tkinter.Frame(window)
CheckFrame = tkinter.Frame(window)
ShowHideFrame = tkinter.Frame(ListLocation, width = 200)
sessionFrame = tkinter.Frame(CheckFrame)
FrontBackFrame = tkinter.Frame(ListLocation)

### define what buttuons do ####

#function to save the new card
def newcard(side1, side2, deck):

    #check entries
    if (len(side2)==0 and len(deck)==0):
        tkinter.messagebox.showinfo("Empty Item", "At least one side of the card must have an entry")
        return 1

    #create the card
    card = cards(side1, side2, deck)

    #get the deck information
    if (len(card.Deck)) == 0:
        card.Deck = 'Default'

    #update the file
    GetExisting = open(data_dir, 'r', encoding = encoding, newline='')
    existing = csv.reader(GetExisting)
    ExistingEntries = []

    for line in existing:
        ExistingEntries.append(list)
        if (line[2] == card.Deck and (line[0] == card.frontSide and line[1] == card.backSide)):
            tkinter.messagebox.showinfo("Duplication", "At least one side of the card must be different than any other in the desk")
            GetExisting.close()
            return 1

    #update the deck dictionary (this part can be maybe removed later)
    new_key = {card.Deck}
    decks.update(new_key)

    #update the file
    WriteFile = open(data_dir, 'a', encoding = encoding, newline='')
    newline = csv.writer(WriteFile)
    newline.writerows([[card.frontSide, card.backSide, card.Deck]])
    WriteFile.close()
    tkinter.messagebox.showinfo("Success!!", "Saved")

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
        tkinter.messagebox.showinfo("No selection", "Please select a deck from the menu above")
        return 1
    else:
        global selectedDeck
        selectedDeck = deckList.get(selected)
        FrontList.delete(0, 'end')
        GetCards = open(data_dir, 'r', encoding = encoding, newline='')
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
        tkinter.messagebox.showinfo("no selection", "Please Select a Card, first")
        return 1
    else:

        GetCards = open(data_dir, 'r', encoding = encoding, newline='')
        reader = csv.reader(GetCards)
        FindCards = list(reader)
        GetCards.close()

        new_cards = []

        for curnCard in FindCards:
            if ((curnCard[2] != selectedDeck) or (curnCard[0] != FrontList.get(chosenCard))):
                new_cards.append(curnCard)

        file = open(data_dir, 'w', encoding = encoding, newline='')
        new_line = csv.writer(file)
        new_line.writerows(new_cards)
        file.close()

        FrontList.delete(chosenCard)

        return 0

#Start Session
def fStartSession():

    global sessionStatus
    global checkMessage
    global Response
    global questions
    global correctAnswer
    global QuestionNum
    global sides
    global selectedDeckInd

    if ((sessionStatus == 1) and (checkMessage == 0)):
        tkinter.messagebox.showinfo("Duplicated Sessions", "The session was already started")
        return 1

    if ((len(deckList.curselection()) == 0) and (checkMessage == 0)):
        tkinter.messagebox.showinfo("No selection", "Please select a deck from the list")
        return 1

    if (FrontInt.get()==0 and BackInt.get()==0):
        tkinter.messagebox.showinfo("No Sides", "Please select the sides that you would like to be questioned")
        return 1

    else:

        if (checkMessage == 0):                         #coming from the start session button
            file = open(data_dir, 'r', encoding = encoding, newline='')
            reader = csv.reader(file)
            allCards = list(reader)
            file.close()

            for quest in allCards:
                if (quest[2] == deckList.get(deckList.curselection())):
                    questions.append(quest)

            if len(questions) == 0:
                tkinter.messagebox.showinfo("Empty Deck", "There is no card in the selected deck")
                return 1

            Question.config(bg = '#aee1e5')

            sessionStatus = 1
            AskFront.config(state = 'disabled')
            AskBack.config(state = 'disabled')

            selectedDeckInd = deckList.curselection()

        else:                                           #coming from the check button

            sessionStatus = 1
            AskFront.config(state = 'disabled')
            AskBack.config(state = 'disabled')

            if (Response.casefold().strip() == correctAnswer.casefold().strip()):
                questions.remove(questions[QuestionNum])
                if (len(questions) == 0):
                    tkinter.messagebox.showinfo("Finished!!", "All the cards are finished")
                    checkMessage = 0
                    sessionStatus = 0
                    Question.itemconfig(text, text = '')
                    Question.itemconfig(feedBack, text = '')
                    Question.config(bg = '#f0f0f0')
                    AskFront.config(state = 'normal')
                    AskBack.config(state = 'normal')
                    return 0

            else:
                tkinter.messagebox.showinfo("Nope", "This isn't the correct anser\nThe correct solution is:\n \"" + correctAnswer + "\"")
       
        ##tell how many cards are left
        Question.itemconfig(feedBack, text = str(len(questions)) + " cards left")

        qIndices = list(range(0, len(questions)))
        QuestionNum = random.sample(qIndices, 1)[0]
        
        if (FrontInt.get() == 1 & BackInt.get() == 1):
            QuestionSide = random.sample(sides, 1)[0]
        elif (FrontInt.get() == 1):
            QuestionSide = 1
        else:
            QuestionSide = 0

        correctAnswer = questions[QuestionNum][QuestionSide*(-1)+(1)]   #cross-switch between 1 and 0

        ## Create question card
        if (len(questions[QuestionNum][QuestionSide]) > 10):
            showQuest = ''
            wordList = questions[QuestionNum][QuestionSide].split(" ")
            splitList = []
            
            for IND in range(len(wordList)):
                if (len(wordList[IND]) >10):

                    toModify = wordList[IND]
                    PieceNum = int(len(toModify)/10)+1
                    wordList.remove(toModify)

                    for No in range(PieceNum):
                        if (No != PieceNum-1):
                            toSend = toModify[No*10:(No+1)*10] + "-"
                            wordList.insert(IND + No, toSend)
                        else:
                            toSend = toModify[No*10:]
                            wordList.insert(IND + No, toSend)
            
            splitList.append(wordList[0])

            for word in wordList:
                if (word != wordList[0]):
                    if (len(splitList[-1] + " " + word)<=10):
                        splitList[-1] = splitList[-1] + " " + word
                    else:
                        splitList.append(word)

            for piece in splitList:
                showQuest = showQuest + piece + "\n"
            showQuest = showQuest[0:showQuest.rfind("\n")]

        else:
            showQuest = questions[QuestionNum][QuestionSide]
        Question.itemconfig(text, text = showQuest)

        checkMessage = 0

    return 0

#endsession
def endSession():
    global sessionStatus
    global questions

    if (sessionStatus == 1):
        sessionStatus = 0
        Question.itemconfig(text, text = '')
        Question.itemconfig(feedBack, text = '')
        Question.config(bg = '#f0f0f0')
        AskFront.config(state = 'normal')
        AskBack.config(state = 'normal')
        questions = []
        return 0
    else:
        tkinter.messagebox.showinfo("No Session", "There isn't any sesion currently going on")
        return -1


#submit button
def submit():
    side1 = Entry1.get()
    side2 = Entry2.get()
    deck = Entry3.get()
    newcard(side1, side2, deck)

#check button
def check(event = None):
    global checkMessage
    global Response
    global selectedDeckInd

    if (sessionStatus == 0):
        tkinter.messagebox.showinfo("No Session", "Please first start a session")
        return 1

    else:
        checkMessage = 1
        Response = AnswerBox.get()
        AnswerBox.select_range(0,'end')
        fStartSession()

        if (sessionStatus == 0):
            deckList.activate(selectedDeckInd[0])


### create entry box ####

#Answer Box
AnswerBox = tkinter.Entry(CheckFrame, font = ("Arial", 10))

#Front Side
Entry1 = tkinter.Entry(InputFrame)

#Back Side
Entry2 = tkinter.Entry(InputFrame)

#Deck
Entry3 = tkinter.Entry(InputFrame)

### create buttons ####

#checkbox
FrontInt = tkinter.IntVar()
BackInt = tkinter.IntVar()

AskFront = tkinter.Checkbutton(FrontBackFrame, text='Ask Front', variable = FrontInt, onvalue=1, offvalue=0)
AskBack = tkinter.Checkbutton(FrontBackFrame, text='Ask Back', variable = BackInt, onvalue=1, offvalue=0)


#Submit button
SubmitButton = tkinter.Button(InputFrame,
                   text = "Submit!",
                   command = submit
                   )

#check button
CheckButton = tkinter.Button(CheckFrame, text = "Check!", command = check)

#ShowFronts button
ShowFronts = tkinter.Button(ShowHideFrame, text = "Show Cards", command = showFronts)

#HideFronts button
HideFronts = tkinter.Button(ShowHideFrame, text = "Hide Cards", command = HideFronts)

#RemoveCard button
RemoveCard = tkinter.Button(ListLocation, text = "Remove Card", command = RemoveCard)

#StartSession button
StartSession = tkinter.Button(sessionFrame, text = "Start Session", command = fStartSession)

#endSession button
endSession = tkinter.Button(sessionFrame, text = "End Session", command = endSession)

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

## Create canvas
Question = tkinter.Canvas(window, bg = '#aee1e5', height = 200, width = 200)

### locate items ####

#locate the lists, scroolbars
yScroll.pack(side='right', fill='y')
deckList.pack(side = 'right')

FrontScroll.pack(side='right', fill='y')
FrontList.pack(side = 'right')

#locate the answer box and the check button
sessionFrame.pack(side = 'bottom')
endSession.pack(side = 'right')
StartSession.pack(side = 'left')
AnswerBox.pack(side = 'left', pady = 10)
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

#locate Front Back Frame
FrontBackFrame.pack(side = 'top')

#locate back/front checkbox
AskFront.pack(side = 'top')
AskBack.pack(side = 'top')

#Create question text
text = Question.create_text(100,50,fill="#e1924d",font="Times 20 bold", text='')
feedBack = Question.create_text(100,180,font="Times 15", text='')

Question.pack(side = 'bottom')

Question.itemconfig(text, text = '')
Question.itemconfig(feedBack, text = '')
Question.config(bg = '#f0f0f0')

#enter key
window.bind('<Return>', check)

window.mainloop()