from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NameCls:
	"""Name commands group definition. 12 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("name", core, parent)

	@property
	def auto(self):
		"""auto commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_auto'):
			from .Auto import AutoCls
			self._auto = AutoCls(self._core, self._cmd_group)
		return self._auto

	def get_value(self) -> str:
		"""SCPI: HCOPy:FILE:[NAME] \n
		Snippet: value: str = driver.hardCopy.file.name.get_value() \n
		Determines the file name and path to save the hard copy, provided automatic naming is disabled. Note: If you have enabled
		automatic naming, the instrument automatically generates the file name and directory, see 'Automatic naming'. \n
			:return: name: string
		"""
		response = self._core.io.query_str('HCOPy:FILE:NAME?')
		return trim_str_response(response)

	def set_value(self, name: str) -> None:
		"""SCPI: HCOPy:FILE:[NAME] \n
		Snippet: driver.hardCopy.file.name.set_value(name = 'abc') \n
		Determines the file name and path to save the hard copy, provided automatic naming is disabled. Note: If you have enabled
		automatic naming, the instrument automatically generates the file name and directory, see 'Automatic naming'. \n
			:param name: string
		"""
		param = Conversions.value_to_quoted_str(name)
		self._core.io.write(f'HCOPy:FILE:NAME {param}')

	def clone(self) -> 'NameCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NameCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
