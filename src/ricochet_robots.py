# ricochet_robots.py: Template para implementaceo do 1 projeto de Inteligencia Artificial 2020/2021.
# Devem alterar as classes e funcoes neste ficheiro de acordo com as instrucoes do enunciado.
# Alem das funcoes e classes ja definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 07:
# 92446 David Baptista
# 92498 Joao Antunes

from search import Problem, Node, astar_search, breadth_first_tree_search, \
	depth_first_tree_search, greedy_search, compare_searchers
import sys
import copy


class RRState:
	state_id = 0

	def __init__(self, board):
		self.board = board
		self.id = RRState.state_id
		RRState.state_id += 1

	def __lt__(self, other):
		""" Este metodo e utilizado em caso de empate na gesteo da lista
		de abertos nas procuras informadas. """
		return self.board.manhattan_distance() < other.board.manhattan_distance()

	def __hash__(self):
		return hash((('Y', self.board.yellow), ('G', self.board.green), ('B', self.board.blue), ('R', self.board.red)))

	def __eq__(self, other):
		if isinstance(other, RRState) and isinstance(other.board, Board):
			return self.board.yellow == other.board.yellow and self.board.red == other.board.red \
				and self.board.green == other.board.green and self.board.blue == other.board.blue
		return False


class Board:
	target_surrounded = False

	""" Representacao interna de um tabuleiro de Ricochet Robots. """
	def __init__(self, n, robots, target, barriers):
		self.grid = [[float("inf") for i in range(n)] for j in range(n)]
		self.n = n	# grid size
		self.targetColour = target[0]
		self.targetCell = (target[1] - 1, target[2] - 1)
		self.barriers = []

		for robot in robots:
			if(robot[0] == 'Y'):
				self.yellow = (robot[1] - 1, robot[2] - 1)
			elif(robot[0] == 'R'):
				self.red = (robot[1] - 1, robot[2] - 1)
			elif(robot[0] == 'G'):
				self.green = (robot[1] - 1, robot[2] - 1)
			elif(robot[0] == 'B'):
				self.blue = (robot[1] - 1, robot[2] - 1)
		
		# criacao das barreiras
		for barrier in barriers:
			xy = (barrier[0] - 1, barrier[1] - 1)
			self.barriers.append((xy, barrier[2]))
			second_barrier = None

			if barrier[2] == 'u':
				if self.get_up(xy):
					second_barrier = (self.get_up(xy), 'd')
					self.barriers.append(second_barrier)
			elif barrier[2] == 'd':
				if self.get_down(xy):
					second_barrier = (self.get_down(xy), 'u')
					self.barriers.append(second_barrier)
			elif barrier[2] == 'r':
				if self.get_right(xy):
					second_barrier = (self.get_right(xy), 'l')
					self.barriers.append(second_barrier)
			elif barrier[2] == 'l':
				if self.get_left(xy):
					second_barrier = (self.get_left(xy), 'r')
					self.barriers.append(second_barrier)

			if xy[0] == self.targetCell[0] and xy[1] == self.targetCell[1]:
				Board.target_surrounded = True
			if second_barrier and second_barrier[0][0] == self.targetCell[0] and second_barrier[0][1] == self.targetCell[1]:
				Board.target_surrounded = True

	''' para debugging '''
	def __str__(self):
		for x in range(0, self.n):
			for y in range(0, self.n):
				if self.has_robot((x, y)):
					if self.yellow == (x,y):
						r = 'Y'
					elif self.red == (x,y):
						r = 'R'
					elif self.blue == (x, y):
						r = 'B'
					elif self.green == (x, y):
						r = 'G'
				print(f'{r}', end=' ') if self.has_robot((x,y)) else print(f'({x},{y})', end=' ')
				#print(f'{self.grid[x][y]}', end=' ')
			print('')
	
		return ''

	'''	def __eq__(self, other):
		if isinstance(other, Board):
			return self.yellow == other.yellow and self.red == other.red and self.green == other.green and self.blue == other.blue
		return False'''

	def calculateSteps(self):
		level = 0
		fifo = [self.get_target()]
		calculated = []

		for x in range(0, self.n):
			for y in range(0, self.n):
				self.grid[x][y] = float('inf')

		self.grid[self.targetCell[0]][self.targetCell[1]] = 0

		while fifo:
			cell = fifo.pop(0)
			calculated.append(cell)
			level = self.grid[cell[0]][cell[1]]

			c = cell
			while self.get_up(c) and not self.has_barrier(c, 'u'):
				c = self.get_up(c)
				if c in calculated:
					break

				if self.grid[c[0]][c[1]] > level + 1:
					self.grid[c[0]][c[1]] = level + 1
					
					if self.has_robot(c):
						calculated.append(c)
						break
					else:
						fifo.append(c)

				elif self.grid[c[0]][c[1]] == level + 1 and not self.has_robot(c):
					continue
				else:
					break
			c = cell
			while self.get_left(c) and not self.has_barrier(c, 'l'):
				c = self.get_left(c)
				if c in calculated:
					break

				if self.grid[c[0]][c[1]] > level + 1:
					self.grid[c[0]][c[1]] = level + 1
					
					if self.has_robot(c):
						calculated.append(c)
						break
					else:
						fifo.append(c)

				elif self.grid[c[0]][c[1]] == level + 1 and not self.has_robot(c):
					continue
				else:
					break
			c = cell
			while self.get_down(c) and not self.has_barrier(c, 'd'):
				c = self.get_down(c)
				if c in calculated:
					break

				if self.grid[c[0]][c[1]] > level + 1:
					self.grid[c[0]][c[1]] = level + 1
					
					if self.has_robot(c):
						calculated.append(c)
						break
					else:
						fifo.append(c)

				elif self.grid[c[0]][c[1]] == level + 1 and not self.has_robot(c):
					continue
				else:
					break
			c = cell
			while self.get_right(c) and not self.has_barrier(c, 'r'):
				c = self.get_right(c)
				if c in calculated:
					break

				if self.grid[c[0]][c[1]] > level + 1:
					self.grid[c[0]][c[1]] = level + 1
					
					if self.has_robot(c):
						calculated.append(c)
						break
					else:
						fifo.append(c)

				elif self.grid[c[0]][c[1]] == level + 1 and not self.has_robot(c):
					continue
				else:
					break

	def get_up(self, cell):
		if(cell[0] == 0):
			return None
		else:
			return (cell[0] - 1, cell[1])

	def get_down(self, cell):
		if(cell[0] == self.n - 1):
			return None
		else:
			return (cell[0] + 1, cell[1])

	def get_left(self, cell):
		if(cell[1] == 0):
			return None
		else:
			return (cell[0], cell[1] - 1)

	def get_right(self, cell):
		if(cell[1] == self.n - 1):
			return None
		else:
			return (cell[0], cell[1] + 1)
	
	def has_robot(self, c):
		return c == self.yellow or c == self.blue or c == self.red or c == self.green

	def has_barrier(self, c, d):
		for barrier in self.barriers:
			if barrier[0] == c and barrier[1] == d:
				return True
		return False

	def get_target(self):
		''' Devolve as coordenadas para a celula target '''
		return self.targetCell
				
	def robot_position(self, robot: str):
		""" Devolve a posiceo atual do robo passado como argumento. """
		if(robot[0] == 'Y'):
			return (self.yellow[0] + 1, self.yellow[1] + 1) 
		elif(robot[0] == 'R'):
			return (self.red[0] + 1, self.red[1] + 1) 
		elif(robot[0] == 'G'):
			return (self.green[0] + 1, self.green[1] + 1) 
		elif(robot[0] == 'B'):
			return (self.blue[0] + 1, self.blue[1] + 1) 

	
	def robot_move(self, robot: str, direction: str):
		cell = None

		if(robot == 'Y'):
			cell = self.yellow
		elif(robot == 'R'):
			cell = self.red
		elif(robot == 'G'):
			cell = self.green
		elif(robot == 'B'):
			cell = self.blue

		if direction == 'u':
			while self.get_up(cell) and not self.has_robot(self.get_up(cell)) and not self.has_barrier(cell, direction):
				cell = self.get_up(cell)
		elif direction == 'r':
			while self.get_right(cell) and not self.has_robot(self.get_right(cell)) and not self.has_barrier(cell, direction):
				cell = self.get_right(cell)
		elif direction == 'd':
			while self.get_down(cell) and not self.has_robot(self.get_down(cell)) and not self.has_barrier(cell, direction):
				cell = self.get_down(cell)
		elif direction == 'l':
			while self.get_left(cell) and not self.has_robot(self.get_left(cell)) and not self.has_barrier(cell, direction):
				cell = self.get_left(cell)

		if(robot == 'Y'):
		 	self.yellow = cell
		elif(robot == 'R'):
			self.red = cell
		elif(robot == 'G'):
			self.green = cell
		elif(robot == 'B'):
			self.blue = cell

	def robot_target(self):
		""" Retorna o robot que e da mesma cor que o target"""
		if self.targetColour == 'Y':
			robot = self.yellow
		elif self.targetColour  == 'R':
			robot = self.red
		elif self.targetColour  == 'G':
			robot = self.green
		elif self.targetColour  == 'B':
			robot = self.blue

		return robot
	
	def check_target_surroundings(self):
		''' Verifica se o board tem um robo ao lado do target, para parar o robo da cor do target, e verifica se o caminho direto para
		o target e accessivel, caso tenha um caminho. Incrementa 1 nas condicoes desfavoraveis'''
		if not self.target_surrounded:
			target = self.get_target()

			if self.has_robot(self.get_up(target)):
				return 0
			if self.has_robot(self.get_down(target)):
				return 0
			if self.has_robot(self.get_right(target)):
				return 0
			if self.has_robot(self.get_left(target)):
				return 0
			
		return 1

	def manhattan_distance(self):
		robot = self.robot_target()
		x, y = robot[0], robot[1]
		xt, yt = self.targetCell[0], self.targetCell[1]
		
		return abs(x - xt) + abs(y - yt) 

def parse_instance(filename: str) -> Board:
	""" Le o ficheiro cujo caminho e passado como argumento e retorna
	uma instencia da classe Board. """

	robots = []
	barriers = []

	file = open(filename, "r")

	n = int(file.readline())
	for i in range(0, 4):
		input_str = file.readline()
		split_str = input_str.split()
		split_str[1] = int(split_str[1])
		split_str[2] = int(split_str[2])	
		robots.append(split_str)

	input_str = file.readline()
	target = input_str.split()
	target[1] = int(target[1])
	target[2] = int(target[2])

	m = int(file.readline())
	for i in range(0, m):
		input_str = file.readline()
		split_str = input_str.split()
		split_str[0] = int(split_str[0])
		split_str[1] = int(split_str[1])	
		barriers.append(split_str)

	return Board(n, robots, target, barriers)

class RicochetRobots(Problem):
	def __init__(self, board: Board):
		""" O construtor especifica o estado inicial. """
		self.initial = RRState(board)

	def actions(self, state: RRState):
		""" Retorna uma lista de acoes que podem ser executadas a
		partir do estado passado como argumento. """
		
		possible_actions = []

		yellow = state.board.yellow
		red = state.board.red
		blue = state.board.blue
		green = state.board.green

		if state.board.get_up(yellow) and not state.board.has_robot(state.board.get_up(yellow)) and not state.board.has_barrier(yellow, 'u'):
			possible_actions.append(("Y","u"))
		if state.board.get_up(red) and not state.board.has_robot(state.board.get_up(red)) and not state.board.has_barrier(red, 'u'):
			possible_actions.append(("R", "u"))
		if state.board.get_up(blue) and not state.board.has_robot(state.board.get_up(blue)) and not state.board.has_barrier(blue, 'u'):
			possible_actions.append(("B", "u"))
		if state.board.get_up(green) and not state.board.has_robot(state.board.get_up(green)) and not state.board.has_barrier(green, 'u'):
			possible_actions.append(("G", "u"))
		if state.board.get_down(yellow) and not state.board.has_robot(state.board.get_down(yellow)) and not state.board.has_barrier(yellow, 'd'):
			possible_actions.append(("Y", "d"))
		if state.board.get_down(red) and not state.board.has_robot(state.board.get_down(red)) and not state.board.has_barrier(red, 'd'):
			possible_actions.append(("R", "d"))
		if state.board.get_down(blue) and not state.board.has_robot(state.board.get_down(blue)) and not state.board.has_barrier(blue, 'd'):
			possible_actions.append(("B", "d"))
		if state.board.get_down(green) and not state.board.has_robot(state.board.get_down(green)) and not state.board.has_barrier(green, 'd'):
			possible_actions.append(("G", "d"))
		if state.board.get_right(yellow) and not state.board.has_robot(state.board.get_right(yellow)) and not state.board.has_barrier(yellow, 'r'):
			possible_actions.append(("Y", "r"))
		if state.board.get_right(red) and not state.board.has_robot(state.board.get_right(red)) and not state.board.has_barrier(red, 'r'):
			possible_actions.append(("R", "r"))
		if state.board.get_right(blue) and not state.board.has_robot(state.board.get_right(blue)) and not state.board.has_barrier(blue, 'r'):
			possible_actions.append(("B", "r"))
		if state.board.get_right(green) and not state.board.has_robot(state.board.get_right(green)) and not state.board.has_barrier(green, 'r'):
			possible_actions.append(("G", "r"))
		if state.board.get_left(yellow) and not state.board.has_robot(state.board.get_left(yellow)) and not state.board.has_barrier(yellow, 'l'):
			possible_actions.append(("Y", "l"))
		if state.board.get_left(red) and not state.board.has_robot(state.board.get_left(red)) and not state.board.has_barrier(red, 'l'):
			possible_actions.append(("R", "l"))
		if state.board.get_left(blue) and not state.board.has_robot(state.board.get_left(blue)) and not state.board.has_barrier(blue, 'l'):
			possible_actions.append(("B", "l"))
		if state.board.get_left(green) and not state.board.has_robot(state.board.get_left(green)) and not state.board.has_barrier(green, 'l'):
			possible_actions.append(("G", "l"))

		return possible_actions 

	def result(self, state: RRState, action):
		""" Retorna o estado resultante de executar a 'action' sobre
		'state' passado como argumento. A aceo retornada deve ser uma
		das presentes na lista obtida pela execuceo de
		self.actions(state). """
		board = copy.deepcopy(state.board)
		board.robot_move(action[0], action[1])

		return RRState(board)

	def goal_test(self, state: RRState):
		""" Retorna True se e so se o estado passado como argumento e
		um estado objetivo. Deve verificar se o alvo e o robo da
		mesma cor ocupam a mesma celula no tabuleiro. """

		return state.board.robot_target() == state.board.get_target()

	def h(self, node: Node):
		""" Funceo heuristica utilizada para a procura A*. """
		node.state.board.calculateSteps()
		robot = node.state.board.robot_target()
		i = node.state.board.check_target_surroundings()

		return node.state.board.grid[robot[0]][robot[1]] + i 


if __name__ == "__main__":
	# Ler o ficheiro de input de sys.argv[1],
	# Usar uma tecnica de procura para resolver a instencia,
	# Retirar a soluceo a partir do no resultante,
	# Imprimir para o standard output no formato indicado.
	# Ler tabuleiro do ficheiro "i1.txt":

	board = parse_instance(sys.argv[1])
	ricochet_robots = RicochetRobots(board)
	node = astar_search(ricochet_robots)
	print(node.depth)

	for e in node.solution():
		print(e[0] + " " + e[1])

	#compare_searchers([ricochet_robots], [], [breadth_first_tree_search])
