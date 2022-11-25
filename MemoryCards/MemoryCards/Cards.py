import sqlite3
from types import NoneType

#sqlConnection
class sqlConnection():

    #init
    def __init__ (self, table):

        self.table = table

        sqlite3.register_converter("sqlCat", self.catConverter)
        sqlite3.register_converter("sqlDeck", self.deckConverter)
        sqlite3.register_converter("sqlCard", self.cardConverter)

        self.connection = sqlite3.connect(self.table.path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.curs = self.connection.cursor()

        #create tables:
        try:
            self.curs.execute("CREATE TABLE cats(categoryCol sqlCat)")
        except:
            pass

        try:
            self.curs.execute("CREATE TABLE decks(deckCol sqlDeck)")
        except:
            pass

        try:
            self.curs.execute("CREATE TABLE cards(cardCol sqlCard)")
        except:
            pass

    #categoryConverter
    def catConverter(self, s):
        nameCat = s.decode("utf-8")

        return Category(nameCat, self.table)

    #deckCoverter
    def deckConverter(self, s):

        #category, name, front, back

        valList = s.decode("utf-8").split("::--::")

        catList = self.table.cats

        for category in catList:
            if valList[0] == catList[category].nameCat:
                deckCat = catList[category]
                break

        if valList[2] == "True":
            deckFront = True
        else:
            deckFront = False

        if valList[3] == "True":
            deckBack = True
        else:
            deckBack = False

        return Deck(deckCat, valList[1], deckFront, deckBack)

    #cardConverter
    def cardConverter(self, s):

        #deck, front, back
        deckList = self.curs.execute("SELECT deckCol FROM decks").fetchall()
        valList = s.decode("utf-8").split("::--::")

        #we will check all the decks and accept the only one who has the same category with the commited card.
        for deck in deckList:
            if (valList[1] == deck.nameDeck and valList[0] == deck.category):
                cardDeck = deck
                break

        return Card(cardDeck, valList[2], valList[3])

    #saveTable
    def saveTable (self):

        self.curs.execute("DELETE FROM cats")
        self.curs.execute("DELETE FROM decks")
        self.curs.execute("DELETE FROM cards")

        for cat in self.table.cats:
            self.curs.execute("INSERT INTO cats(categoryCol) VALUES(?)", (self.table.cats[cat],))
            for deck in self.table.cats[cat].decks:
                self.curs.execute("INSERT INTO decks(deckCol) VALUES(?)", (self.table.cats[cat].decks[deck],))
                for card in self.table.cats[cat].decks[deck].cards:
                    self.curs.execute("INSERT INTO cards(cardCol) VALUES(?)", (self.table.cats[cat].decks[deck].cards[card],))

        self.connection.commit()

    #release
    def release(self):
        del self.curs
        self.connection.close()
        del self

#table
class Table(object):

    #init
    def __init__(self, name, path):
        self.nameTab = name
        self.path = path

        self.catNum = 0
        self.cats = dict()

        self.sql3 = NoneType

    def updateDict(self, cat, nameCat):

        catKeys = list(self.cats.keys())
        catVals = list(self.cats.values())

        newCats = dict()

        for i in range(len(catKeys)):

            if cat == catVals[i]:
                newCats.update({nameCat:cat})
            else:
                newCats.update({catKeys[i]:catVals[i]})

        self.cats = newCats

    #cleanTable
    def CleanTable(self, name, path):

        self.nameTab = name
        self.path = path

        ####celan all the cards
        for key in self.cats:
            for ind, deck in self.cats[key].decks:
                for i in range(len(self.cats[key].decks[ind].cards)):
                    self.cats[key].decks[ind].cards.popitem()

        ####celan all the decks
        for key in self.cats:
            for i in range(len(self.cats[key].decks)):
                self.cats[key].decks.popitem()

        ####clean all the categories
        for i in range(len(self.cats)):
            self.cats.popitem()

        self.catNum = 0

    #str
    def __str__(self):
        return self.nameTab

    #addCat
    def addCat(self, cat):
        self.cats.update({cat.nameCat:cat})
        self.catNum += 1

    #deleteCat
    def deleteCat(self, cat):
        self.cats.pop(cat.nameCat)
        self.catNum -= 1

    #connect
    def connect(self):
        if (self.sql3 == NoneType):
            self.sql3 = sqlConnection(self)
            #Check error handle needed
            pass

    #diconnect
    def disconnect(self):
        if (self.sql3 != NoneType):
            self.sql3.release()
            self.sql3 = NoneType
            #Check error handle needed
            pass

#category
class Category(Table):

    #init
    def __init__(self, name, table):

        self.table = table
        self.nameCat = name

        self.sqlVal = name

        self.deckNum = 0
        self.decks = dict()
        table.addCat(self)

    def updateDict(self, deck, newName):
        deckKeys = list(self.decks.keys())
        deckVals = list(self.decks.values())

        newDecks = dict()

        for i in range(len(deckKeys)):

            if deck == deckVals[i]:
                newDecks.update({newName:deck})
            else:
                newDecks.update({deckKeys[i]:deckVals[i]})

        self.cats = newDecks

    #str
    def __str__(self):
        return self.nameCat

    #conform
    def __conform__(self, protocol):
        if protocol == sqlite3.PrepareProtocol:
            return self.sqlVal

    #Update
    def UpdateCat (self, newName):
        self.table.updateDict(self, newName)
        self.nameCat = newName

    #addDeck
    def addDeck(self, deck):
        self.decks.update({deck.nameDeck:deck})
        self.deckNum += 1

    #deleteDeck
    def deleteDeck(self, deck):
        self.decks.pop(deck.nameDeck)
        self.deckNum -= 1

    #release
    def release(self):
        self.table.deleteCat(self)
        del self

#deck
class Deck(Category):

    #init
    def __init__(self, category, name, front, back):
        self.category = category
        self.nameDeck = name
        self.askFront = front
        self.askBack = back

        self.sqlVal = category.nameCat + "::--::" + name + "::--::" + str(front) + "::--::" + str(back)

        self.cardNum = 0
        self.cards = dict()
        category.addDeck(self)

    #conform
    def __conform__(self, protocol):
        if protocol == sqlite3.PrepareProtocol:
            return self.sqlVal

    #str
    def __str__(self):
        return self.nameDeck

    def updateDeck(self, newCategory, newName, newFront, newBack):

        if self.category != newCategory:
            pass

        if newName != self.nameDeck:
            self.category.updateDict(self, newName)
            self.nameCat = newName

        self.askFront = newFront
        self.askBack = newBack




    #addCard
    def addCard(self, card):
        self.cards.update({card.nameCard:card})
        self.cardNum += 1

    #deleteCard
    def deleteCard(self, card):
        self.cards.pop(card.nameCard)
        self.cardNum -= 1

    #release
    def release(self):
        self.category.deleteDeck(self)
        del self

#Card
class Card(Deck):

    #init
    def __init__(self, deck, front, back):
        self.nameCard = front
        self.front = front
        self.back = back

        self.deck = deck
        self.category = deck.category

        #we send the category information here. When we receive it, we will check if the deck belongs to this category or not.
        self.sqlVal = deck.category + "::--::" + deck + "::--::" + front + "::--::" + back

        deck.addCard(self)

    #conform
    def __conform__(self, protocol):
        if protocol == sqlite3.PrepareProtocol:
            return self.sqlVal

    #str
    def __str__(self):
        return self.Front

    #release
    def release(self):
        self.deck.deleteCard(self)
        del self
