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
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def scode(self):
		"""scode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scode'):
			from .Scode import ScodeCls
			self._scode = ScodeCls(self._core, self._cmd_group)
		return self._scode

	@property
	def tdelay(self):
		"""tdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdelay'):
			from .Tdelay import TdelayCls
			self._tdelay = TdelayCls(self._core, self._cmd_group)
		return self._tdelay

	def get_count(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:ADDitional:COUNt \n
		Snippet: value: int = driver.source.bb.w3Gpp.mstation.additional.get_count() \n
		The command sets the amount of additional user equipment. Up to 128 additional user equipment can be simulated -
		corresponding to a receive signal for a base station with high capacity utilization. The fourth user equipment (UE4)
		serves as a template for all other stations. The only parameters of the additional user equipment to be modified are the
		scrambling code and the power. \n
			:return: count: integer Range: 1 to 128
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ADDitional:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, count: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:ADDitional:COUNt \n
		Snippet: driver.source.bb.w3Gpp.mstation.additional.set_count(count = 1) \n
		The command sets the amount of additional user equipment. Up to 128 additional user equipment can be simulated -
		corresponding to a receive signal for a base station with high capacity utilization. The fourth user equipment (UE4)
		serves as a template for all other stations. The only parameters of the additional user equipment to be modified are the
		scrambling code and the power. \n
			:param count: integer Range: 1 to 128
		"""
		param = Conversions.decimal_value_to_str(count)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ADDitional:COUNt {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:ADDitional:STATe \n
		Snippet: value: bool = driver.source.bb.w3Gpp.mstation.additional.get_state() \n
		Activates additional user equipment. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ADDitional:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:ADDitional:STATe \n
		Snippet: driver.source.bb.w3Gpp.mstation.additional.set_state(state = False) \n
		Activates additional user equipment. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ADDitional:STATe {param}')

	def clone(self) -> 'AdditionalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AdditionalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
