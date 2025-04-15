from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScontrolCls:
	"""Scontrol commands group definition. 5 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scontrol", core, parent)

	@property
	def fragment(self):
		"""fragment commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_fragment'):
			from .Fragment import FragmentCls
			self._fragment = FragmentCls(self._core, self._cmd_group)
		return self._fragment

	@property
	def sequence(self):
		"""sequence commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sequence'):
			from .Sequence import SequenceCls
			self._sequence = SequenceCls(self._core, self._cmd_group)
		return self._sequence

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:SCONtrol:STATe \n
		Snippet: value: bool = driver.source.bb.wlad.pconfig.mac.scontrol.get_state() \n
		Activates/deactivates the sequence control. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:SCONtrol:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:SCONtrol:STATe \n
		Snippet: driver.source.bb.wlad.pconfig.mac.scontrol.set_state(state = False) \n
		Activates/deactivates the sequence control. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:SCONtrol:STATe {param}')

	def clone(self) -> 'ScontrolCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ScontrolCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
