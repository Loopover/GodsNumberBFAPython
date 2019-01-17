#import pyximport; pyximport.install(pyimport=True)
import copy
import tracemalloc
import os
import linecache
def switchTheStuff(board,currentNum,start,j,side):
	if side == 1:
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
		c = tuple(switchTheStuff(board,currentNum,start,j,1) for currentNum,start in enumerate(board))
		if c not in boards:
			foundA.append(tuple(c))
			#print(c)
			foundL = True
	for j in range(len(board)):
		locnumber += 1
		c = tuple(switchTheStuff(board,currentNum,start,j,-1) for currentNum,start in enumerate(board))
		if c not in boards:
			foundA.append(tuple(c))
			#print(c)
			foundL = True
	return (locnumber,foundA,foundL)
def getNewPositions(board):
	locnumber = 0
	found = set()
	for k in [1,-1]:
		for j in range(len(board)):
			locnumber += 2
			c = board[:j] + (board[j][k:]+board[j][:k],) + board[j+1:]
			found.add(tuple(c))
			c = tuple(switchTheStuff(board,currentNum,start,j,k) for currentNum,start in enumerate(board))
			found.add(tuple(c))
	return (found,locnumber)

def display_top(snapshot, key_type='lineno', limit=3):
	snapshot = snapshot.filter_traces((
		tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
		tracemalloc.Filter(False, "<unknown>"),
	))
	top_stats = snapshot.statistics(key_type)

	print("Top %s lines" % limit)
	for index, stat in enumerate(top_stats[:limit], 1):
		frame = stat.traceback[0]
		# replace "/path/to/module/file.py" with "module/file.py"
		filename = os.sep.join(frame.filename.split(os.sep)[-2:])
		print("#%s: %s:%s: %.1f KiB" % (index, filename, frame.lineno, stat.size / 1024))
		line = linecache.getline(frame.filename, frame.lineno).strip()
		if line:
			print('    %s' % line)

	other = top_stats[limit:]
	if other:
		size = sum(stat.size for stat in other)
		print("%s other: %.1f KiB" % (len(other), size / 1024))
	total = sum(stat.size for stat in top_stats)
	print("Total allocated size: %.1f KiB" % (total / 1024))
