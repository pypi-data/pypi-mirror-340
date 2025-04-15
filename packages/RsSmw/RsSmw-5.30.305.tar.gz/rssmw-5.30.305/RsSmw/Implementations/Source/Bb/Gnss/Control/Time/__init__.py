from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TimeCls:
	"""Time commands group definition. 5 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("time", core, parent)

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Duration import DurationCls
			self._duration = DurationCls(self._core, self._cmd_group)
		return self._duration

	@property
	def repetition(self):
		"""repetition commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_repetition'):
			from .Repetition import RepetitionCls
			self._repetition = RepetitionCls(self._core, self._cmd_group)
		return self._repetition

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:CONTrol:TIME:STATe \n
		Snippet: value: bool = driver.source.bb.gnss.control.time.get_state() \n
		Enables a time-controlled GNSS simulation for a configured period and number of repetitions. \n
			:return: time_control_stat: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:CONTrol:TIME:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, time_control_stat: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:CONTrol:TIME:STATe \n
		Snippet: driver.source.bb.gnss.control.time.set_state(time_control_stat = False) \n
		Enables a time-controlled GNSS simulation for a configured period and number of repetitions. \n
			:param time_control_stat: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(time_control_stat)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:CONTrol:TIME:STATe {param}')

	def clone(self) -> 'TimeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TimeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
