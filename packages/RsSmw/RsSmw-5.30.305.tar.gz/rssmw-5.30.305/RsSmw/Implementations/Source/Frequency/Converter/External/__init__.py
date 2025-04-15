from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExternalCls:
	"""External commands group definition. 16 total commands, 7 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("external", core, parent)

	@property
	def adjust(self):
		"""adjust commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_adjust'):
			from .Adjust import AdjustCls
			self._adjust = AdjustCls(self._core, self._cmd_group)
		return self._adjust

	@property
	def connection(self):
		"""connection commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_connection'):
			from .Connection import ConnectionCls
			self._connection = ConnectionCls(self._core, self._cmd_group)
		return self._connection

	@property
	def detector(self):
		"""detector commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_detector'):
			from .Detector import DetectorCls
			self._detector = DetectorCls(self._core, self._cmd_group)
		return self._detector

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def overrange(self):
		"""overrange commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_overrange'):
			from .Overrange import OverrangeCls
			self._overrange = OverrangeCls(self._core, self._cmd_group)
		return self._overrange

	@property
	def simulation(self):
		"""simulation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_simulation'):
			from .Simulation import SimulationCls
			self._simulation = SimulationCls(self._core, self._cmd_group)
		return self._simulation

	@property
	def test(self):
		"""test commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_test'):
			from .Test import TestCls
			self._test = TestCls(self._core, self._cmd_group)
		return self._test

	def get_snumber(self) -> str:
		"""SCPI: [SOURce<HW>]:FREQuency:CONVerter:EXTernal:SNUMber \n
		Snippet: value: str = driver.source.frequency.converter.external.get_snumber() \n
		No command help available \n
			:return: ser_number: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:CONVerter:EXTernal:SNUMber?')
		return trim_str_response(response)

	def clone(self) -> 'ExternalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ExternalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
