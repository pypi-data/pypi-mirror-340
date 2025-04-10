#-== @h1
# Grid Data Structure
#
#-== A data structure to manipulate
# and traverse a 2-dimensional array
# in an intutive manner.

#-== @class
class Grid:
	#-== @attributes
	#	width :		the width of the grid
	#	height:		the height of the grid
	#	focus_xy:	a tuple of coordinates within the grid data
	#				indicating the cell which is currently in focus
	#	focus_obj:	the data within the cell which is currently focused
	#	grid:		the raw 2-D array which stores the data

	#-== @method
	def __init__(self, width = None, height = None, default = None, data = None):
		#-== @params
		#	width:		the width of the grid
		#	height:		the height of the grid
		#	default:	a default value to insert into empty cells
		#	data:		a 2-D array of data to populate the new grid
		#
		#-== A /Grid object is a rectangluar 2-dimensional array, meaning that
		# each row has the same number of columns. The size of this structure can be
		# determined either by the provided /width and /height , or by the /data
		# passed into it.
		# The /width and /height must be specified unless /data has been provided.
		# If /data is provided without /width or /height, the dimensions of the /data
		# will be used as the size of the /Grid object.
		#
		#-==@note
		# The /data is assumed to be rectangular as well, and the height and width
		# are determined by the first row and first column, respectively.
		# If any rows below the first row are longer, they will be truncated
		# and that data will not be inserted into the /Grid object.
		#
		#-== If both /data and the /width or /height is provided, the appropriate
		# dimension of the grid will be sized according to that value. If the
		# value is greater than the dimension of the /data , the /default value will
		# be inserted into those cells. If the value is less than the dimension of
		# the /data , then those cells will not be copied to the /Grid object.
		# (See the /populate() method below for more details)

		self.width = width
		self.height = height
		if data is not None and len(data) > 0 and width is None:
			self.width = len(data[0])
		if data is not None and height is None:
			self.height = len(data)

		self.default = default
		self.grid = []
		self.focus_xy = [0, 0]
		self.focus_obj = None

		if data is None:
			if self.width is None or self.height is None:
				raise ValueError('Width and height must be provided if no data')
		self.populate(data)

	#-== @method
	def populate(self, data):
		#-== @params
		#	data:	a 2-D array of data to populate the grid
		#
		#-== This method fills in the /Grid object with the contents of each cell
		# of the provided /data object. The insertion to each cell
		# of the /Grid object is a simple assignment. This means that literal values
		# will be copies, but Python objects will be references.
		#
		#-== @note
		# Because Python always does pass by reference, the assignment which takes place
		# in /populate() places a *reference* to any Python object which is in the cell
		# of /data . If you wish to have shallow or deep copies in the /Grid object,
		# you must do those before passing the /data to this method.

		self.grid = []
		for row in range(self.height):
			self.grid.append([])
			for column in range(self.width):
				value = self.default
				if data is not None and row < len(data):
					if data[row] is not None and column < len(data[row]):
						value = data[row][column]
				self.grid[row].append(value)

	#-== @method
	def check_bounds(self, value, upper, lower, raise_exc=True):
		#-== @params
		#	value:		the value to check
		#	upper: 		the maximum threshold of /value
		#	lower:		the minimum threshold of /value
		#	raise_exc:	a boolean indicating if an /IndexError
		#					should be raised when /value exceeds
		#					the /upper or /lower bounds
		#-== @return
		#	The /value, possibly adjusted by the bounds, or raise an /IndexError
		#
		#-== Usually, this method simply returns the unaltered /value, unless it
		# exceeds one or both of the bounds provided ( /upper and /lower ).
		# However, if /raise_exc is set to /False , then this method will adjust
		# the /value to stay within the bounds. If the /value exceeds one
		# of the bounds, the method returns the bound itself, since it is
		# the furthest value allowed.
		# This can be useful in situations where you implicitly need
		# the value to stay within the bounds without raising an error.

		if value > upper:
			if raise_exc:
				raise IndexError
			else:
				return upper
		if value < lower:
			if raise_exc:
				raise IndexError
			else:
				return lower
		return value

	#-== @method
	def focus(self, x=None, y=None, stay_in_bounds=False):
		#-== @params
		#	x:		the horizontal coordinate to focus on in the grid
		#	y:		the vertical coordinate to focus on in the grid
		#	stay_in_bounds:	a boolean indicating if this method should
		#						automatically correct the focus coordinates
		#						if the provided /x or /y values are outside
		#						the bounds of the grid
		#-== @return
		# The content of the cell at ( /x , /y ) in the grid.
		#
		#-== A major concept of the /Grid is *focus*, also referred to in some other
		# data structures and data mangement utilities as a "cursor". The focus of
		# the /Grid is the specific cell which can be read or manipulated.
		# This method will use the provided /x and/or /y values to set the focus
		# of the /Grid to a specific cell. The coordinate system in use with a /Grid
		# object is such that the cell in the top left corner is coordinate (0, 0).
		# and values along the x and y axes are positive integer values.
		# There are no decimal or negative values in a /Grid object's coordinates.
		# If the provided /x or /y values are not within the bounds of the grid,
		# an /IndexError will be raised, unless /stay_in_bounds is set to /True (see below).
		#
		#-== If an /x or /y value is not provided, this method will use the current
		# focus /x or /y coordinate. Calling /focus() , with no arguments,
		# simply retuns the currently focused cell contents. Calling /focus(x=2)
		# would move the focus to the third column of the currently focused row.
		#
		#-== @note
		# Keep in mind that the /Grid coordinate system starts at (0,0), so the
		# first column is an x-coordinate of 0, not 1.
		#
		#-== If /stay_in_bounds is set to /True , then this method implicitly limits
		# the focus to the bounds of the grid. Any value outside the bounds,
		# will be automatically corrected to the bound(s) that were crossed.
		# This is useful for implementations that may attempt to exceed the grid bounds,
		# but don't necessarily need to raise an exception when it occurs.

		if x is None:
			x = self.focus_xy[0]
		if y is None:
			y = self.focus_xy[1]

		y = self.check_bounds(y, len(self.grid)-1, 0, not stay_in_bounds)
		x = self.check_bounds(x, len(self.grid[y])-1, 0, not stay_in_bounds)

		self.focus_xy = [x, y]
		self.focus_obj = self.grid[y][x]
		return self.focus_obj

	#-== @method
	def focus_up(self, amount=1, stay_in_bounds=False):
		#-== @params
		#	amount:			the number of cells to shift the focus upwards
		#	stay_in_bounds:	a boolean indicating if this method should
		#						automatically correct the focus coordinates
		#						if it is outside the bounds of the grid
		#-== @return
		# The content of the cell that is /amount number
		# of cells above the currently focused cell.
		#
		#-== This a convenience method which shifts the focus of the /Grid object
		# upwards by an /amount. It directly calls the /focus() method (see above).

		if amount < 0:
			raise ValueError
		translate = self.focus_xy[1] - amount
		return self.focus(y=translate, stay_in_bounds=stay_in_bounds)

	#-== @method
	def focus_down(self, amount=1, stay_in_bounds=False):
		#-== @params
		#	amount:			the number of cells to shift the focus downwards
		#	stay_in_bounds:	a boolean indicating if this method should
		#						automatically correct the focus coordinates
		#						if it is outside the bounds of the grid
		#-== @return
		# The content of the cell that is /amount number
		# of cells below the currently focused cell.
		#
		#-== This a convenience method which shifts the focus of the /Grid object
		# downwards by an /amount. It directly calls the /focus() method (see above).

		if amount < 0:
			raise ValueError
		translate = self.focus_xy[1] + amount
		return self.focus(y=translate, stay_in_bounds=stay_in_bounds)

	#-== @method
	def focus_left(self, amount=1, stay_in_bounds=False):
		#-== @params
		#	amount:			the number of cells to shift the focus to the left
		#	stay_in_bounds:	a boolean indicating if this method should
		#						automatically correct the focus coordinates
		#						if it is outside the bounds of the grid
		#-== @return
		# The content of the cell that is /amount number
		# of cells to the left of the currently focused cell.
		#
		#-== This a convenience method which shifts the focus of the /Grid object
		# to the left by an /amount. It directly calls the /focus() method (see above).

		if amount < 0:
			raise ValueError
		translate = self.focus_xy[0] - amount
		return self.focus(x=translate, stay_in_bounds=stay_in_bounds)

	#-== @method
	def focus_right(self, amount=1, stay_in_bounds=False):
		#-== @params
		#	amount:			the number of cells to shift the focus to the right
		#	stay_in_bounds:	a boolean indicating if this method should
		#						automatically correct the focus coordinates
		#						if it is outside the bounds of the grid
		#-== @return
		# The content of the cell that is /amount number
		# of cells to the right of the currently focused cell.
		#
		#-== This a convenience method which shifts the focus of the /Grid object
		# to the right by an /amount. It directly calls the /focus() method (see above).

		if amount < 0:
			raise ValueError
		translate = self.focus_xy[0] + amount
		return self.focus(x=translate, stay_in_bounds=stay_in_bounds)

	#-== @method
	def replace_focused(self, newitem):
		#-== Replaces the item currently in focus with /newitem .
		#@params
		# newitem: the data to replace the currently focused item in the grid

		x = self.focus_xy[0]
		y = self.focus_xy[1]
		self.grid[y][x] = newitem


	#-== @method
	def typewriter_traverse(self):
		#-== @return
		# a /TypewriterGridIterator for use in a /for loop

		return iter(TypewriterGridIterator(self))

	#-== @method
	def serpentine_traverse(self):
		#-== @return
		# a /SerpentineGridIterator for use in a /for loop

		return iter(SeprentineGridIterator(self))

	#-== @method
	def vertical_typewriter_traverse(self):
		#-== @return
		# a /VerticalTypewriterGridIterator for use in a /for loop

		return iter(VerticalTypewriterGridIterator(self))

	#-== @method
	def vertical_serpentine_traverse(self):
		#-== @return
		# a /VerticalSerpentineGridIterator for use in a /for loop

		return iter(VerticalSeprentineGridIterator(self))

	#-== @method
	def spiral_in_traverse(self):
		#-== @return
		# a /SpiralInGridIterator for use in a /for loop

		return iter(SpiralInGridIterator(self))

#-== @class
class AbstractGridIterator:
	#-== An abstract class for deriving iterators for a /Grid object.
	#
	#-== /GridIterator classes are unique in that
	# they don't simply return the content of the cell,
	# they also return the x and y coordinates of the cell.
	# When using a /GridIterator ,
	# you must account for these extra values:
	# @codeblock
	# mygrid = Grid(24, 12)
	# for x, y, item in mygrid.typwriter_traverse():
	#//   # do stuff
	# @codeblockend

	def __init__(self, gridobj):
		self.gridobj = gridobj

	def __iter__(self):
		self.gridobj.focus(0,0)
		self.end = False
		self._prepare_iter()
		return self

	def __next__(self):
		if not self.end:
			result = self.gridobj.focus()
			x = self.gridobj.focus_xy[0]
			y = self.gridobj.focus_xy[1]
			self._next_step()
			return x, y, result
		raise StopIteration

	def _prepare_iter(self):
		pass

	def _next_step(self):
		raise NotImplemented

#-== @class
class TypewriterGridIterator(AbstractGridIterator):
	#-== "Typewriter" traversal is the most common way
	# to traverse a 2-dimensional array.
	# The iterator starts at (0, 0), and moves along the x-axis.
	# When it reaches the end of the row, it goes down
	# to the next row, and begins again at the 0 x-coordinate
	# and travels along the x-axis.
	#
	#-== *Example:*
	# @codeblock
	# 1234
	# 5678    typwriter
	# 9000    traversal = 123456789000
	# @codeblockend

	def _next_step(self):
		try:
			self.gridobj.focus_right()
		except IndexError:
			try:
				self.gridobj.focus_down()
				self.gridobj.focus(x=0)
			except IndexError:
				self.end = True

#-== @class
class SeprentineGridIterator(AbstractGridIterator):
	#-== "Serpentine" traversal is another fairly common
	# traversal method. The iterator starts at (0, 0),
	# and moves along the x-axis, just like a typewriter
	# traversal. However, when it reaches the end of the row,
	# it simply changes direction after moving down a row.
	#
	#-== *Example:*
	# @codeblock
	# 1234
	# 5678    serpentine
	# 9000    traversal = 123487659000
	# @codeblockend

	LEFT = 'left'
	RIGHT = 'right'

	def _prepare_iter(self):
		self.direction = self.RIGHT

	def _next_step(self):
		try:
			if self.direction == self.LEFT:
				self.gridobj.focus_left()
			else:
				self.gridobj.focus_right()
		except IndexError:
			try:
				self.gridobj.focus_down()
				if self.direction == self.LEFT:
					self.direction = self.RIGHT
				else:
					self.direction = self.LEFT
			except IndexError:
				self.end = True

#-== @class
class VerticalTypewriterGridIterator(AbstractGridIterator):
	#-== "Vertical Typewriter" traversal is the same as typewriter,
	# except turned vertically. Starting at (0, 0), the iterator
	# moves down the column. When it reaches the end of the column,
	# it goes to the next one and, starting again at the 0 y-coordinate,
	# traverses down teh column.
	#
	#-== *Example:*
	# @codeblock
	# 1234    vertical
	# 5678    typewriter
	# 9000    traversal = 159260370480
	# @codeblockend

	def _next_step(self):
		try:
			self.gridobj.focus_down()
		except IndexError:
			try:
				self.gridobj.focus_right()
				self.gridobj.focus(y=0)
			except IndexError:
				self.end = True

#-== @class
class VerticalSeprentineGridIterator(AbstractGridIterator):
	#-== "Vertical Serpentine" traversal is the same as serpentine,
	# except turned vertically. Starting at (0, 0), the iterator
	# moves down the column. When it reaches the end of the column,
	# it changes direction, and traverses up the next column.
	#
	#-== *Example:*
	# @codeblock
	# 1234    vertical
	# 5678    serpentine
	# 9000    traversal = 159062370084
	# @codeblockend

	UP = 'up'
	DOWN = 'down'

	def _prepare_iter(self):
		self.direction = self.DOWN

	def _next_step(self):
		try:
			if self.direction == self.DOWN:
				self.gridobj.focus_down()
			else:
				self.gridobj.focus_up()
		except IndexError:
			try:
				self.gridobj.focus_right()
				if self.direction == self.UP:
					self.direction = self.DOWN
				else:
					self.direction = self.UP
			except IndexError:
				self.end = True

#-== @class
class SpiralInGridIterator(AbstractGridIterator):
	#-== "Spiral In" traversal is concerned with visiting
	# the outermost cells of the grid before visiting those
	# closer to the center. The iterator starts at (0, 0),
	# and moves along the x-axis. However, upon reaching
	# the end of the x-axis, it moves down the column,
	# then backwards across the bottom row, and upwards
	# towards the start. Upon reaching the start, the iterator
	# moves down 1 row and does the same movement again,
	# 1 "layer" deeper (and thus 1 unit closer to the center)
	# than before. This continues until it reaches
	# the center of the grid.
	#
	#-== *Example:*
	# @codeblock
	# 1234
	# 5678    spiral in
	# 9000    traversal = 123480009567
	# @codeblockend

	LEFT = 'left'
	RIGHT = 'right'
	UP = 'up'
	DOWN = 'down'

	def _prepare_iter(self):
		self.items = 0
		self.total_items = self.gridobj.width * self.gridobj.height
		self.direction = self.RIGHT
		self.top_edge = 0
		self.left_edge = 0
		self.right_edge = self.gridobj.width - 1
		self.bottom_edge = self.gridobj.height - 1

	def _next_step(self):
		if self.direction == self.RIGHT:
			if self.gridobj.focus_xy[0] == self.right_edge:
				self.top_edge += 1
				self.direction = self.DOWN
			else:
				self.gridobj.focus_right()
		if self.direction == self.DOWN:
			if self.gridobj.focus_xy[1] == self.bottom_edge:
				self.right_edge -= 1
				self.direction = self.LEFT
			else:
				self.gridobj.focus_down()
		if self.direction == self.LEFT:
			if self.gridobj.focus_xy[0] == self.left_edge:
				self.bottom_edge -= 1
				self.direction = self.UP
			else:
				self.gridobj.focus_left()
		if self.direction == self.UP:
			if self.gridobj.focus_xy[1] == self.top_edge:
				self.left_edge += 1
				self.direction = self.RIGHT
				self.gridobj.focus_right()
			else:
				self.gridobj.focus_up()

		self.items += 1
		if self.items >= self.total_items:
			self.end = True


