#import pyximport; pyximport.install(pyimport=True)
import copy
def switchTheStuff(board,currentNum,start,j,side):
	if side:
		if currentNum == len(board)-1:
			return (start[:j]+(board[0][j],)+start[j+1:])
		else:
			return (start[:j]+(board[currentNum+1][j],)+start[j+1:])
	else:
		if currentNum == 0:
			return start[:j]+(board[-1][j],)+start[j+1:]
		else:
			return start[:j]+(board[currentNum-1][j],)+start[j+1:]
def getFound(board, boards):
	#print(board)
	locnumber = 0
	foundA = []
	foundL = False
	for j, line in enumerate(board):
		for k in [1,-1]:
			locnumber += 1
			c = board[:j] + (line[k:]+line[:k],) + board[j+1:]
			if c not in boards:
				foundA.append(tuple(c))
				#print(c)
				foundL = True
	for j in range(len(board)):
		locnumber += 1
		c = tuple(switchTheStuff(board,currentNum,start,j,True) for currentNum,start in enumerate(board))
		if c not in boards:
			foundA.append(tuple(c))
			#print(c)
			foundL = True
	for j in range(len(board)):
		locnumber += 1
		c = tuple(switchTheStuff(board,currentNum,start,j,False) for currentNum,start in enumerate(board))
		if c not in boards:
			foundA.append(tuple(c))
			#print(c)
			foundL = True
	return (locnumber,foundA,foundL)
