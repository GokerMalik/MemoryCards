import sqlite3
import Cards
import string
import os

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __conform__(self, protocol):
        if protocol == sqlite3.PrepareProtocol:
            return f"{self.x};{self.y}".encode("utf-8")



def convert_deck(s):

    vals = s.decode("utf-8").split("::--::")

    if vals[2] == "True":
        bool1 = True
    else:
        bool1 = False

    if vals[3] == "True":
        bool2 = True
    else:
        bool2 = False

    return Cards.Deck(cat, vals[1], bool1, bool2)

# Register the adapter and converter
sqlite3.register_converter("bar", convert_deck)

homeDir = os.path.expanduser('~')
dirTemp = homeDir + fr'\OneDrive\Desktop\tempB.mem'

# 1) Parse using declared types
tab = Cards.Table("abc", dirTemp)
cat = Cards.Category("cat1", tab)

dec1 = Cards.Deck(cat, "deck1", True, True)
dec2 = Cards.Deck(cat, "deck2", True, True)
dec3 = Cards.Deck(cat, "deck3", True, True)
dec4 = Cards.Deck(cat, "deck4", True, True)

con = sqlite3.connect(dirTemp, detect_types=sqlite3.PARSE_DECLTYPES)

cur = con.cursor()

try:
    cur.execute("CREATE TABLE deck(abcd bar)")
except:
    pass


cur.execute("INSERT INTO deck(abcd) VALUES(?)", (dec1,))
cur.execute("INSERT INTO deck(abcd) VALUES(?)", (dec2,))
cur.execute("INSERT INTO deck(abcd) VALUES(?)", (dec3,))
cur.execute("INSERT INTO deck(abcd) VALUES(?)", (dec4,))

list = cur.execute("SELECT abcd FROM deck").fetchall()
print(list[1][0].nameDeck)
cur.close()
con.close()