from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PowerCls:
	"""Power commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("power", core, parent)

	@property
	def adjust(self):
		"""adjust commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adjust'):
			from .Adjust import AdjustCls
			self._adjust = AdjustCls(self._core, self._cmd_group)
		return self._adjust

	def get_total(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:C2K:POWer:[TOTal] \n
		Snippet: value: float = driver.source.bb.c2K.power.get_total() \n
		The command queries the total power of the active channels. After 'Power Adjust', this power corresponds to 0 dB. \n
			:return: total: float Range: -80 dB to 30 dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:POWer:TOTal?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'PowerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PowerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
