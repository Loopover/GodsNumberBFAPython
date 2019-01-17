#import pyximport; pyximport.install(pyimport=True)
import copy
import tracemalloc
import os
import linecache
def switchTheStuff(board,currentNum,start,j,side):
	isSide = currentNum == ((-(side)^1)%3)*(len(board)-1)
	return start[:j]+(board[int(isSide)*(-(((side)^1)%3))+int(not isSide)*(currentNum+side)][j],)+start[j+1:]
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
