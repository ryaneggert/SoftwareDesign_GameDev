# grid_matrix.property

ring_none = []
full_board = []

# for num in range(8):
# 	ring_none.append(None)
# print ring_none

# for num in range(4):
# 	full_board.append(ring_none)
# print full_board

for num in range(4):
	full_board.append([])
	for num2 in range(8):
		full_board[num].append(None)

# full_board = [[None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]

full_board[1][2] = 'Potato'
print full_board