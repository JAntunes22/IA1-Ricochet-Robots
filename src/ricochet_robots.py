# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

from search import Problem, Node, astar_search, breadth_first_tree_search, \
	depth_first_tree_search, greedy_search
import sys


class RRState:
	state_id = 0

	def __init__(self, board):
		self.board = board
		self.id = RRState.state_id
		RRState.state_id += 1

	def __lt__(self, other):
		""" Este método é utilizado em caso de empate na gestão da lista
		de abertos nas procuras informadas. """
		return self.id < other.id


class Board:
	class Cell:
		def __init__(self, x, y):
			self.up = None
			self.right = None
			self.down = None
			self.left = None
			
			self.x = x
			self.y = y

			self.target = None
			self.robot = None

		def setUp(self, p):
			self.up = p

		def setDown(self, p):
			self.down = p

		def setRight(self, p):
			self.right = p

		def setLeft(self, p):
			self.left = p

		def getUp(self):
			return self.up

		def getDown(self):
			return self.down

		def getRight(self):
			return self.right

		def getLeft(self):
			return self.left

		def getPosition(self):
			return (self.x, self.y)

		def addRobot(self, robot):
			if not self.robot:
				self.robot = robot
			else:
				pass
		
		def removeRobot(self):
			if self.robot:
				self.robot = None
			else:
				pass

		def setTarget(self, target):
			self.target = target
		
	
	""" Representacao interna de um tabuleiro de Ricochet Robots. """
	def __init__(self, n, robots, target, barriers):
		self.grid = [[Board.Cell(i, j) for i in range(n)] for j in range(n)]
		self.target = self.grid[target[2] - 1][target[1] - 1]
		self.target.setTarget(target[0])
		self.n = n # grid size

		for robot in robots:
			c = self.grid[robot[2]-1][robot[1]-1]
			c.addRobot(robot[0])

			if(robot[0] == 'Y'):
				self.yellow = c
			elif(robot[0] == 'R'):
				self.red = c
			elif(robot[0] == 'G'):
				self.green = c
			elif(robot[0] == 'B'):
				self.blue = c
		
		for y in range(0, n):
			for x in range(0, n):
				if x < (n - 1):
					self.grid[y][x].setRight(self.grid[y][x+1])
					self.grid[y][x+1].setLeft(self.grid[y][x])
				if y < (n - 1):
					self.grid[y][x].setDown(self.grid[y+1][x])
					self.grid[y+1][x].setUp(self.grid[y][x])

		
		for barrier in barriers:
			c = self.grid[barrier[1] - 1][barrier[0] - 1]
			if(barrier[2] == 'u'):
				c.setUp(None)
			elif(barrier[2] == 'r'):
				c.setRight(None)
			elif(barrier[2] == 'd'):
				c.setDown(None)
			elif(barrier[2] == 'l'):
				c.setLeft(None)
				

	def robot_position(self, robot: str):
		""" Devolve a posição atual do robô passado como argumento. """
		if(robot[0] == 'Y'):
			return self.yellow.getPosition()
		elif(robot[0] == 'R'):
			return self.red.getPosition()
		elif(robot[0] == 'G'):
			return self.green.getPosition()
		elif(robot[0] == 'B'):
			return self.blue.getPosition()

	
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
		else:
			raise NotImplementedError

		cell.removeRobot()

		if direction == 'u':
			while cell.up is not None:
				cell = cell.up
		elif direction == 'r':
			while cell.right is not None:
				cell = cell.right
		elif direction == 'd':
			while cell.down is not None:
				cell = cell.down
		elif direction == 'l':
			while cell.left is not None:
				cell = cell.left
		else:
			cell.addRobot(robot)
			raise NotImplementedError

		cell.addRobot(robot)

def parse_instance(filename: str) -> Board:
	""" Lê o ficheiro cujo caminho é passado como argumento e retorna
	uma instância da classe Board. """

	robots = []
	barriers = []

	file = open(filename, "r")

	n = int(file.readline())
	for i in range(0, n):
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
		self.initial = RRState(Board)

	def actions(self, state: RRState):
		""" Retorna uma lista de ações que podem ser executadas a
		partir do estado passado como argumento. """
		return ["move_blue_top", "move_red_top", "move_yellow_top", "move_green_top", \
				"move_blue_right", "move_red_right", "move_yellow_right", "move_green_right", \
				"move_blue_down", "move_red_down", "move_yellow_down", "move_green_down", \
				"move_blue_left", "move_red_left", "move_yellow_left", "move_green_left",]

	def result(self, state: RRState, action):
		""" Retorna o estado resultante de executar a 'action' sobre
		'state' passado como argumento. A ação retornada deve ser uma
		das presentes na lista obtida pela execução de
		self.actions(state). """
		if action == "move_blue_top":
			return state.board.robot_move('B', 't')
		elif action == "move_red_top":
			return state.board.robot_move('R', 't')
		elif action == "move_yellow_top":
			return state.board.robot_move('Y', 't')
		elif action == "move_green_top":
			return state.board.robot_move('G', 't')
		elif action == "move_blue_right":
			return state.board.robot_move('B', 'r')
		elif action == "move_red_right":
			return state.board.robot_move('R', 'r')
		elif action == "move_yellow_right":
			return state.board.robot_move('Y', 'r')
		elif action == "move_green_right":
			return state.board.robot_move('G', 'r')
		elif action == "move_blue_down":
			return state.board.robot_move('B', 'd')
		elif action == "move_red_down":
			return state.board.robot_move('R', 'd')
		elif action == "move_yellow_down":
			return state.board.robot_move('Y', 'd')
		elif action == "move_green_down":
			return state.board.robot_move('G', 'd')
		elif action == "move_blue_left":
			return state.board.robot_move('B', 'l')
		elif action == "move_red_left":
			return state.board.robot_move('R', 'l')
		elif action == "move_yellow_left":
			return state.board.robot_move('Y', 'l')
		elif action == "move_green_left":
			return state.board.robot_move('G', 'l')

		
	def goal_test(self, state: RRState):
		""" Retorna True se e só se o estado passado como argumento é
		um estado objetivo. Deve verificar se o alvo e o robô da
		mesma cor ocupam a mesma célula no tabuleiro. """
		robot = None
		if state.board.target.target == 'Y':
			robot = state.board.yellow
		elif state.board.target.target == 'R':
			robot = state.board.red
		elif state.board.target.target == 'G':
			robot = state.board.green
		elif state.board.target.target == 'B':
			robot = state.board.blue

		return robot.getPosition() == state.board.target.getPosition()

	def h(self, node: Node):
		""" Função heuristica utilizada para a procura A*. """
		#TODO


if __name__ == "__main__":
	# TODO:
	# Ler o ficheiro de input de sys.argv[1],
	# Usar uma técnica de procura para resolver a instância,
	# Retirar a solução a partir do nó resultante,
	# Imprimir para o standard output no formato indicado.

	board = parse_instance(sys.argv[1])

	
	pass
