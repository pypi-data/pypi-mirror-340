from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AdditionalCls:
	"""Additional commands group definition. 5 total commands, 3 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("additional", core, parent)

	@property
	def lcMask(self):
		"""lcMask commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lcMask'):
			from .LcMask import LcMaskCls
			self._lcMask = LcMaskCls(self._core, self._cmd_group)
		return self._lcMask

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def tdelay(self):
		"""tdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdelay'):
			from .Tdelay import TdelayCls
			self._tdelay = TdelayCls(self._core, self._cmd_group)
		return self._tdelay

	def get_count(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:C2K:MSTation:ADDitional:COUNt \n
		Snippet: value: int = driver.source.bb.c2K.mstation.additional.get_count() \n
		Sets the number of additional mobile stations. \n
			:return: count: integer Range: 1 to 64
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:MSTation:ADDitional:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, count: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:C2K:MSTation:ADDitional:COUNt \n
		Snippet: driver.source.bb.c2K.mstation.additional.set_count(count = 1) \n
		Sets the number of additional mobile stations. \n
			:param count: integer Range: 1 to 64
		"""
		param = Conversions.decimal_value_to_str(count)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:MSTation:ADDitional:COUNt {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:C2K:MSTation:ADDitional:STATe \n
		Snippet: value: bool = driver.source.bb.c2K.mstation.additional.get_state() \n
		The command activates additional mobile stations. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:MSTation:ADDitional:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:C2K:MSTation:ADDitional:STATe \n
		Snippet: driver.source.bb.c2K.mstation.additional.set_state(state = False) \n
		The command activates additional mobile stations. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:MSTation:ADDitional:STATe {param}')

	def clone(self) -> 'AdditionalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AdditionalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
