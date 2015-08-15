from Tkinter import *
import tkMessageBox
import random

#Global constants
numCols = 10
numRows = 15
midCol = numCols/2
cellDim = 30
colorNames = ["red", "magenta", "yellow", "cyan", "blue", "light grey", "lime"]
lineColor = "black"
edgeColor = "black"
emptyColor = "black"

shapeNames = ["I", "J", "L", "O","S","T","Z"]
shapeConfigs = [[[True, True, True, True],[False, False, False, False]], 
				[[True, False, False], [True, True, True]],
				[[False, False, True], [True, True, True]],
				[[True, True], [True, True]],
				[[False, True, True], [True, True, False]],
				[[False, True, False], [True, True, True]],
				[[True, True, False], [False, True, True]],
]

timeDelay = 1000

"""
#For testing only
shapeNames = ["I", "O"]
shapeConfigs = [[[True, True, True, True],[False, False, False, False]],
				[[True, True], [True, True]],
				]
"""

#Board class
class Board:
	#Initialize a new empty board
	def __init__ (self):
		#Create an array to represent the board
		self.grid = [[emptyColor for col in range(numCols)]
						for row in range(numRows)]
		#Create an array to store the shape IDs for the canvas
		self.ids = [[emptyColor for col in range(numCols)]
						for row in range(numRows)]
	#Clear the board of all game pieces
	def clear (self):
		self.grid = [[emptyColor for col in range(numCols)]
						for row in range(numRows)]
						
	#Update the board colors
	def updateBoard(self, piece):
		for iRow in range(len(piece.position)):
			for iCol in range(len(piece.position[iRow])):
				if piece.shape[iRow][iCol]:
					posX = piece.position[iRow][iCol][0]
					posY = piece.position[iRow][iCol][1]
					self.grid[posX][posY] = piece.color
	
	
	#Checks if the row is full
	def checkRow(self, theRow):
		fullRow = True
		for iCol in range(numCols):
			if self.grid[theRow][iCol] == emptyColor:
				fullRow = False
				break
		return fullRow
		
	#Remove row
	def removeFullRows (self):
		counter = 0
		tempBoard = [[self.grid[row][col] for col in range(numCols)]
						for row in range(numRows)]
		for iRow in range(numRows):
			#If the row is full
			if self.checkRow(iRow):
				#Increment the counter
				counter+=1
				#For each row up to and including the full row, move everything down by 1 row
				for jRow in range(iRow+1):
					if not(jRow == 0):
						for iCol in range(numCols):
							tempBoard[jRow][iCol] = self.grid[jRow-1][iCol]
				
				#Update the board
				for jRow in range(numRows):
					for iCol in range(numCols):
						self.grid[jRow][iCol] = tempBoard[jRow][iCol]
		return counter
		
	#Check if board is full
	def checkFull (self):
		isFull = False
		for iCol in range(numCols):
			if self.grid[0][iCol] != emptyColor:
				isFull = True
		return isFull
	
		
		
#test = Board ()
#print test.grid

#Game piece class
class GamePiece:
	#Initialize a new game piece
	def __init__ (self):
		#Set the shape
		shape = self.selectShape()
		self.shape = shapeConfigs[shape]
		self.shapeName = shapeNames[shape]
		#Set the color
		self.color = colorNames[self.selectColor()]
		#Set the initial position to be the top middle of the board
		self.position = [[0 for col in range(len(self.shape[0]))]
						for row in range(len(self.shape))]
		for iRow in range (len(self.shape)):
			for iCol in range(len(self.shape[iRow])):
				self.position[iRow][iCol] = [iRow,iCol+midCol - len(self.shape[iRow])/2]
		#Create an array to hold the ids for each block
		self.ids = [[0 for col in range(len(self.shape[0]))]
						for row in range(len(self.shape))]
		
		#Set the anchor block (used for rotate function)
		self.anchor = [1,1]
		
	#Randomly select and return a shape
	def selectShape(self):
		theShape = random.randrange(len(shapeConfigs))
		return theShape
		#return shapeConfigs[3]
	
	#Randomly select and return a color
	def selectColor(self):
		theColor = random.randrange(len(colorNames))
		return theColor
	
	
		
#test = GamePiece()
#for i in range(25):
#	test.movePiece("left")
#	print "Loop ", i, " ", test.position

#Main class for game loop
class GameController:
	def __init__ (self, parent):
		#Initialize root window, canvas, and board
		self.parent = parent
		self.canvas = Canvas(self.parent)
		self.board = Board()
		self.drawBoard()
		
		#Select a new shape and draw it on the board
		self.currentShape = GamePiece()
		self.drawShape()
		self.parent.update()
		self.canvas.after(timeDelay)
		
		#Set the score to zero
		self.score = 0
		
		#Event callbacks
		self.parent.bind('<Key>', self.keyPressed)
		
		#Move the shape
		self.moveShapeDown()
	
	#Loop for moving piece down
	def moveShapeDown (self):
		self.handleMove("down")
		self.parent.after(timeDelay,self.moveShapeDown)
	
	#Handle the move based on state of the board
	def handleMove(self, direction):
		#If piece can't be moved
		if not self.movePiece(direction):
			#Check if it has hit the bottom
			if self.checkBottom ():
				#Update the board
				self.board.updateBoard(self.currentShape)
				self.repaintBoard()
				self.deleteShape()
				#Check for and remove full rows, and increment the total score
				incr = self.board.removeFullRows()
				self.score+=incr
				self.repaintBoard()
				
				#Check if board is full
				if self.board.checkFull ():
					tkMessageBox.showwarning(
						title="GAME OVER",
						message ="Score: %7d\t" % (
                            self.score),
						parent=self.parent
						)
					#Toplevel().destroy()
					self.parent.destroy()
					sys.exit(0)
				
				#Otherwise, create the next shape
				else:
					self.currentShape = GamePiece()
					self.drawShape()
					self.parent.update()
				
	#Move the game piece
	def movePiece(self,direction):
		
		#If direction is left
		if direction == "left":
			#Change the x coordinate (y coordinate in terms of the grid)
			changeIdx = 1
			#Set the increment amount
			incrAmt = -1
		
		#If direction is right
		elif direction == "right":
			#Change the x coordinate (y coordinate in terms of the grid)
			changeIdx = 1
			#Set the increment amount
			incrAmt = 1
			
		#If direction is down
		else:
			#Change the y coordinate (x coordinate in terms of the grid)
			changeIdx = 0
			#Set the increment amount
			incrAmt = 1
			
		#Shift the position of each block
		movePiece = True
		for iRow in range (len(self.currentShape.position)):
			for iCol in range(len(self.currentShape.position[iRow])):
				if self.currentShape.shape[iRow][iCol]:	
					newPosition = self.currentShape.position[iRow][iCol][changeIdx] + incrAmt
					#If a new position is not legal, then set movePiece to false
					if not(self.checkLegalMove (newPosition,changeIdx, iRow, iCol)):
						movePiece = False
						break
		if movePiece:
			for iRow in range (len(self.currentShape.position)):
				for iCol in range(len(self.currentShape.position[iRow])):
					self.currentShape.position[iRow][iCol][changeIdx] += incrAmt
		
			#Redraw the block in its new position
			self.deleteShape()
			self.drawShape()
			self.parent.update()
		
		return movePiece
		
	#Main function for rotate
	def rotatePiece(self):
		
		#If shape is L, J, or T, do a full rotate counterclockwise
		if self.currentShape.shapeName == "L" or self.currentShape.shapeName == "J" or self.currentShape.shapeName == "T":
			self.fullRotate("minus")
		#If shape is I, S, or Z, do a limited rotate
		elif self.currentShape.shapeName == "I" or self.currentShape.shapeName == "S" or self.currentShape.shapeName == "Z":
			if len(self.currentShape.shape) == 2:
				self.fullRotate("minus")
			else:
				self.fullRotate("plus")
		
		#Redraw the block in its new position
		self.deleteShape()
		self.drawShape()
		self.parent.update()	
		
		
	#Rotate function
	def fullRotate(self, direction):
		
		rotatePiece = True
		
		#Get the relative and absolute positions of the anchor block in the current shape
		old_rel_anchorRow = self.currentShape.anchor[0]
		old_rel_anchorCol = self.currentShape.anchor[1]
		abs_anchorRow = self.currentShape.position[old_rel_anchorRow][old_rel_anchorCol][0]
		abs_anchorCol = self.currentShape.position[old_rel_anchorRow][old_rel_anchorCol][1]
		
		#Get the dimensions of the current shape
		oldNumRows = len(self.currentShape.shape)
		oldNumCols = len(self.currentShape.shape[0])
		
		#Memorize the current configuration
		oldShape = [[False for col in range(oldNumCols)]
						for row in range(oldNumRows)]
		oldIds = [[0 for col in range(oldNumCols)]
						for row in range(oldNumRows)]
		for iRow in range(oldNumRows):
			for iCol in range(oldNumCols):
				oldShape[iRow][iCol] = self.currentShape.shape[iRow][iCol]
				oldIds[iRow][iCol] = self.currentShape.ids[iRow][iCol]
				
		#Get the new configuration
		tempConfig = [[False for col in range(oldNumRows)]
						for row in range(oldNumCols)]
		tempId = [[0 for col in range(oldNumRows)]
						for row in range(oldNumCols)]
		for iRow in range(oldNumRows):
			for iCol in range (oldNumCols):
				#If clockwise
				if direction == "plus":
					tempConfig[iCol][oldNumRows-1-iRow] = self.currentShape.shape[iRow][iCol]
					tempId[iCol][oldNumRows-1-iRow] = self.currentShape.ids[iRow][iCol]
				#If counter-clockwise
				else:
					tempConfig[oldNumCols-1-iCol][iRow] = self.currentShape.shape[iRow][iCol]
					tempId[oldNumCols-1-iCol][iRow] = self.currentShape.ids[iRow][iCol]
					
		self.currentShape.shape = tempConfig
		self.currentShape.ids = tempId
		
		#Update the anchor
		if direction == "plus":
			self.currentShape.anchor[0] = old_rel_anchorCol
			self.currentShape.anchor[1] = oldNumRows-1-old_rel_anchorRow
		else:
			self.currentShape.anchor[0] = oldNumCols - 1 - old_rel_anchorCol
			self.currentShape.anchor[1] = old_rel_anchorRow
			
		#Get the new relative position of the anchor block
		rel_anchorRow = self.currentShape.anchor[0]
		rel_anchorCol = self.currentShape.anchor[1]		
		#Get the new positions
		tempPosition = [[[0,0] for col in range(oldNumRows)]
						for row in range(oldNumCols)]
		for iRow in range(oldNumCols):
			if not rotatePiece:
				break
			row_offset = iRow - rel_anchorRow
			for iCol in range (oldNumRows):
				col_offset = iCol - rel_anchorCol
				tempPosition[iRow][iCol] = [abs_anchorRow+row_offset,abs_anchorCol+col_offset]
				if self.currentShape.shape[iRow][iCol]:	
					if not self.checkLegalRotate(tempPosition[iRow][iCol][0], tempPosition[iRow][iCol][1]):
						rotatePiece = False
						break
		
		#If the rotate is legal
		if rotatePiece:
			self.currentShape.position = tempPosition
		#Otherwise, set the shape, ids and anchor back to the previous configuration
		else:
			self.currentShape.shape = oldShape
			self.currentShape.ids = oldIds
			self.currentShape.anchor = [old_rel_anchorRow,old_rel_anchorCol]
	
	#Check if move is legal
	def checkLegalMove(self, newPosition, changeIdx, row, col):
		isLegal = True
		#If the piece was shifted vertically
		if changeIdx == 0:
			#If the new position is <0 or >numRows
			if (newPosition< 0 or newPosition> numRows-1):
				isLegal = False
			elif self.board.grid[newPosition][self.currentShape.position[row][col][1]] !=emptyColor:
				isLegal = False
		#If the piece was shifted horizontally
		elif changeIdx == 1:
			#If the new position is <0 or > numCols
			if (newPosition< 0 or newPosition> numCols-1):
				isLegal = False
			elif self.board.grid[self.currentShape.position[row][col][0]][newPosition] !=emptyColor:
				isLegal = False
		
		return isLegal
		
	#Check if rotate is legal
	def checkLegalRotate(self, row, col):
		isLegal = True
		if (row < 0) or (row>numRows-1):
			isLegal = False
		elif (col < 0) or (col>numCols-1):
			isLegal = False
		elif self.board.grid[row][col] !=emptyColor:
			isLegal = False
		
		return isLegal
		
	#Check if block has reached the bottom
	def checkBottom (self):
		bottomReached = False
		for iRow in range(len(self.currentShape.position)):
			for iCol in range(len(self.currentShape.position[iRow])):
				if self.currentShape.shape[iRow][iCol]:	
					#Check if block has reached the bottom of the board
					if self.currentShape.position[iRow][iCol][0] == numRows - 1:
						bottomReached = True
					#Check if block has touched another block
					elif self.board.grid[self.currentShape.position[iRow][iCol][0]+1][self.currentShape.position[iRow][iCol][1]] != emptyColor:
						bottomReached = True
		return bottomReached			
	
	#Key pressed event handler
	def keyPressed (self, event):
		#If the left key is pressed
		if event.keysym == "Left":
			self.handleMove("left")
		#If the right key is pressed
		elif event.keysym == "Right":
			self.handleMove("right")
		#If the down key is pressed
		elif event.keysym == "Down":
			self.handleMove("down")
		#If the up key is pressed
		elif event.keysym == "Up":
			self.rotatePiece()
	
	#Draws the board
	def drawBoard(self):
		for iRow in range (numRows):
			for iCol in range(numCols):
				theColor = self.board.grid[iRow][iCol]
				self.board.ids[iRow][iCol] = self.drawCell(iCol*cellDim,iRow*cellDim,iCol*cellDim+cellDim,iRow*cellDim+cellDim,lineColor,theColor)

	#Repaints the board
	def repaintBoard (self):
		for iRow in range(numRows):
			for iCol in range(numCols):
				id = self.board.ids[iRow][iCol]
				theColor = self.board.grid[iRow][iCol]
				if theColor == emptyColor:
					self.canvas.itemconfigure(id, fill = theColor, outline = lineColor)
				else:
					self.canvas.itemconfigure(id, fill = theColor, outline = edgeColor)
	
	#Draws a shape			
	def drawShape (self):
		theColor = self.currentShape.color
		for iRow in range (len(self.currentShape.shape)):
			for iCol in range(len(self.currentShape.shape[iRow])):
				notEmpty = self.currentShape.shape[iRow][iCol]
				if notEmpty:
				#if notEmpty and (self.board.grid[self.currentShape.position[iRow][iCol][0]][self.currentShape.position[iRow][iCol][1]] == emptyColor):
					x_1 = cellDim*self.currentShape.position[iRow][iCol][1]
					x_2 = cellDim*self.currentShape.position[iRow][iCol][1]+cellDim
					y_1 = cellDim*self.currentShape.position[iRow][iCol][0]
					y_2 = cellDim*self.currentShape.position[iRow][iCol][0]+cellDim
					self.currentShape.ids[iRow][iCol] = self.drawCell(x_1,y_1,x_2,y_2,edgeColor,theColor)

	#Draws a cell on the board and returns its ID
	def drawCell(self,topLeft_x, topLeft_y, bottomRight_x, bottom_right_y, lineColor, fillColor):
		id = self.canvas.create_rectangle (topLeft_x, topLeft_y, bottomRight_x, bottom_right_y,
		outline=lineColor, fill=fillColor)
		self.canvas.pack(fill = BOTH, expand = 1)
		return id

	#Deletes a game piece from the canvas
	def deleteShape (self):
		for iRow in range(len(self.currentShape.ids)):
			for iCol in range(len(self.currentShape.ids[iRow])):
				if self.currentShape.ids[iRow][iCol] > 0:
					self.canvas.delete(self.currentShape.ids[iRow][iCol])

	
#Main function
if __name__ == '__main__':
	#Create a new window
	root = Tk()
	root.geometry("300x450+300+300")
	root.title("Tetris")
	
	newGame = GameController(root)
		
	root.mainloop()		
	






