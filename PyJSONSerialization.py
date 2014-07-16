import json
from datetime import datetime

"""Parses a python object from a JSON string. Every Object which should be loaded needs a constuctor that doesn't need any Arguments.
Arguments: The JSON string; the module which contains the class, the parsed object is instance of."""
def load(jsonString, module):
	def _load(d, module):
		if isinstance(d, list):
			l = []
			for item in d:
				l.append(_load(item, module))
			return l
		elif isinstance(d, dict) and "type" in d: #object
			t = d["type"]
			try:
				o = module[t]()
			except KeyError, e:
				raise ClassNotFoundError("Class '%s' not found in the given module!" % t)
			except TypeError, e:
				raise TypeError("Make sure there is an constuctor that doesn't take any arguments (class: %s)" % t)
			for key in d:
				if key != "type":
					setattr(o, key, _load(d[key], module))
			return o
		elif isinstance(d, dict): #dict
			rd = {}
			for key in d:
				rd[key] = _load(d[key], module)
			return rd
		else:
			return d
	d = json.loads(jsonString)
	return _load(d, module)

"""Dumps a python object to a JSON string. Argument: Python object"""
def dump(obj):
	def _dump(obj, path):
		if isinstance(obj, list):
			l = []
			i = 0
			for item in obj:
				l.append(_dump(item, path + "/[" + str(i) + "]"))
				i+=1
			return l
		elif isinstance(obj, dict): #dict
			rd = {}
			for key in obj:
				rd[key] = _dump(obj[key], path + "/" + key)
			return rd
		elif isinstance(obj, str) or isinstance(obj, unicode) or isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, long) or isinstance(obj, complex) or isinstance(obj, bool) or type(obj).__name__ == "NoneType":
			return obj
		else:
			d = {}
			d["type"] = obj.__class__.__name__
			for key in obj.__dict__:
				d[key] = _dump(obj.__dict__[key], path + "/" + key)
			return d
	return json.dumps(_dump(obj, "/"))

class ClassNotFoundError(Exception):
	"""docstring for ClassNotFoundError"""
	def __init__(self, msg):
		super(ClassNotFoundError, self).__init__(msg)		

if __name__ == "__main__":
	class Test1(object):
		def __init__(self):
			super(Test1, self).__init__()
			self.one = []
			for x in range(10):
				self.one.append(Test3())
			self.two = {"2": Test2()}
			self.null = None

	class Test2(object):
		def __init__(self):
			super(Test2, self).__init__()
			self.test3 = Test3()

	class Test3(object):
		def __init__(self):
			super(Test3, self).__init__()
			self.string = "string"
			self.integer = 123
			self.boolean = True

	t = Test1()
	print t
	print ""
	j = dump(t)
	print j
	print ""
	print load(j, globals()).two["2"]
