from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BbCls:
	"""Bb commands group definition. 25 total commands, 3 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bb", core, parent)

	@property
	def bnc(self):
		"""bnc commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_bnc'):
			from .Bnc import BncCls
			self._bnc = BncCls(self._core, self._cmd_group)
		return self._bnc

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 6 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def generator(self):
		"""generator commands group. 5 Sub-classes, 3 commands."""
		if not hasattr(self, '_generator'):
			from .Generator import GeneratorCls
			self._generator = GeneratorCls(self._core, self._cmd_group)
		return self._generator

	def get_connection(self) -> bool:
		"""SCPI: TEST:BB:CONNection \n
		Snippet: value: bool = driver.test.bb.get_connection() \n
		No command help available \n
			:return: connection: No help available
		"""
		response = self._core.io.query_str('TEST:BB:CONNection?')
		return Conversions.str_to_bool(response)

	def clone(self) -> 'BbCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BbCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
