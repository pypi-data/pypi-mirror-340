from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class McoderCls:
	"""Mcoder commands group definition. 5 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mcoder", core, parent)

	@property
	def arbitrary(self):
		"""arbitrary commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_arbitrary'):
			from .Arbitrary import ArbitraryCls
			self._arbitrary = ArbitraryCls(self._core, self._cmd_group)
		return self._arbitrary

	@property
	def dm(self):
		"""dm commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_dm'):
			from .Dm import DmCls
			self._dm = DmCls(self._core, self._cmd_group)
		return self._dm

	def get_value(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:PROGress:MCODer \n
		Snippet: value: int = driver.source.bb.progress.mcoder.get_value() \n
		Queries the status of an initiated process. This process can be, for example, the calculation of a signal in accordance
		to a digital standard, or the calculation of a multicarrier or multi-segment waveform file. \n
			:return: mcoder: integer Indicates the task progress in percent Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PROGress:MCODer?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'McoderCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = McoderCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
