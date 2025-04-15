from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CalibrationCls:
	"""Calibration commands group definition. 40 total commands, 11 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("calibration", core, parent)

	@property
	def all(self):
		"""all commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_all'):
			from .All import AllCls
			self._all = AllCls(self._core, self._cmd_group)
		return self._all

	@property
	def bbin(self):
		"""bbin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bbin'):
			from .Bbin import BbinCls
			self._bbin = BbinCls(self._core, self._cmd_group)
		return self._bbin

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def delay(self):
		"""delay commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_delay'):
			from .Delay import DelayCls
			self._delay = DelayCls(self._core, self._cmd_group)
		return self._delay

	@property
	def fmOffset(self):
		"""fmOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fmOffset'):
			from .FmOffset import FmOffsetCls
			self._fmOffset = FmOffsetCls(self._core, self._cmd_group)
		return self._fmOffset

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def iqModulator(self):
		"""iqModulator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqModulator'):
			from .IqModulator import IqModulatorCls
			self._iqModulator = IqModulatorCls(self._core, self._cmd_group)
		return self._iqModulator

	@property
	def level(self):
		"""level commands group. 4 Sub-classes, 4 commands."""
		if not hasattr(self, '_level'):
			from .Level import LevelCls
			self._level = LevelCls(self._core, self._cmd_group)
		return self._level

	@property
	def loscillator(self):
		"""loscillator commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_loscillator'):
			from .Loscillator import LoscillatorCls
			self._loscillator = LoscillatorCls(self._core, self._cmd_group)
		return self._loscillator

	@property
	def roscillator(self):
		"""roscillator commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_roscillator'):
			from .Roscillator import RoscillatorCls
			self._roscillator = RoscillatorCls(self._core, self._cmd_group)
		return self._roscillator

	@property
	def selected(self):
		"""selected commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_selected'):
			from .Selected import SelectedCls
			self._selected = SelectedCls(self._core, self._cmd_group)
		return self._selected

	def get_continue_on_error(self) -> bool:
		"""SCPI: CALibration<HW>:CONTinueonerror \n
		Snippet: value: bool = driver.calibration.get_continue_on_error() \n
		Continues the calibration even though an error was detected. By default adjustments are aborted on error. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('CALibration<HwInstance>:CONTinueonerror?')
		return Conversions.str_to_bool(response)

	def set_continue_on_error(self, state: bool) -> None:
		"""SCPI: CALibration<HW>:CONTinueonerror \n
		Snippet: driver.calibration.set_continue_on_error(state = False) \n
		Continues the calibration even though an error was detected. By default adjustments are aborted on error. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CALibration<HwInstance>:CONTinueonerror {param}')

	def set_debug(self, state: bool) -> None:
		"""SCPI: CALibration<HW>:DEBug \n
		Snippet: driver.calibration.set_debug(state = False) \n
		Activates logging of the internal adjustments. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CALibration<HwInstance>:DEBug {param}')

	def clone(self) -> 'CalibrationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CalibrationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
