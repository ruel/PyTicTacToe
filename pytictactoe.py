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

import os, random, time

# Classes #################################################################################

# Class for players (user and cpu)
class Player:
	def __init__(self, arg, arg2):
		self.name = arg
		self.wep = arg2
		self.moves = 0
		self.first = False
		self.won = False

# Class for the cells
class BoardCell:
	def __init__(self, arg, arg2, arg3):
		self.x = arg
		self.y = arg2
		self.num = arg3
		self.empty = True
		self.content = ' '
		
# Main program flow ########################################################################
def main():
	ru, rc, rd = 0, 0, 0
	while True:
		# Choose weapon!
		uwep, cwep = choosewep()
		# Create the user and cpu players
		user = Player('User', uwep)
		cpu = Player('CPU', cwep)
		# Toss the coin!
		won = cointoss()
		if won:
			while True:
				fr = raw_input('Who goes first (U)ser or (C)PU? ')
				if fr == 'U':
					user.first = True
					break
				elif fr == 'C':
					cpu.first = True
					break
		else:
			cpu.first = True
		print user.name if user.first else cpu.name, 'goes first.'
		# Timeout 5 seconds
		print 'Clearing screen in 3 seconds (Get Ready!)'
		time.sleep(3)
		# Let the game begin
		tgame(user, cpu)
		# Show the winner
		if user.won:
			ru += 1
			winner = user
		elif cpu.won:
			rc += 1
			winner = cpu
		else:
			rd += 1
			winner = Player('DRAW', '-')
		print '\nWINNER:', winner.name, '(' + winner.wep + ')'
		print 'Moves:', winner.moves
		# Record
		print '\nRecord:\tUser:', ru, '\n\tCPU:', rc, '\n\tDRAW:', rd
		# Play Again?
		while True:
			pa = raw_input('\nPlay again? [Y]es or [N]o: ')
			if pa == 'Y' or pa == 'N':
				break
		if pa == 'Y':
			cls()
		else:
			break
	print 
	
# Sub functions ###############################################################################
	
# Sub function for choosing between X and O
def choosewep():
	while True:
		uwep = raw_input('Please choose your weapon (X or O): ')
		if uwep == 'X':
			cwep = 'O'
			break
		elif uwep == 'O':
			cwep = 'X'
			break
		else:
			print 'Invalid Input. Try again.'
	return [uwep, cwep]

# Coin Toss sub function
def cointoss():
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

# Draw the board for the game
def drawboard(bcont):
	cls()
	boardstr = ''
	print boardstr + '\n'
	for i in range(3):
		boardstr += '\t'
		if i == 0:
			boardstr += '      |       |      \n\t'
		for j in range(3):
			boardstr += '  ' + bcont[i][j].content
			if j != 2:
			    boardstr += '   | ' 
		boardstr += '\n'
		if i != 2:
			boardstr += '\t      |       |      \n\t------|-------|------\n\t      |       |      \n'
		else:
			boardstr += '\t      |       |      \n'
	print boardstr
	
# Initialize the cells on the board
def boardinit():
	bcont = [ [ None for j in range(3) ] for i in range(3) ]
	c = 1
	for i in range(3):
		for j in range(3):
			bcont[i][j] = BoardCell(i, j, c)
			c += 1
	return bcont
	
# Insert X or O
def bdraw(num, bcont, player):
	for i in range(3):
		for j in range(3):
			#print bcont[i][j].num, num
			if bcont[i][j].num == num:
				if bcont[i][j].empty:
					bcont[i][j].content = player.wep
					bcont[i][j].empty = False
					return True
	return False

# User's turn
def usermove(user, bcont):
	user.moves += 1
	while True:
		num = 0
		try:
			num = int(raw_input('Your turn [1-9]: '))
		except:
			print 'Invalid input'
		if num >= 1 and num <= 9:
				if bdraw(num, bcont, user):
					break
			 
# CPU's turn
def cpumove(cpu, user, bcont):
	cpu.moves += 1
	num = getwnum(bcont, cpu.wep, cpu.wep)
	if num == -2:
		num = getwnum(bcont, user.wep, cpu.wep)
	while True:
		if num <= 0:
			num = random.randrange(1, 10)
		if bdraw(num, bcont, cpu):
			break
		num = -1
		
# Get the board contents
def getboard(bcont, wep):
	xo = []
	for i in range(3):
		for j in range(3):
			if not bcont[i][j].empty:
				if wep == 'T':
					xo.append(bcont[i][j].num)
				else:
					if bcont[i][j].content == wep:
						xo.append(bcont[i][j].num)
	return xo

# Check if there's a winning/breaking cell
def getwnum(bcont, wep, cwep):
	num = -2
	t = getboard(bcont, wep)
	ex = getboard(bcont, 'T')
	# Line 1 of 8
	if isin(1, t) and isin(2, t) and not isin(3, ex):
		num = 3
	elif isin(2, t) and isin(3, t) and not isin(1, ex):
		num = 1
	elif isin(1, t) and isin(3, t) and not isin(2, ex):
		num = 2
		
	# Line 2 of 8
	elif isin(4, t) and isin(5, t) and not isin(6, ex):
		num = 6
	elif isin(5, t) and isin(6, t) and not isin(4, ex):
		num = 4
	elif isin(4, t) and isin(6, t) and not isin(5, ex):
		num = 5
		
	# Line 3 of 8
	elif isin(7, t) and isin(8, t) and not isin(9, ex):
		num = 9
	elif isin(8, t) and isin(9, t) and not isin(7, ex):
		num = 7
	elif isin(7, t) and isin(9, t) and not isin(8, ex):
		num = 8
		
	# Line 4 of 8
	elif isin(1, t) and isin(5, t) and not isin(9, ex):
		num = 9
	elif isin(5, t) and isin(9, t) and not isin(1, ex):
		num = 1
	elif isin(1, t) and isin(9, t) and not isin(5, ex):
		num = 5
		
	# Line 5 of 8
	elif isin(3, t) and isin(5, t) and not isin(7, ex):
		num = 7
	elif isin(5, t) and isin(7, t) and not isin(3, ex):
		num = 3
	elif isin(3, t) and isin(7, t) and not isin(5, ex):
		num = 5
		
	# Line 6 of 8
	elif isin(1, t) and isin(4, t) and not isin(7, ex):
		num = 7
	elif isin(4, t) and isin(7, t) and not isin(1, ex):
		num = 1
	elif isin(1, t) and isin(7, t) and not isin(4, ex):
		num = 4
		
	# Line 7 of 8
	elif isin(2, t) and isin(5, t) and not isin(8, ex):
		num = 8
	elif isin(5, t) and isin(8, t) and not isin(2, ex):
		num = 2
	elif isin(2, t) and isin(8, t) and not isin(5, ex):
		num = 5
		
	# Line 8 of 8
	elif isin(3, t) and isin(6, t) and not isin(9, ex):
		num = 9
	elif isin(6, t) and isin(9, t) and not isin(3, ex):
		num = 3
	elif isin(3, t) and isin(9, t) and not isin(6, ex):
		num = 6
	else:
		if wep == cwep:
			num == 0
	return num
	
# Checking if a value exists in a list
def isin(val, list):
	if val in list:
		return True
	return False

# Internal number checking. To prevent, messy code (sort of)
def checknum(xo):
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

# Check if someone won already
def checkwin(bcont, wep):
	xo = getboard(bcont, wep)
	if checknum(xo):
		return True
	return False
	
def checktie(bcont):
	t = getboard(bcont, 'T')
	if len(t) == 9:
		return True
	return False
	
# Main Game function
def tgame(user, cpu):	
	bcont = boardinit()
	drawboard(bcont)
	if cpu.first:
		cpumove(cpu, user, bcont)
		drawboard(bcont)
	while True:
		usermove(user, bcont)
		drawboard(bcont)
		if checktie(bcont):
			break
		if checkwin(bcont, user.wep):
			user.won = True
			break
		cpumove(cpu, user, bcont)
		drawboard(bcont)
		if checktie(bcont):
			break
		if checkwin(bcont, cpu.wep):
			cpu.won = True
			break

# We're not in a module, aren't we? #############################################################
if __name__ == '__main__':
	main()