#!/usr/bin/python

'''
	PyTicTacToe - Tic Tac Toe in Python
	http://ruel.me

	Copyright (c) 2010, Ruel Pagayon - ruel@ruel.me
	All rights reserved.

	Redistribution and use in source and binary forms, with or without
		* Redistributions of source code must retain the above copyright
		  notice, this list of conditions and the following disclaimer.
		* Redistributions in binary form must reproduce the above copyright
		  notice, this list of conditions and the following disclaimer in the
		  documentation and/or other materials provided with the distribution.
		* Neither the name of ruel.me nor the names of its contributors
		  may be used to endorse or promote products derived from this
		  script without specific prior written permission.

	THIS SCRIPT IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
	ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
	WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
	DISCLAIMED. IN NO EVENT SHALL RUEL PAGAYON BE LIABLE FOR ANY
	DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
	(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
	LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
	ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
	(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
	SCRIPT, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

	General Description: 	The CPU difficulty is Human-Like. Means, you can still WIN!
							I made it so, because I do not want this to be boring, and
							end up with loses and draws.
'''

import os, random, time, operator

'''
	Classes
'''

class Player:
	'''Class for players (user and cpu)'''
	def __init__(self, name, weapon):
		self.name = name
		self.weapon = weapon
		self.moves = 0
		self.first = False
		self.won = False

class BoardCell:
	'''Class for the cells'''
	def __init__(self, number):
		self.number = number
		self.empty = True
		self.content = ' '
		
'''
	Main Program Flow
'''
		
def main():
	recorduser, recordcpu, recorddraw = 0, 0, 0
	while True:
		# Toss the coin!
		won = cointoss()
		if won:
			user = Player('User', 'X')
			cpu = Player('CPU', 'O')
			user.first = True
		else:
			user = Player('User', 'O')
			cpu = Player('CPU', 'X')
			cpu.first = True
		print user.name if user.first else cpu.name, 'goes first.'
		# Timeout 5 seconds
		print 'Clearing screen in 3 seconds (Get Ready!)'
		time.sleep(3)
		# Let the game begin
		tgame(user, cpu)
		# Show the winner
		if user.won:
			recorduser += 1
			winner = user
		elif cpu.won:
			recordcpu += 1
			winner = cpu
		else:
			recorddraw += 1
			winner = Player('DRAW', '-')
		print '\nWINNER:', winner.name, '(' + winner.weapon + ')'
		print 'Moves:', winner.moves
		# Record
		print '\nRecord:\tUser:', recorduser, '\n\tCPU:', recordcpu, '\n\tDRAW:', recorddraw
		# Play Again?
		while True:
			choice = raw_input('\nPlay again? [Y]es or [N]o: ')
			if choice == 'Y' or choice == 'N':
				break
		if choice == 'Y':
			cls()
		else:
			break
	print 
	
'''
	Sub function section
'''

def cointoss():
	'''Coin Toss sub function'''
	won = False
	while True:
		choice = raw_input('Heads or Tails (H or T): ')
		if choice == 'H' or choice == 'T':
			print 'Tossing Coin..'
			coin = ['Heads', 'Tails'][random.randrange(0,2)]
			print '\n -- ', coin , ' -- \n'
			if  coin[0] == choice:
				won = True
			break
	return won

# Clear screen subfunction
def cls():
	# Cross-platform :)
	os.system('cls' if os.name == 'nt' else 'clear')

def drawboard(board):
	'''Draw the board for the game'''
	cls()
	boardstr = ''
	print boardstr + '\n'
	i = 0
	for row in board:
		boardstr += '\t'
		if i == 0:
			boardstr += '      |       |      \n\t'
		boardstr += '  {0}   |   {1}   |   {2}\n'.format(*[cell.content for cell in row])
		if i != 2:
			boardstr += '\t      |       |      \n\t------|-------|------\n\t      |       |      \n'
		else:
			boardstr += '\t      |       |      \n'
		i += 1
	print boardstr
	
def boardinit():
	'''Initialize the cells on the board'''
	return [[BoardCell((i + 1) + (j * 3)) for i in range(3)] for j in range(3)]

def bdraw(number, board, player):
	'''Insert X or O'''
	for i in range(3):
		for j in range(3):
			if board[i][j].number == number:
				if board[i][j].empty:
					board[i][j].content = player.weapon
					board[i][j].empty = False
					return True
	return False

def usermove(user, board):
	'''User's turn'''
	user.moves += 1
	while True:
		number = 0
		try:
			number = int(raw_input('Your turn [1-9]: '))
		except:
			print 'Invalid input'
		if number >= 1 and number <= 9:
				if bdraw(number, board, user):
					break
			 
def cpumove(cpu, user, board):
	'''CPU's turn'''
	cpu.moves += 1
	number = getwnumber(board, cpu.weapon, cpu.weapon)
	if number == -2:
		number = getwnumber(board, user.weapon, cpu.weapon)
	while True:
		if number <= 0:
			number = random.randrange(1, 10)
		if bdraw(number, board, cpu):
			break
		number = -1
		
def getboard(board, weapon):
	'''Get the board contents'''
	xo = []
	for i in range(3):
		for j in range(3):
			if not board[i][j].empty:
				if weapon == 'T':
					xo.append(board[i][j].number)
				else:
					if board[i][j].content == weapon:
						xo.append(board[i][j].number)
	return xo

def getwnumber(board, weapon, cweapon):
	'''Check if there's a winning/breaking cell'''
	number = -2
	t = getboard(board, weapon)
	ex = getboard(board, 'T')
	# Line 1 of 8
	if isin(1, t) and isin(2, t) and not isin(3, ex):
		number = 3
	elif isin(2, t) and isin(3, t) and not isin(1, ex):
		number = 1
	elif isin(1, t) and isin(3, t) and not isin(2, ex):
		number = 2
		
	# Line 2 of 8
	elif isin(4, t) and isin(5, t) and not isin(6, ex):
		number = 6
	elif isin(5, t) and isin(6, t) and not isin(4, ex):
		number = 4
	elif isin(4, t) and isin(6, t) and not isin(5, ex):
		number = 5
		
	# Line 3 of 8
	elif isin(7, t) and isin(8, t) and not isin(9, ex):
		number = 9
	elif isin(8, t) and isin(9, t) and not isin(7, ex):
		number = 7
	elif isin(7, t) and isin(9, t) and not isin(8, ex):
		number = 8
		
	# Line 4 of 8
	elif isin(1, t) and isin(5, t) and not isin(9, ex):
		number = 9
	elif isin(5, t) and isin(9, t) and not isin(1, ex):
		number = 1
	elif isin(1, t) and isin(9, t) and not isin(5, ex):
		number = 5
		
	# Line 5 of 8
	elif isin(3, t) and isin(5, t) and not isin(7, ex):
		number = 7
	elif isin(5, t) and isin(7, t) and not isin(3, ex):
		number = 3
	elif isin(3, t) and isin(7, t) and not isin(5, ex):
		number = 5
		
	# Line 6 of 8
	elif isin(1, t) and isin(4, t) and not isin(7, ex):
		number = 7
	elif isin(4, t) and isin(7, t) and not isin(1, ex):
		number = 1
	elif isin(1, t) and isin(7, t) and not isin(4, ex):
		number = 4
		
	# Line 7 of 8
	elif isin(2, t) and isin(5, t) and not isin(8, ex):
		number = 8
	elif isin(5, t) and isin(8, t) and not isin(2, ex):
		number = 2
	elif isin(2, t) and isin(8, t) and not isin(5, ex):
		number = 5
		
	# Line 8 of 8
	elif isin(3, t) and isin(6, t) and not isin(9, ex):
		number = 9
	elif isin(6, t) and isin(9, t) and not isin(3, ex):
		number = 3
	elif isin(3, t) and isin(9, t) and not isin(6, ex):
		number = 6
	else:
		if weapon == cweapon:
			number == 0
	return number

def isin(val, list):
	'''Checking if a value exists in a list'''
	return val in list

def checknumber(xo):
	'''Internal number checking. To prevent, messy code (sort of)'''
	if isin(1, xo) and isin(2, xo) and isin(3, xo) or \
	isin(4, xo) and isin(5, xo) and isin(6, xo) or \
	isin(7, xo) and isin(8, xo) and isin(9, xo) or \
	isin(1, xo) and isin(5, xo) and isin(9, xo) or \
	isin(3, xo) and isin(5, xo) and isin(7, xo) or \
	isin(1, xo) and isin(4, xo) and isin(7, xo) or \
	isin(2, xo) and isin(5, xo) and isin(8, xo) or \
	isin(3, xo) and isin(6, xo) and isin(9, xo):
		return True
	return False

def checkwin(board, weapon):
	'''Check if someone won already'''
	xo = getboard(board, weapon)
	if checknumber(xo):
		return True
	return False
	
def checktie(board):
	'''Check if it's a draw'''
	t = getboard(board, 'T')
	if len(t) == 9:
		return True
	return False
	
def tgame(user, cpu):
	'''Main Game function'''
	board = boardinit()
	drawboard(board)
	if cpu.first:
		cpumove(cpu, user, board)
		drawboard(board)
	while True:
		usermove(user, board)
		drawboard(board)
		if checktie(board):
			break
		if checkwin(board, user.weapon):
			user.won = True
			break
		cpumove(cpu, user, board)
		drawboard(board)
		if checktie(board):
			break
		if checkwin(board, cpu.weapon):
			cpu.won = True
			break

'''
	Lines below is the entry point of the script
'''

if __name__ == '__main__':
	main()

'''End of Code'''