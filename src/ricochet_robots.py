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
		self.grid = [[Board.Cell(j, i) for i in range(n)] for j in range(n)]
		self.target = self.grid[target[1] - 1][target[2] - 1]
		self.target.setTarget(target[0])
		self.n = n # grid size

		for robot in robots:
			c = self.grid[robot[1]-1][robot[2]-1]
			c.addRobot(robot[0])

			if(robot[0] == 'Y'):
				self.yellow = c
			elif(robot[0] == 'R'):
				self.red = c
			elif(robot[0] == 'G'):
				self.green = c
			elif(robot[0] == 'B'):
				self.blue = c
		
		for x in range(0, n):
			for y in range(0, n):
				if y < (n - 1):
					self.grid[x][y].setRight(self.grid[x][y+1])
					self.grid[x][y+1].setLeft(self.grid[x][y])
				if x < (n - 1):
					self.grid[x][y].setDown(self.grid[x+1][y])
					self.grid[x+1][y].setUp(self.grid[x][y])

		
		for barrier in barriers:
			c = self.grid[barrier[0] - 1][barrier[1] - 1]
			if(barrier[2] == 'u'):
				c.up.setDown(None)
				c.setUp(None)
			elif(barrier[2] == 'r'):
				c.right.setLeft(None)
				c.setRight(None)
			elif(barrier[2] == 'd'):
				c.down.setUp(None)
				c.setDown(None)
			elif(barrier[2] == 'l'):
				c.left.setRight(None)
				c.setLeft(None)
	
	def getTarget(self):
		return self.target
				

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
			while cell.up and not cell.up.robot:
				cell = cell.up
		elif direction == 'r':
			while cell.right and not cell.right.robot:
				cell = cell.right
		elif direction == 'd':
			while cell.down and not cell.down.robot:
				cell = cell.down
		elif direction == 'l':
			while cell.left and not cell.left.robot:
				cell = cell.left
		else:
			cell.addRobot(robot)
			raise NotImplementedError

		cell.addRobot(robot)

		return RRState(self)

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
		super().__init__(RRState(board), board.target)

	def actions(self, state: RRState):
		""" Retorna uma lista de ações que podem ser executadas a
		partir do estado passado como argumento. """
		
		possible_actions = []

		if state.board.yellow.up and not state.board.yellow.up.robot:
			possible_actions.append("move_yellow_up")
		if state.board.red.up and not state.board.red.up.robot:
			possible_actions.append("move_red_up")
		if state.board.blue.up and not state.board.blue.up.robot:
			possible_actions.append("move_blue_up")
		if state.board.green.up and not state.board.green.up.robot:
			possible_actions.append("move_green_up")
		if state.board.yellow.down and not state.board.yellow.down.robot:
			possible_actions.append("move_yellow_down")
		if state.board.red.down and not state.board.red.down.robot:
			possible_actions.append("move_red_down")
		if state.board.blue.down and not state.board.blue.down.robot:
			possible_actions.append("move_blue_down")
		if state.board.green.down and not state.board.green.down.robot:
			possible_actions.append("move_green_down")
		if state.board.yellow.right and not state.board.yellow.right.robot:
			possible_actions.append("move_yellow_right")
		if state.board.red.right and not state.board.red.right.robot:
			possible_actions.append("move_red_right")
		if state.board.blue.right and not state.board.blue.right.robot:
			possible_actions.append("move_blue_right")
		if state.board.green.right and not state.board.green.right.robot:
			possible_actions.append("move_green_right")
		if state.board.yellow.left and not state.board.yellow.left.robot:
			possible_actions.append("move_yellow_left")
		if state.board.red.left and not state.board.red.left.robot:
			possible_actions.append("move_red_left")
		if state.board.blue.left and not state.board.blue.left.robot:
			possible_actions.append("move_blue_left")
		if state.board.green.left and not state.board.green.left.robot:
			possible_actions.append("move_green_left")

		return possible_actions

	def result(self, state: RRState, action):
		""" Retorna o estado resultante de executar a 'action' sobre
		'state' passado como argumento. A ação retornada deve ser uma
		das presentes na lista obtida pela execução de
		self.actions(state). """

		if action == "move_blue_up":
			return state.board.robot_move('B', 'u')
		elif action == "move_red_up":
			return state.board.robot_move('R', 'u')
		elif action == "move_yellow_up":
			return state.board.robot_move('Y', 'u')
		elif action == "move_green_up":
			return state.board.robot_move('G', 'u')
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
	
		if self.goal.target == 'Y':
			robot =  node.state.board.yellow
		elif self.goal.target == 'R':
			robot =  node.state.board.red
		elif self.goal.target == 'G':
			robot =  node.state.board.green
		elif self.goal.target == 'B':
			robot =  node.state.board.blue

		x, y = robot.x, robot.y
		xt, yt = self.goal.x, self.goal.y
		return abs(x - xt) + abs(y - yt)


if __name__ == "__main__":
	# Ler o ficheiro de input de sys.argv[1],
	# Usar uma técnica de procura para resolver a instância,
	# Retirar a solução a partir do nó resultante,
	# Imprimir para o standard output no formato indicado.

	board = parse_instance(sys.argv[1])
	ricochet_robots = RicochetRobots(board)

	'''for x in range(0, 4):
		for y in range(0, 4):
			print(f'({x},{y})', end=' ') if board.grid[x][y].robot == None else print(board.grid[x][y].robot, end=' ')

		print('')'''


	result = astar_search(ricochet_robots, ricochet_robots.h)

