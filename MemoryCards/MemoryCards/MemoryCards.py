import random
import os
import tkinter

main_dir = os.getcwd()[0:os.getcwd().rfind("MemoryCards")]
data_dir = main_dir + "data.crd"

#define the cards
class cards:
    def __init__(self, frontSide, backSide, Deck):
        self.frontSide = frontSide
        self.backSide = backSide
        self.Deck = Deck


#check the existing decks
decks = []

#create a window instance
window = tkinter.Tk()
window.geometry("500x500")
window.title("Memory")


### define what buttuons do ####

#create data file
checkFile = open(data_dir, 'a', encoding = 'UTF-8', newline='')
checkFile.close()

# "$" is used to divide data by cards
# "%" is used to divide cards by properties

def newcard(side1, side2, deck):
        WriteFile = open(data_dir, 'a', encoding = 'UTF-8', newline='')
        WriteFile.write(side1 + "%" + side2 + "%" + deck + "$")
        WriteFile.close


#submit button
def submit():
    side1 = Entry1.get()
    side2 = Entry2.get()
    deck = Entry3.get()

    #read the content in the file
    readFile = open(data_dir, 'r', encoding = 'UTF-8', newline='')
    content = readFile.read()
    readFile.close

    #check if the file exists
    Location = content.find("$")
    if(Location < 0):
        newcard(side1,side2,deck)
    else:
        print("there are data")
        cards = content.split("$")
        print(cards)
        for i in cards:
            sides = i.split("%")
            print(sides[0])
            if (sides[0] == side1):
                tkinter.messagebox.showinfo(title=("Caution"), message=("There is already an entry with the same frontside"))
                break

        ####Say when to create a new card
        #newcard(side1,side2,deck)


#check button
def check():
    print(AnswerBox.get() + " checked")


### creater entry box ####

#Answer Box
AnswerBox = tkinter.Entry(window, font = ("Arial", 10))

#Front Side
Entry1 = tkinter.Entry(window)

#Back Side
Entry2 = tkinter.Entry(window)

#Deck
Entry3 = tkinter.Entry(window)

### create buttons ####

#Submit button
SubmitButton = tkinter.Button(window,
                   text = "Submit!",
                   command = submit
                   )

#check button
CheckButton = tkinter.Button(window,
                   text = "Check!",
                   command = check
                   )


### locate items ####

#locate the answer box and the check button
AnswerBox.place(x=150, y=400)
CheckButton.place(x=300, y=400-4)

#Locate front and back labels
tkinter.Label(window,text = "Front").grid(row=1,column=0)
tkinter.Label(window,text = "Back").grid(row=2,column=0)
tkinter.Label(window,text = "Deck").grid(row=3,column=0)

#locate entry box
Entry1.grid(row=1,column=1)
Entry2.grid(row=2,column=1)
Entry3.grid(row=3,column=1)

#locate submit button
SubmitButton.grid(row=4, column=1)

window.mainloop()