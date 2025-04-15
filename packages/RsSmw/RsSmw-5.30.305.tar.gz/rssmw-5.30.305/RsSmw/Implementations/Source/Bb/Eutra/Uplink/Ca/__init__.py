from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CaCls:
	"""Ca commands group definition. 13 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ca", core, parent)

	@property
	def cell(self):
		"""cell commands group. 12 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .Cell import CellCls
			self._cell = CellCls(self._core, self._cmd_group)
		return self._cell

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:CA:STATe \n
		Snippet: value: bool = driver.source.bb.eutra.uplink.ca.get_state() \n
		Enables UL carrier aggregation. \n
			:return: ulca_glob_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:CA:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, ulca_glob_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:CA:STATe \n
		Snippet: driver.source.bb.eutra.uplink.ca.set_state(ulca_glob_state = False) \n
		Enables UL carrier aggregation. \n
			:param ulca_glob_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(ulca_glob_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:CA:STATe {param}')

	def clone(self) -> 'CaCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CaCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
