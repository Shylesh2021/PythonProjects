from datetime import date
import os
import platform
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
import json

class GameResult:
    @staticmethod
    def loadResultsFromFile():
        filePath = filedialog.askopenfilename(filetypes=[("Game data", ".ticdata")])
        if not filePath:
            return []
        with open(file=filePath, mode="r") as file:
            jsonData = file.read()
            gameResults = json.loads(jsonData)
            if GameResult.validateLoadedData(gameResults):
                return gameResults
        return []

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

class GameScreen:
    def __init__(self, window: tk.Tk):
        self.window = window
        # self.showTestBoard()
        # return
        self.showScreen1(window)
    
    def showTestBoard(self):
        GameBoard(self.window, {
            "p1": "Prajwal",
            "p2": "Renu",
            "row": 4,
            "col": 4
        }).initialize()

    def showScreen1(self, window: tk.Tk):
        window.geometry("350x450")
        self.homeScreen = tk.Frame(window)
        self.screen1Grid = tk.Frame(self.homeScreen)
        self.screen1Grid.columnconfigure(0, weight=1)
        self.screen1Grid.columnconfigure(1, weight=3)

        tk.Label(self.screen1Grid, text="Enter name:").grid(row=0, column=0)
        tk.Label(self.screen1Grid, text="Player 1:").grid(row=1, column=0)
        
        self.p1Name = tk.Entry(self.screen1Grid, width=20)
        self.p1Name.grid(row=1, column=1)
        
        tk.Label(self.screen1Grid, text="Player 2:").grid(row=2, column=0)
        self.p2Name = tk.Entry(self.screen1Grid, width=20)
        self.p2Name.grid(row=2, column=1)

        tk.Label(self.screen1Grid, text="Board Dimensions", pady=13).grid(row=3, column=0)
        dimsGrid = tk.Frame(self.screen1Grid)
        dimsGrid.columnconfigure(0, weight=2)
        dimsGrid.columnconfigure(1, weight=1)
        dimsGrid.columnconfigure(1, weight=2)
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

    def createPreviousDataPanel(self, parent: tk.Frame):
        table = tk.Frame(parent)
        table.columnconfigure(0, weight=1)
        table.columnconfigure(1, weight=1)
        table.columnconfigure(2, weight=1)
        table.columnconfigure(3, weight=1)
        def onLoadButtonClick():
            tk.Label(table, text="Player 1", font=(font.Font(size=8, weight="bold"))).grid(row=2, column=0)
            tk.Label(table, text="Player 2", font=(font.Font(size=8, weight="bold"))).grid(row=2, column=1)
            tk.Label(table, text="Who Won", font=(font.Font(size=8, weight="bold"))).grid(row=2, column=2)
            tk.Label(table, text="Match Date", font=(font.Font(size=8, weight="bold"))).grid(row=2, column=3)
            resultList = GameResult.loadResultsFromFile()
            row = 3
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
        if self.validateData(data):
            self.homeScreen.pack_forget()
            gameBoard = GameBoard(self.window, data)
            gameBoard.initialize()
    
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
        if data["row"] > 5 or data["row"] < 3 or data["col"] > 5 or data["col"] < 3 or data["col"] != data["row"]:
            messagebox.showerror("Data error!", "Board dimensions should be greater than 2 and less than 6.")
            return False
        return True
    
    def isDigit(self, p):
        if str.isdigit(p) or p == "":
            return True
        else:
            return False

class GameBoard(tk.Frame):
    messageboxTitle = "TicTacToe Py"
    currentPlayerLabel: tk.Label
    playerWon = False
    gameTie = False
    coloredBtns = []

    def __init__(self, mainWindow: tk.Tk, data) -> None:
        tk.Frame.__init__(self, master=mainWindow)
        self.mainWindow = mainWindow
        self.p1 = { "name": data["p1"], "symbol": "X", "color": "blue" }
        self.p2 = { "name": data["p2"], "symbol": "O", "color": "green" }
        self.data = data
        self.os = platform.system()
    
    def initialize(self):
        self.boardData = { }
        self.currentPlayer = self.p1
        self.setDynamicWindowSize(self.data["col"])
        # self.mainWindow.geometry("720x650")
        self.mainWindow.title("TicTacToe Py")
        self.pack(fill="x")

        self.cells = { } # button -> (row, col)
        self.cellsGrid = tk.Frame(self.mainWindow)
        self.createScoreboard()
        self.createBoard()
        self.addMenuItems()
        self.cellsGrid.pack(anchor="center")
        
    def setDynamicWindowSize(self, rows):
        if rows == 5:
            self.mainWindow.geometry("720x680")
        elif rows == 4:
            self.mainWindow.geometry("600x580")
        else:
            self.mainWindow.geometry("500x470")

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
    
    def addOptionsButtons(self, parent: tk.Frame):
        tk.Button(parent, text="Reload Game", command=self.playAgainMenu).grid(row=3, column=0, padx=10)
        tk.Button(parent, text="Save Game", command=self.saveGame).grid(row=3, column=2)
    
    def saveGame(self):
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
        GameResult.saveData(finalObject)

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
        self.mainWindow.configure(menu=optionsMenu)
    
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
    
    def quitGameMenu(self):
        exit(0)
    
    def gotoHomeMenu(self):
        self.pack_forget()
        self.cellsGrid.pack_forget()
        GameScreen(self.mainWindow)
        self.mainWindow.configure(menu="")
        self.menuItems.pack_forget()
        self.optionsMenu.pack_forget()

    def onCellClick(self, button):
        if self.playerWon:
            self.showMessage(f"Player: {self.currentPlayer['name']} won the match")
            return
        totalCount = self.data["row"] * self.data["col"]
        if totalCount == len(self.boardData.keys()):
            self.handleTieLogic()
            return
        row, col = self.cells[button.widget]
        if not self.isValidClick(row, col):
            self.showMessage("Cell is already filled")
            return
        self.setCellValue(row, col, button.widget)
        if self.checkWinner(row, col):
            self.currentPlayerLabel.configure(text=f"{self.currentPlayer['symbol']} won the match.")
            self.showMessage(f"Player: {self.currentPlayer['name']} won the match.\nClick options to restart/quit.")
            self.playerWon = True
            return
        self.swapPlayer()
        if totalCount == len(self.boardData.keys()):
            self.handleTieLogic()
            return
    
    def handleTieLogic(self):
        self.showMessage("Board is full!\nClick options to restart/quit.")
        self.gameTie = True
    
    def checkWinner(self, row, col):
        maxRows = self.data["row"]
        count = 0
        coords = []
        for i in range(maxRows):
            key = str(row) + "," + str(i)
            coords.append((row, i))
            if key in self.boardData and self.boardData[key] == self.currentPlayer:
                count += 1
        if count == maxRows:
            self.highlightButtons(coords)
            return True
            
        count = 0
        coords = []
        for i in range(maxRows):
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
            j = maxRows - i - 1
            key = str(j) + "," + str(i)
            coords.append((j, i))
            if key in self.boardData and self.boardData[key] == self.currentPlayer:
                count += 1
        if count == maxRows:
            self.highlightButtons(coords)
            return True

        return False

    def highlightButtons(self, coords: list[(int, int)]):
        coloredBtns = []
        for i in coords:
            for btn in self.cells:
                row, col = self.cells[btn]
                if i == (row, col):
                    btn.configure(background="#95fcb4", activebackground="#66ff94")
                    coloredBtns.append(btn)
        self.coloredBtns = coloredBtns

    def setCellValue(self, row, col, button: tk.Button):
        key = str(row) + "," + str(col)
        self.boardData[key] = self.currentPlayer
        button.configure(
                text=self.currentPlayer["symbol"], 
                foreground=self.currentPlayer["color"],
                activeforeground=self.currentPlayer["color"],
            )
    
    def showMessage(self, msg):
        messagebox.showinfo(title=self.messageboxTitle, message=msg)
    
    def swapPlayer(self):
        if self.currentPlayer == self.p1:
            self.currentPlayer = self.p2
        else:
            self.currentPlayer = self.p1
        self.currentPlayerLabel.configure(text=self.currentPlayer["symbol"], foreground=self.currentPlayer["color"])

    def isValidClick(self, row: int, col: int):
        key = str(row) + "," + str(col)
        return key not in self.boardData

    def createBoard(self):
        w = 3
        h = 2
        if self.os == "windows":
            w = 1
            h = 1
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
                cell.bind("<ButtonPress-1>", self.onCellClick)
                cell.grid(row=row, column=col, sticky=tk.W + tk.E, padx=3, pady=3)
                self.cells[cell] = (row, col)

def mainFunc():
    window = tk.Tk()
    window.title("TEST")
    window.geometry("300x150")
    window.resizable(0, 0)
    GameScreen(window)
    window.mainloop()

if __name__ == "__main__":
    mainFunc()