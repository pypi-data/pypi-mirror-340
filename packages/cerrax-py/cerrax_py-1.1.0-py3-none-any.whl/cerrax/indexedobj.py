#-==@h1 Indexed Object

#-== A chimera of data structures,
# this object is an ordered, indexed hashtable with
# the ability to access attributes by both dot notation and bracket notation.


RESERVED = ['RESERVED', '_reserved', '_objs', '_keyindex', '_generated_key',
		'_generate_key', '_add_object', 'get', 'keys', 'values',
		'items', 'index', 'insert', 'append', 'remove', 'popindex',
		'pop', 'extend', 'reverse', 'copy', 'clear',
	]

#-==@class
class IndexedObject():
	"""-== This object provides the benefits of several data
	structures simultaneously.

	-== *Attribute Access*
	* Dot notation - /myobj.attr
	* Bracket notation (key) - /myobj['attr']
	* Bracket notation (index) - /myobj[2]
	* Built-in /getattr() function - /getattr(myobj, 'attr', None)
	* Instance /get() method - /myobj.get('attr', None)
	* Can use /len() to get number of attributes
	
	-== *Attribute Storage*
	* Attributes are ordered
	* Attributes can change order
	* New attributes can be inserted
		at any index
	* Keys, values, and key-value pairs 
		can be iterated in order
	* Can handle both keyed and keyless
		data in the same object

	@note
	Because of the inherent complexity of this data structure,
	it is not advised to create subclasses of /IndexedObject.
	It is best to create a new class and include /IndexedObject
	as one of its members.
	"""

	_reserved = []

	#-==@method
	def __init__(self, *args, **kwargs):
		"""-== Creates a new /IndexedObject .
		This constructor creates the attributes differently based on the
		/args or /kwargs supplied to it. The constructor *cannot* accept
		both /args and /kwargs together. The object must be instantiated
		with either only /args, or only /kwargs. All attributes will be
		inserted into the object in the order they are passed to the constructor.

		-== If /arg values are tuples, it is assumed they are /-(key, value)-/
		tuples, and will assign attributes as such. Any other /arg values are
		considered keyless values, and will have an automatically generated key
		assigned to them. /kwargs are inserted exactly they are passed, with the
		attribute name being the /kwarg name, and the value being the /kwarg value.
		Because the /args can be read as either key-value tuples, or keyless values,
		you can get around the /arg & /kwarg limitation by inserting keyword args
		as key-value tuples instead.

		-== Keyless data is always given an automatically generated key anytime it is
		inserted into this object. Generated keys follow the pattern of /_x_ where /x
		is an auto-incrementing counter that starts at zero. The increment is based on the
		lifetime of the object. For example, an /IndexedObject with 8 keyless attributes
		has a previously generated key of /_7_ . If a new keyless attribute is added,
		this will increment to /_8_ . However, if a keyless attribute is removed, the
		generated key does not decrement.
		
		-== @note
		Objects which will frequently change the number of keyless attributes should not
		use /IndexedObject , since there is a possibility of encountering the upper bounds
		of Python's built in /int type (typically 2,147,483,647 for most Python interpreters).
		"""

		self._objs = {}
		self._keyindex = []
		self._generated_key = 0

		if len(args) > 0 and len(kwargs) > 0:
			raise ValueError('Cannot provide args and kwargs together in IndexedObject constructor')

		for entry in args:
			if isinstance(entry, tuple) and len(entry) == 2:
				self.append(*entry)
			else:
				self.append(entry)

		for key, val in kwargs.items():
			self.append(key, val)


	def __getattr__(self, key):
		if key in RESERVED:
			try:
				val = self.__dict__[key]
			except KeyError:
				val = self.__class__.__dict__[key]
			return val
		elif isinstance(key, int):
			return self._objs[self._keyindex[key]]
		elif key in self._objs.keys():
			return self._objs[key]
		raise AttributeError('{}'.format(key))

	def __setattr__(self, key, value):
		if key in RESERVED:
			self.__dict__[key] = value
		elif isinstance(key, int):
			self._objs[self._keyindex[key]] = value
		elif key in self._objs.keys():
			self._objs[key] = value
		else:
			raise AttributeError('{}'.format(key))

	def __len__(self):
		return len(self._keyindex)

	def __getitem__(self, key):
		return self.__getattr__(key)

	def __setitem__(self, key, value):
		self.__setattr__(key, value)

	def _generate_key(self):
		keystr = '_{}_'.format(self._generated_key)
		self._generated_key += 1
		return keystr

	def _add_object(self, arg1, arg2=None):
		if arg1 is None:
			raise TypeError('expected at least 1 argument')
		if arg2 is None:
			key = self._generate_key()
			value = arg1
		else:
			key = arg1
			value = arg2

		if key in RESERVED or key in self._reserved:
			raise ValueError('{} is a reserved key'.format(key))
		if key in self.keys():
			raise ValueError('Cannot add {}, key already exists'.format(key))

		self._objs[key] = value
		return key, value

	#-==@method
	def get(self, key, default=None):
		#-== @params
		#	key: 	the attribute name to retrieve
		#	default: the value to return if the /key is not found
		#-== @return
		# The attribute indentified by /key ,
		# or the /default value if the key is not found

		return getattr(self, key, default)

	#-==@method
	def keys(self):
		#-==@return
		# A list of the keys in this object, in order.

		return self._keyindex.copy()

	#-==@method
	def values(self):
		#-==@return
		# A list of the values in this object, in order.

		valuelist = []
		for key in self._keyindex:
			valuelist.append(self._objs[key])
		return valuelist

	#-==@method
	def items(self):
		#-==@return
		# A list of the /-(key, value)-/ tuples in this object, in order.

		itemslist = []
		for key in self._keyindex:
			itemslist.append((key, self._objs[key]))
		return itemslist

	#-==@method
	def index(self, key):
		#-== @params
		#	key: the key to search for
		#-== @return
		# The index of a given /key .

		for i in range(len(self._keyindex)):
			if self._keyindex[i] == key:
				return i
		raise ValueError('key {} not found'.format(key))

	#-==@method
	def insert(self, index, arg1, arg2=None):
		#-== @params
		#	index:	the index to insert the attribute
		#	arg1:	either the value, or the key to insert
		#	arg2:	the value to insert
		#
		#-== * To insert keyless data: /- myobj.insert(2, value) -/
		#    * To insert keyed data:   /- myobj.insert(2, key, value) -/

		if index < 0 or index >= len(self):
			raise IndexError
		key, value = self._add_object(arg1, arg2)
		self._keyindex.insert(index, key)

	#-==@method
	def append(self, arg1, arg2=None):
		#-== @params
		#	arg1:	either the value, or the key to append
		#	arg2:	the value to append
		#
		#-== * To append keyless data: /- myobj.append(value) -/
		#    * To append keyed data:   /- myobj.append(key, value) -/

		key, value = self._add_object(arg1, arg2)
		self._keyindex.append(key)

	#-==@method
	def popindex(self, index):
		#-== @params
		#	index:	index of the attribute to remove
		#-== @return
		# A tuple of the key and value at the /index

		retkey = self._keyindex[index]
		retobj = self._objs.pop(retkey)
		self._keyindex.pop(index)
		return retkey, retobj

	#-==@method
	def pop(self, key=None):
		#-== @params
		#	key:	key of the attribute to remove
		#-== @return
		# A tuple of the index and value at the /key

		if key:
			keyindex = self.index(key)
			self._keyindex.pop(keyindex)
		else:
			key = self._keyindex.pop()
			keyindex = len(self._keyindex)
		return keyindex, self._objs.pop(key)

	#-==@method
	def extend(self, new_obj):
		#-== @params
		#	new_obj: a /list , /dict , or /IndexedObject
		#				to append to this object
		#
		#-== Appends all of the attributes of /new_obj to this object.
		# The attributes will be appended in order with the same keys.
		# If duplicate keys are detected, a /KeyError is raised.
		# When /new_obj is a /list , each value will have a key
		# auto-generated before being appended.
		#
		#-== @note
		# Because duplicate keys are not allowed, using /extend() with
		# an /IndexedObject that has keyless attributes will most likely
		# cause a /KeyError to be raised.

		if isinstance(new_obj, (list, tuple)):
			for item in new_obj:
				self.append(item)
		elif isinstance(new_obj, dict) or isinstance(new_obj, IndexedObject):
			overlapping_keys = set(self.keys()) & set(new_obj.keys())
			if len(overlapping_keys) > 0:
				raise KeyError('cannot extend, keys {} already exist'.format(overlapping_keys))
			for key, value in new_obj.items():
				self.append(key, value)
		else:
			raise TypeError('cannot extend IndexedObject with type {}'.format(new_obj.__class__.__name__))

	#-==@method
	def reverse(self):
		#-== Reverses the order attributes in place.

		self._keyindex.reverse()

	#-==@method
	def copy(self):
		#-== @return
		# A shallow copy of this object.

		new_obj = IndexedObject()
		new_obj._keyindex = self._keyindex.copy()
		new_obj._objs = self._objs.copy()
		new_obj._generated_key = self._generated_key
		return new_obj

	#-==@method
	def clear(self):
		#-== Removes all attributes from this object
		# and resets the generated key to zero.

		self._keyindex.clear()
		self._objs.clear()
		self._generated_key = 0


