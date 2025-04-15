from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MatrixCls:
	"""Matrix commands group definition. 3 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("matrix", core, parent)

	@property
	def row(self):
		"""row commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_row'):
			from .Row import RowCls
			self._row = RowCls(self._core, self._cmd_group)
		return self._row

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:ANTenna:INVerse:MATRix:STATe \n
		Snippet: value: bool = driver.source.cemulation.mimo.antenna.inverse.matrix.get_state() \n
		No command help available \n
			:return: ant_mod_inv_matrix: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:MIMO:ANTenna:INVerse:MATRix:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, ant_mod_inv_matrix: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:ANTenna:INVerse:MATRix:STATe \n
		Snippet: driver.source.cemulation.mimo.antenna.inverse.matrix.set_state(ant_mod_inv_matrix = False) \n
		No command help available \n
			:param ant_mod_inv_matrix: No help available
		"""
		param = Conversions.bool_to_str(ant_mod_inv_matrix)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MIMO:ANTenna:INVerse:MATRix:STATe {param}')

	def clone(self) -> 'MatrixCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MatrixCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
