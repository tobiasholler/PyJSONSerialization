PyJSONSerialization
===================

This is a small library which serializes and parses Python objects to and from readable JSON files.

Works with Python 2.7, all other versions not tested.

This example is all Documentation you'll get:

### Example:

```python
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

test1 = Test1()
test1Json = dump(t)
print test1Json # Outputs: '{"null": null, "type": "Test1", "two": {"2": {"test3": {"integer": 123, "boolean": true, ...
print load(test1Json, globals()).two["2"] # Outputs: <__main__.Test2 object at 0x7fa4a4bf1250>
```
