class States:
    EMPTY = 0
    CABLE = 1
    TAIL = 2
    ELECTRO = 3
    SELECT = 4
    PASTE = 5

class Colors:
    BG = (15, 15, 15)
    GRID = (30, 30, 30)
    CABLE = (197, 106, 57)
    TAIL = (137, 55, 39)
    ELECTRO = (241, 196, 15)
    SELECT_BOX = (52, 152, 219, 100)

MINI_TRANS = {
    States.EMPTY: "Empty Cell",
    States.CABLE: "Cable",
    States.TAIL: "Tail",
    States.ELECTRO: "Electro",
    States.SELECT: "Select Area",
    States.PASTE: "Paste Blueprint"
}