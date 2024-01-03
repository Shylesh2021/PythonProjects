# Datetime function is used to store the game data
from datetime import date

# To check whether the game data file is there are not in a specific path
import os

# To check which OS the game is running
import platform

# Third Party library from python to build the UI
import tkinter as tk

# To pop-up the messages while playing the game
from tkinter import messagebox

# Used to save the file
from tkinter import filedialog

# To configure the font size, type and family
from tkinter import font

# Used to store the game data from python object to JSON String 
import json


#Helper for loading and saving the game
class GameResult:
    # this opens a file dialog and loads the game data from json and de-serialize it to Array of Dictionaries
    @staticmethod
    def loadResultsFromFile(): 
        filePath = filedialog.askopenfilename(filetypes=[])
        if not filePath:
            return []
        with open(file=filePath, mode="r") as file:
            jsonData = file.read()
            gameResults = json.loads(jsonData)
            if GameResult.validateLoadedData(gameResults):
                return gameResults
        return []

    # Validating all the necessary properties before loading the data to app.
    @staticmethod    
    def validateLoadedData(data):
        count = 0
        if type(data) is list:
            count +=1
        for d in data:
            if "Player1" in d and type(d["Player1"]) == str and "Player2" in d and type(d["Player2"]) == str and "WhoWon" in d and type(d["WhoWon"]) == str and "MatchDate" in d and type(d["MatchDate"]) == str:
                count += 1
        if count == (1 + len(data)):
            return True
        return False
    
    # File save dialog to save the game state information to a json file with custom file extension(.ticdata*)
    @staticmethod
    def saveData(data):
        filePath = filedialog.asksaveasfilename(filetypes=[("Game data", ".ticdata")])
        if not filePath:
            return
        if not os.path.isfile(filePath):
            with open(filePath, "xt") as f:
                f.write(json.dumps([data]))
                return
        with open(filePath, "r") as f:
            fdata = json.loads(f.read())
            fdata.append(data)
        with open(filePath, "w") as f:
            f.write(json.dumps(fdata))


# main class which implements the logic for the intial display of screen and UI elements
class GameScreen:
    # class constructor
    def __init__(self, window: tk.Tk):
        self.window = window
        # self.showTestBoard()
        # return
        self.showScreen1(window)
    
    # a temp function for testing/developing the game screen that loads the game screen instead of home screen
    def showTestBoard(self):
        GameBoard(self.window, {
            "p1": "Shylesh",
            "p2": "Moremi",
            "row": 4,
            "col": 4
        }).initialize()

    # The entire logic and UI elements for the Home/Initial screen
    def showScreen1(self, window: tk.Tk):
        window.geometry("500x500") # sets the initial window size
        window.title("Welcome to the Tic-Tac-Toe Game Powered By Python-Tkinter")
       
        # parent ui element that contains all the child UI
        self.homeScreen = tk.Frame(window)
        self.screen1Grid = tk.Frame(self.homeScreen) 
        self.screen1Grid.columnconfigure(0, weight=1)
        self.screen1Grid.columnconfigure(1, weight=3)
        alphabetValidator = self.homeScreen.register(self.isAlphabet)

        # text labes for information
        tk.Label(self.screen1Grid, text="Enter name:").grid(row=0, column=0)
        tk.Label(self.screen1Grid, text="Player 1:").grid(row=1, column=0)
        
        # Input box to enter player names
        self.p1Name = tk.Entry(self.screen1Grid, width=20, validatecommand=(alphabetValidator, "%P"), validate="all")
        self.p1Name.grid(row=1, column=1)
        
        tk.Label(self.screen1Grid, text="Player 2:").grid(row=2, column=0)
        self.p2Name = tk.Entry(self.screen1Grid, width=20, validatecommand=(alphabetValidator, "%P"), validate="all")
        # the grid() method calls denotes where to place the element in a grid
        self.p2Name.grid(row=2, column=1) 

        tk.Label(self.screen1Grid, text="Board Dimensions", pady=13).grid(row=3, column=0)
        dimsGrid = tk.Frame(self.screen1Grid)
        dimsGrid.columnconfigure(0, weight=2)
        dimsGrid.columnconfigure(1, weight=1)
        dimsGrid.columnconfigure(1, weight=2)
        # Tk's built-in function validator. It triggers everytime when a key is pressed on an entry UI element
        # and this will validate the input to accept only numbers
        validator = dimsGrid.register(self.isDigit)

        self.rowEntry = tk.Entry(dimsGrid, width=3, validatecommand=(validator, '%P'), validate='all')
        self.rowEntry.grid(row=0, column=0)
        tk.Label(dimsGrid, text="x").grid(row=0, column=1)
        self.colEntry = tk.Entry(dimsGrid, width=3, validatecommand=(validator, '%P'), validate='all')
        self.colEntry.grid(row=0, column=2)
        
        dimsGrid.grid(row=3, column=1)
        tk.Button(self.screen1Grid, text="Start Game", justify="right", command=self.startGame).grid(row=4, column=1)
        self.screen1Grid.pack(fill="none")
        self.createPreviousDataPanel(self.homeScreen)
        self.homeScreen.pack(fill="x")
        # the pack() is used to place an element in the parent ui

    #Previous matches data table
    def createPreviousDataPanel(self, parent: tk.Frame):
        # we need a parent to place the table
        table = tk.Frame(parent)
        # table is configured according to the need
        table.columnconfigure(0, weight=1)
        table.columnconfigure(1, weight=1)
        table.columnconfigure(2, weight=1)
        table.columnconfigure(3, weight=1)

        # Triggers when Load btn is clicked and static functions are called for loading data.
        def onLoadButtonClick():
            tk.Label(table, text="Player 1", font=(font.Font(size=8, weight="bold"))).grid(row=2, column=0)
            tk.Label(table, text="Player 2", font=(font.Font(size=8, weight="bold"))).grid(row=2, column=1)
            tk.Label(table, text="Who Won", font=(font.Font(size=8, weight="bold"))).grid(row=2, column=2)
            tk.Label(table, text="Match Date", font=(font.Font(size=8, weight="bold"))).grid(row=2, column=3)
            resultList = GameResult.loadResultsFromFile()
            row = 5
            for r in resultList:
                tk.Label(table, text=r["Player1"], font=font.Font(size=7)).grid(row=row, column=0)
                tk.Label(table, text=r["Player2"], font=font.Font(size=7)).grid(row=row, column=1)
                tk.Label(table, text=r["WhoWon"], font=font.Font(size=7)).grid(row=row, column=2)
                tk.Label(table, text=r["MatchDate"], font=font.Font(size=7)).grid(row=row, column=3)
                row += 1
        
        tk.Label(table, text="Previous Game data").grid(row=0, column=0)
        tk.Button(table, text="Load data", command=onLoadButtonClick).grid(row=1, column=0)
        
        table.pack(fill="x")
        self.table = table

    # This will run when Start btn is clicked
    def startGame(self):
        p1 = self.p1Name.get()
        p2 = self.p2Name.get()
        row = self.rowEntry.get()
        col = self.colEntry.get()
        data = {
            "p1": p1,
            "p2": p2,
            "row": int(row),
            "col": int(col)
        }
        #Validating the data input made by the player
        if self.validateData(data):
            # pack_forget() will unload/remove the ui elements from the parent 
            self.homeScreen.pack_forget()
            # here it will create a new ui elements to play the game.
            gameBoard = GameBoard(self.window, data)
            gameBoard.initialize()
    
    #Validating the input data by the  player
    def validateData(self, data):
        if len(data["p1"]) <= 2 or data["p1"] == "":
            messagebox.showerror("Data error!", "Player 1 name is too short.")
            return False
        if len(data["p2"]) <= 2 or data["p2"] == "":
            messagebox.showerror("Data error!", "Player 2 name is too short.")
            return False
        if data["p1"] == data["p2"]:
            messagebox.showerror("Data error!", "Player 1 and Player 2 name is equal.")
            return False
        if data["row"] > 5 or data["row"] < 3 or data["col"] > 5 or data["col"] < 3:
            messagebox.showerror("Data error!", "Board dimensions should be greater than 2 and less than 6.")
            return False
        
        if data["col"] != data["row"]:
            messagebox.showerror("Data error!", "Board dimensions entered in two cells should be identical.")
            return False
        return True
    
    # A function to check if the input value/string is a number or not
    def isDigit(self, p):
        if str.isdigit(p) or p == "":
            return True
        else:
            return False
        
    def isAlphabet(self, p):
        asciiVal = 65 # A-> 65
        if len(p) > 0:
            asciiVal = ord(p[len(p) - 1:len(p)])
        return not self.isDigit(p) and (asciiVal >= 65 and asciiVal <= 90) or (asciiVal >= 97 and asciiVal <= 122)


# Main class that inherits from the Tk's basic UI element i.e. Frame 
# and implements all the logic for running the game
class GameBoard(tk.Frame):
    #Message box title
    messageboxTitle = "TicTacToe Py"
    currentPlayerLabel: tk.Label # a reference to label to change dynamically which player is playing
    playerWon = False # flag to check if player won 
    gameTie = False 
    coloredBtns = [] # array filled with btn's to highlight which cells result the player win

    # constructor accepting the main window and data inputed by player
    def __init__(self, mainWindow: tk.Tk, data) -> None:
        tk.Frame.__init__(self, master=mainWindow)
        self.mainWindow = mainWindow
        # hard-coding the P1 & P2 values
        self.p1 = { "name": data["p1"], "symbol": "X", "color": "blue" } 
        self.p2 = { "name": data["p2"], "symbol": "O", "color": "green" }
        self.data = data
        # to get which platform user is in
        self.os = platform.system()
    
    # A function which is called after GameBoard class is created and to initialize the Game
    def initialize(self):
        # contains which user clicked which button
        self.boardData = { }
        self.currentPlayer = self.p1
        # sets dynamic window size based on row/column size
        self.setDynamicWindowSize(self.data["col"])
        # self.mainWindow.geometry("720x650")
        self.mainWindow.title("TicTacToe Py")
        self.pack(fill="x")

        # contains buttons and row,column 
        self.cells = { } # button -> (row, col)
        self.cellsGrid = tk.Frame(self.mainWindow)
        # 1st we create a score-board at the top of the screen
        self.createScoreboard()
        # then we create the actual game board
        self.createBoard()
        # then we add menu items at the top of the window for a list of Options 
        self.addMenuItems()
        self.cellsGrid.pack(anchor="center")
        
    #Setting the window size based on the row/column to fit everything in the screen
    def setDynamicWindowSize(self, rows):
        if rows == 5:
            self.mainWindow.geometry("720x680")
        elif rows == 4:
            self.mainWindow.geometry("600x580")
        else:
            self.mainWindow.geometry("500x470")

    # logic to create scoreboard ui which uses grid structure to place ui elements
    def createScoreboard(self):
        board = tk.Frame(self, width=10)
        board.columnconfigure(0, weight=1)
        board.columnconfigure(1, weight=1)
        board.columnconfigure(2, weight=4)
        board.columnconfigure(3, weight=4)
        self.addOptionsButtons(board)
        tk.Label(board, text="P1: " + self.p1["name"], padx=10).grid(row=0, column=0)
        tk.Label(board, text="P2: " + self.p2["name"], padx=10).grid(row=1, column=0)

        tk.Label(board, 
                text=self.p1["symbol"], 
                foreground=self.p1["color"], 
                font=font.Font(weight="bold", size=10)
            ).grid(row=0, column=1)
        tk.Label(board, 
                text=self.p2["symbol"], 
                foreground=self.p2["color"], 
                font=font.Font(weight="bold", size=10)
            ).grid(row=1, column=1)
        
        tk.Label(board, text="Current Player: ", padx=10).grid(row=2, column=0)
        scoreLabel = tk.Label(board, 
                text=self.p1["symbol"], 
                foreground=self.p1["color"], 
                font=font.Font(weight="bold", size=10)
            )
        scoreLabel.grid(row=2, column=1)
        self.currentPlayerLabel = scoreLabel
        
        board.pack(anchor="w", padx=10)
    
    # here this adds some option btns under the scoreboard for Reloading and saving game
    def addOptionsButtons(self, parent: tk.Frame):
        # the command param is a lambda or function we need to pass, this will trigger when btn is clicked
        tk.Button(parent, text="Reload Game", command=self.playAgainMenu).grid(row=3, column=0, padx=10)
        tk.Button(parent, text="Save Game", command=self.saveGame).grid(row=3, column=2)
    
    # logic to save the current state of the game after win/draw
    def saveGame(self):
        # Logic to show the status of the game, i.e. WOn/Tie/In Progress
        if not self.playerWon and not self.gameTie:
            self.showMessage("Game is still in progress")
            return
        p1 = self.p1["name"]
        p2 = self.p2["name"]
        status = "Tie"
        if self.playerWon:
            if self.currentPlayer["symbol"] == "X":
                status = "P1"
            else:
                status = "P2"
        dateWon = str(date.today())
        finalObject = {
            "Player1": p1,
            "Player2": p2,
            "WhoWon": status,
            "MatchDate": dateWon
        }
        # the actual save logic is here
        GameResult.saveData(finalObject)

    #Used for reating 3 menu items at the top-left of the window
    def addMenuItems(self):
        optionsMenu = tk.Menu(self)
        menuItems = tk.Menu(optionsMenu)
        optionsMenu.add_cascade(label="Options", menu=menuItems)
        menuItems.add_command(label="Play Again", command=self.playAgainMenu)
        menuItems.add_command(label="Goto Home", command=self.gotoHomeMenu)
        menuItems.add_separator()
        menuItems.add_command(label="Quit Game", command=self.quitGameMenu)
        self.optionsMenu = optionsMenu
        self.menuItems = menuItems
        # the configure() will change the settings of any UI element.
        # but in here we are setting options to the main window
        self.mainWindow.configure(menu=optionsMenu)
    
    # triggered when Play again menu-item btn is clicked
    def playAgainMenu(self):
        # reset board logic
        self.playerWon = False
        self.gameTie = False
        self.currentPlayer = self.p1
        for k in self.cells:
            k.configure(text="")
        self.boardData = { }
        self.currentPlayerLabel.configure(text=self.p1["symbol"], foreground=self.p1["color"])
        for btn in self.coloredBtns:
            btn.configure(activebackground="white", background="white")
    
    # triggered when Quit menu-item btn is clicked, and quits the application
    def quitGameMenu(self):
        exit(0)
    
    # Loads all the UI elements, and opens the home screen
    def gotoHomeMenu(self):
        self.pack_forget()
        self.cellsGrid.pack_forget()
        GameScreen(self.mainWindow)
        self.mainWindow.configure(menu="")
        self.menuItems.pack_forget()
        self.optionsMenu.pack_forget()

    # triggered when a cell/grid-btn is clicked
    # main game logic goes here
    def onCellClick(self, button):
        # checks if game won the match, if so then stop the player from clicking the btn's
        if self.playerWon:
            self.showMessage(f"Player: {self.currentPlayer['name']} Won the match")
            return
        #Checking the total row*col count to check if all btn's are clicked and not won to check if game is Tie/Draw.
        totalCount = self.data["row"] * self.data["col"]
        if totalCount == len(self.boardData.keys()):
            # function to handle Tie game logic
            self.handleTieLogic() 
            return
        # To get the row and column by passing the button as the key to the dictionary
        row, col = self.cells[button.widget]
        # checking if the cell is valid and empty to click
        if not self.isValidClick(row, col):
            self.showMessage("Cell is already filled")
            return
        # setting the cell value and blocks the btn to not able to click in future
        self.setCellValue(row, col, button.widget)
        #Main function to check if the current player won the match
        if self.checkWinner(row, col):
            self.currentPlayerLabel.configure(text=f"{self.currentPlayer['name']} won the match.")
            self.showMessage(f"Player: {self.currentPlayer['name']} won the match.\nClick options to restart/quit.")
            self.playerWon = True
            return
        # here we swap the current player to the opponent player
        self.swapPlayer()
        if totalCount == len(self.boardData.keys()):
            self.handleTieLogic()
            return
    
    # shows message popup 
    def handleTieLogic(self):
        self.showMessage("Match Tie!\nClick options to restart/quit.")
        self.gameTie = True
    
    # logic to check is there a win
    def checkWinner(self, row, col):
        maxRows = self.data["row"]
        count = 0 # if this count is equals to the row, then there is a win
        coords = [] # this is to get the buttons for highlighting if win

        # looping over columns
        for i in range(maxRows): 
            key = str(row) + "," + str(i)
            coords.append((row, i))
            # here if the board data is filled 
            # checks if the current player is clicked in this column
            if key in self.boardData and self.boardData[key] == self.currentPlayer:
                count += 1
        if count == maxRows:
            # highlights btn's which are in a win-pattern
            self.highlightButtons(coords)
            return True
            
        # Resets the count and coords array to restart the loop
        count = 0
        coords = []
        for i in range(maxRows):
            # loops in row wise
            key = str(i) + "," + str(col)
            coords.append((i, col))
            if key in self.boardData and self.boardData[key] == self.currentPlayer:
                count += 1
        if count == maxRows:
            self.highlightButtons(coords)
            return True
            
        count = 0
        coords = []
        for i in range(maxRows):
            # from top-left to bottom-right like -> \
            key = str(i) + "," + str(i)
            coords.append((i, i))
            if key in self.boardData and self.boardData[key] == self.currentPlayer:
                count += 1
        if count == maxRows:
            self.highlightButtons(coords)
            return True

        count = 0
        coords = []
        for i in range(maxRows):
            # from bottom-left to top-right like -> /
            j = maxRows - i - 1
            key = str(j) + "," + str(i)
            coords.append((j, i))
            if key in self.boardData and self.boardData[key] == self.currentPlayer:
                count += 1
        if count == maxRows:
            self.highlightButtons(coords)
            return True

        return False

    # Simple logic that loops over cords and highlights the btns which are stored in Dictionary
    def highlightButtons(self, coords: list[(int, int)]):
        coloredBtns = []
        for i in coords:
            for btn in self.cells:
                row, col = self.cells[btn]
                if i == (row, col):
                    btn.configure(background="#95fcb4", activebackground="#66ff94")
                    coloredBtns.append(btn)
        self.coloredBtns = coloredBtns

    # Setting the value in the Board Data
    # stores in Dictionary Key=row,col and value is currentPlayer (P1 or P2)
    def setCellValue(self, row, col, button: tk.Button):
        key = str(row) + "," + str(col)
        self.boardData[key] = self.currentPlayer
        button.configure(
                text=self.currentPlayer["symbol"], 
                foreground=self.currentPlayer["color"],
                activeforeground=self.currentPlayer["color"],
            )
    
    #Wrapper showing a popup msg
    def showMessage(self, msg):
        messagebox.showinfo(title=self.messageboxTitle, message=msg)
    
    # swap logic i.e. if current Player is P1, this sets to P2 and vice-versa
    def swapPlayer(self):
        if self.currentPlayer == self.p1:
            self.currentPlayer = self.p2
        else:
            self.currentPlayer = self.p1
        self.currentPlayerLabel.configure(text=self.currentPlayer["symbol"], foreground=self.currentPlayer["color"])

    # checks if the cell is a valid click i.e. if it is empty
    def isValidClick(self, row: int, col: int):
        key = str(row) + "," + str(col)
        return key not in self.boardData

    # logic to create board i.e. grid of cells/buttons
    def createBoard(self):
        w = 3 # btn width
        h = 2 # btn height
        if self.os == "Windows": # in windows, the btn dimensions gets screwed.
            w = 3
            h = 1

        # loop row * col times, so Time Complexity = O(row * col)
        for row in range(self.data["row"]):
            for col in range(self.data["col"]):
                cell = tk.Button(
                        self.cellsGrid, 
                        font=font.Font(size=30, weight="bold"),
                        text="",
                        width=w,
                        height=h,
                        highlightbackground="lightblue",
                        activebackground="white",
                        background="white",
                        foreground="green",
                        activeforeground="green"
                    )
                # bind() is called when btn is pressed
                cell.bind("<ButtonPress-1>", self.onCellClick)
                cell.grid(row=row, column=col, sticky=tk.W + tk.E, padx=3, pady=3)
                self.cells[cell] = (row, col)

# a simple clean-up, instead of writing this mess under if condition
def mainFunc():
    window = tk.Tk()
    window.title("TEST")
    window.geometry("300x150")
    window.resizable(0, 0)
    GameScreen(window)
    window.mainloop()

if __name__ == "__main__":
    mainFunc()