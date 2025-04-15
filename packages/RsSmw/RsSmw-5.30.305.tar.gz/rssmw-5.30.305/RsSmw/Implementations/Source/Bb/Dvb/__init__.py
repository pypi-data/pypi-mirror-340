from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DvbCls:
	"""Dvb commands group definition. 367 total commands, 13 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dvb", core, parent)

	@property
	def clipping(self):
		"""clipping commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clipping'):
			from .Clipping import ClippingCls
			self._clipping = ClippingCls(self._core, self._cmd_group)
		return self._clipping

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Clock import ClockCls
			self._clock = ClockCls(self._core, self._cmd_group)
		return self._clock

	@property
	def dvbh(self):
		"""dvbh commands group. 6 Sub-classes, 4 commands."""
		if not hasattr(self, '_dvbh'):
			from .Dvbh import DvbhCls
			self._dvbh = DvbhCls(self._core, self._cmd_group)
		return self._dvbh

	@property
	def dvbr(self):
		"""dvbr commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_dvbr'):
			from .Dvbr import DvbrCls
			self._dvbr = DvbrCls(self._core, self._cmd_group)
		return self._dvbr

	@property
	def dvbs(self):
		"""dvbs commands group. 17 Sub-classes, 13 commands."""
		if not hasattr(self, '_dvbs'):
			from .Dvbs import DvbsCls
			self._dvbs = DvbsCls(self._core, self._cmd_group)
		return self._dvbs

	@property
	def dvbt(self):
		"""dvbt commands group. 6 Sub-classes, 4 commands."""
		if not hasattr(self, '_dvbt'):
			from .Dvbt import DvbtCls
			self._dvbt = DvbtCls(self._core, self._cmd_group)
		return self._dvbt

	@property
	def dvbx(self):
		"""dvbx commands group. 18 Sub-classes, 16 commands."""
		if not hasattr(self, '_dvbx'):
			from .Dvbx import DvbxCls
			self._dvbx = DvbxCls(self._core, self._cmd_group)
		return self._dvbx

	@property
	def filterPy(self):
		"""filterPy commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPyCls
			self._filterPy = FilterPyCls(self._core, self._cmd_group)
		return self._filterPy

	@property
	def notch(self):
		"""notch commands group. 4 Sub-classes, 3 commands."""
		if not hasattr(self, '_notch'):
			from .Notch import NotchCls
			self._notch = NotchCls(self._core, self._cmd_group)
		return self._notch

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .SymbolRate import SymbolRateCls
			self._symbolRate = SymbolRateCls(self._core, self._cmd_group)
		return self._symbolRate

	@property
	def trigger(self):
		"""trigger commands group. 6 Sub-classes, 5 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	@property
	def waveform(self):
		"""waveform commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_waveform'):
			from .Waveform import WaveformCls
			self._waveform = WaveformCls(self._core, self._cmd_group)
		return self._waveform

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:PRESet \n
		Snippet: driver.source.bb.dvb.preset() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:DVB:STATe. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:PRESet \n
		Snippet: driver.source.bb.dvb.preset_with_opc() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:DVB:STATe. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:DVB:PRESet', opc_timeout_ms)

	# noinspection PyTypeChecker
	def get_standard(self) -> enums.DvbStandard:
		"""SCPI: [SOURce<HW>]:BB:DVB:STANdard \n
		Snippet: value: enums.DvbStandard = driver.source.bb.dvb.get_standard() \n
		Selects the DVB standard to be used. \n
			:return: standard: DVBH| DVBT | DVBS| DVBX | DVBR
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:STANdard?')
		return Conversions.str_to_scalar_enum(response, enums.DvbStandard)

	def set_standard(self, standard: enums.DvbStandard) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:STANdard \n
		Snippet: driver.source.bb.dvb.set_standard(standard = enums.DvbStandard.DVBH) \n
		Selects the DVB standard to be used. \n
			:param standard: DVBH| DVBT | DVBS| DVBX | DVBR
		"""
		param = Conversions.enum_scalar_to_str(standard, enums.DvbStandard)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:STANdard {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:DVB:STATe \n
		Snippet: value: bool = driver.source.bb.dvb.get_state() \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:STATe \n
		Snippet: driver.source.bb.dvb.set_state(state = False) \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:STATe {param}')

	def clone(self) -> 'DvbCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DvbCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
