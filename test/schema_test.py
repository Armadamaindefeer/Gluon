import unittest
from library.datafield.validator.schema import validate
from library.datafield.validator.type import DATAFIELD_KEY_TYPE, DATAFIELD_TYPE

class TestSchemeValidator(unittest.TestCase):

	def test_scheme_not_type_key(self):
		schema = {"comment" : 1}
		self.assertFalse(validate(schema))

	def test_invalid_type_key(self):
		schema = {"type" : 1}
		self.assertFalse(validate(schema))

	def test_invalid_type(self):
		schema = {"type" : "test"}
		self.assertFalse(validate(schema))

	def test_valid_type_key(self):
		for type in DATAFIELD_TYPE:
			with self.subTest(type=type):
				schema = {"type" : type}
				self.assertTrue(validate(schema))

	def test_unknown_key(self):
		schema = {"type" : "string", "unknow" : 1}
		self.assertFalse(validate(schema))

	def test_skip_comment(self):
		schema = {"type" : "comment" , "value" : True}
		self.assertTrue(validate(schema))

	def test_default_invalid_type(self):
		for type in DATAFIELD_TYPE:
			if type =="comment":
				continue
			with self.subTest(type=type):
				schema = {"type" : type,"default" : print}
				self.assertFalse(validate(schema))

	def test_valid_default(self):
		for typename,type in DATAFIELD_TYPE.items():
			if typename == "comment":
				continue
			with self.subTest(typename=typename):
				schema_a = {"type" : typename,"default" : type()}
				self.assertTrue(schema_a)
				schema_b = {"type" : typename,"default" : None}
				self.assertTrue(schema_b)

	def test_invalid_key_type(self):
		for key in DATAFIELD_KEY_TYPE:
			with self.subTest(key=key):
				schema = {"type" : "string",key : print}
				self.assertFalse(validate(schema))

	def test_none_default_not_allowed(self):
		schema = {"type" : "string", "allowNone" : False,"default" : None}
		self.assertFalse(validate(schema))
