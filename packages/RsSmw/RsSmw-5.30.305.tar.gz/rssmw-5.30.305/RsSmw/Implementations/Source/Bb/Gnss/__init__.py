from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GnssCls:
	"""Gnss commands group definition. 2497 total commands, 29 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gnss", core, parent)

	@property
	def adGeneration(self):
		"""adGeneration commands group. 9 Sub-classes, 1 commands."""
		if not hasattr(self, '_adGeneration'):
			from .AdGeneration import AdGenerationCls
			self._adGeneration = AdGenerationCls(self._core, self._cmd_group)
		return self._adGeneration

	@property
	def apattern(self):
		"""apattern commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_apattern'):
			from .Apattern import ApatternCls
			self._apattern = ApatternCls(self._core, self._cmd_group)
		return self._apattern

	@property
	def atmospheric(self):
		"""atmospheric commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_atmospheric'):
			from .Atmospheric import AtmosphericCls
			self._atmospheric = AtmosphericCls(self._core, self._cmd_group)
		return self._atmospheric

	@property
	def awgn(self):
		"""awgn commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_awgn'):
			from .Awgn import AwgnCls
			self._awgn = AwgnCls(self._core, self._cmd_group)
		return self._awgn

	@property
	def body(self):
		"""body commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_body'):
			from .Body import BodyCls
			self._body = BodyCls(self._core, self._cmd_group)
		return self._body

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Clock import ClockCls
			self._clock = ClockCls(self._core, self._cmd_group)
		return self._clock

	@property
	def control(self):
		"""control commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_control'):
			from .Control import ControlCls
			self._control = ControlCls(self._core, self._cmd_group)
		return self._control

	@property
	def galileo(self):
		"""galileo commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_galileo'):
			from .Galileo import GalileoCls
			self._galileo = GalileoCls(self._core, self._cmd_group)
		return self._galileo

	@property
	def l1Band(self):
		"""l1Band commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_l1Band'):
			from .L1Band import L1BandCls
			self._l1Band = L1BandCls(self._core, self._cmd_group)
		return self._l1Band

	@property
	def l2Band(self):
		"""l2Band commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_l2Band'):
			from .L2Band import L2BandCls
			self._l2Band = L2BandCls(self._core, self._cmd_group)
		return self._l2Band

	@property
	def l5Band(self):
		"""l5Band commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_l5Band'):
			from .L5Band import L5BandCls
			self._l5Band = L5BandCls(self._core, self._cmd_group)
		return self._l5Band

	@property
	def logging(self):
		"""logging commands group. 4 Sub-classes, 1 commands."""
		if not hasattr(self, '_logging'):
			from .Logging import LoggingCls
			self._logging = LoggingCls(self._core, self._cmd_group)
		return self._logging

	@property
	def monitor(self):
		"""monitor commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_monitor'):
			from .Monitor import MonitorCls
			self._monitor = MonitorCls(self._core, self._cmd_group)
		return self._monitor

	@property
	def obscuration(self):
		"""obscuration commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_obscuration'):
			from .Obscuration import ObscurationCls
			self._obscuration = ObscurationCls(self._core, self._cmd_group)
		return self._obscuration

	@property
	def ostreams(self):
		"""ostreams commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_ostreams'):
			from .Ostreams import OstreamsCls
			self._ostreams = OstreamsCls(self._core, self._cmd_group)
		return self._ostreams

	@property
	def perrors(self):
		"""perrors commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_perrors'):
			from .Perrors import PerrorsCls
			self._perrors = PerrorsCls(self._core, self._cmd_group)
		return self._perrors

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def receiver(self):
		"""receiver commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_receiver'):
			from .Receiver import ReceiverCls
			self._receiver = ReceiverCls(self._core, self._cmd_group)
		return self._receiver

	@property
	def rt(self):
		"""rt commands group. 9 Sub-classes, 4 commands."""
		if not hasattr(self, '_rt'):
			from .Rt import RtCls
			self._rt = RtCls(self._core, self._cmd_group)
		return self._rt

	@property
	def rtk(self):
		"""rtk commands group. 2 Sub-classes, 5 commands."""
		if not hasattr(self, '_rtk'):
			from .Rtk import RtkCls
			self._rtk = RtkCls(self._core, self._cmd_group)
		return self._rtk

	@property
	def setting(self):
		"""setting commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	@property
	def simulation(self):
		"""simulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_simulation'):
			from .Simulation import SimulationCls
			self._simulation = SimulationCls(self._core, self._cmd_group)
		return self._simulation

	@property
	def stream(self):
		"""stream commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_stream'):
			from .Stream import StreamCls
			self._stream = StreamCls(self._core, self._cmd_group)
		return self._stream

	@property
	def sv(self):
		"""sv commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_sv'):
			from .Sv import SvCls
			self._sv = SvCls(self._core, self._cmd_group)
		return self._sv

	@property
	def svid(self):
		"""svid commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_svid'):
			from .Svid import SvidCls
			self._svid = SvidCls(self._core, self._cmd_group)
		return self._svid

	@property
	def system(self):
		"""system commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_system'):
			from .System import SystemCls
			self._system = SystemCls(self._core, self._cmd_group)
		return self._system

	@property
	def time(self):
		"""time commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_time'):
			from .Time import TimeCls
			self._time = TimeCls(self._core, self._cmd_group)
		return self._time

	@property
	def trigger(self):
		"""trigger commands group. 6 Sub-classes, 4 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	@property
	def vehicle(self):
		"""vehicle commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_vehicle'):
			from .Vehicle import VehicleCls
			self._vehicle = VehicleCls(self._core, self._cmd_group)
		return self._vehicle

	def get_cfrequency(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:CFRequency \n
		Snippet: value: int = driver.source.bb.gnss.get_cfrequency() \n
		Queries the central RF frequency. The response is a mean value depending on enabled RF bands and GNSS systems. \n
			:return: central_rf_freq: integer Range: 1E9 to 2E9, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:CFRequency?')
		return Conversions.str_to_int(response)

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:PRESet \n
		Snippet: driver.source.bb.gnss.preset() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:GNSS:STATe. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:PRESet \n
		Snippet: driver.source.bb.gnss.preset_with_opc() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:GNSS:STATe. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:PRESet', opc_timeout_ms)

	def get_scenario(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SCENario \n
		Snippet: value: str = driver.source.bb.gnss.get_scenario() \n
		Queries the current scenario. \n
			:return: scenario: string NONE Indicates the preset configuration or a user-defined configuration. Scenario name Returns the scenario name of a predefined scenario, e.g. '3GPP TS 37.571-2: S7 Signaling ST1'. See 'Predefined GNSS scenarios'. Filename Returns the filename of a saved, user-defined scenario. The scenario file has the extension *.gnss.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SCENario?')
		return trim_str_response(response)

	def get_ss_values(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SSValues \n
		Snippet: value: bool = driver.source.bb.gnss.get_ss_values() \n
		Defines if the navigation message parameters are set as scaled or unscaled values and thus which subset of remote-control
		commands is used. \n
			:return: show_scaled_value: 1| ON| 0| OFF 0 Used are unscaled values The SOURcehw:BB:GNSS:...:UNSCaled commands apply. 1 Used are scaled values Commands without the mnemonic UNSCaled apply.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SSValues?')
		return Conversions.str_to_bool(response)

	def set_ss_values(self, show_scaled_value: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SSValues \n
		Snippet: driver.source.bb.gnss.set_ss_values(show_scaled_value = False) \n
		Defines if the navigation message parameters are set as scaled or unscaled values and thus which subset of remote-control
		commands is used. \n
			:param show_scaled_value: 1| ON| 0| OFF 0 Used are unscaled values The SOURcehw:BB:GNSS:...:UNSCaled commands apply. 1 Used are scaled values Commands without the mnemonic UNSCaled apply.
		"""
		param = Conversions.bool_to_str(show_scaled_value)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SSValues {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:STATe \n
		Snippet: value: bool = driver.source.bb.gnss.get_state() \n
		Enables/disables the GNSS signal simulation. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:STATe \n
		Snippet: driver.source.bb.gnss.set_state(state = False) \n
		Enables/disables the GNSS signal simulation. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:STATe {param}')

	# noinspection PyTypeChecker
	def get_tmode(self) -> enums.SimMode2:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TMODe \n
		Snippet: value: enums.SimMode2 = driver.source.bb.gnss.get_tmode() \n
		Sets the test mode. \n
			:return: smode: NAVigation| TRACking| MSI| AMSI NAVigation Navigation mode The generated signal contains satellite signals to simulate a particular location of a GNSS receiver. This signal implies a realistic navigation scenario. The DUT can achieve position fix, since the satellite constellation comprises of at least three satellites. The signal is suitable for signal acquisition and TTFF tests. TRACking Tracking mode The generated signal contains no positioning data. You do not need to configure the GNSS receiver. Navigation and acquiring of position fix is not possible. The signal is sufficient to test the ability of the DUT to find the channel and to decode the signal. It is also sufficient for receiver sensitivity testing. Use this mode to simulate high signal dynamics. For example, simulate spinning vehicles and precision code (P code) signals. MSI Matched-spectrum interferer mode The generated signal is a tracking mode signal that contains continuous wave (CW) interference signals for all space vehicles of a given satellite constellation. These signals have no navigation message data. AMSI Advanced matched-spectrum interferer mode The generated signal is a navigation mode signal that contains continuous wave (CW) interference signals for all space vehicles of a given satellite constellation. These signals have no navigation message data.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TMODe?')
		return Conversions.str_to_scalar_enum(response, enums.SimMode2)

	def set_tmode(self, smode: enums.SimMode2) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TMODe \n
		Snippet: driver.source.bb.gnss.set_tmode(smode = enums.SimMode2.AMSI) \n
		Sets the test mode. \n
			:param smode: NAVigation| TRACking| MSI| AMSI NAVigation Navigation mode The generated signal contains satellite signals to simulate a particular location of a GNSS receiver. This signal implies a realistic navigation scenario. The DUT can achieve position fix, since the satellite constellation comprises of at least three satellites. The signal is suitable for signal acquisition and TTFF tests. TRACking Tracking mode The generated signal contains no positioning data. You do not need to configure the GNSS receiver. Navigation and acquiring of position fix is not possible. The signal is sufficient to test the ability of the DUT to find the channel and to decode the signal. It is also sufficient for receiver sensitivity testing. Use this mode to simulate high signal dynamics. For example, simulate spinning vehicles and precision code (P code) signals. MSI Matched-spectrum interferer mode The generated signal is a tracking mode signal that contains continuous wave (CW) interference signals for all space vehicles of a given satellite constellation. These signals have no navigation message data. AMSI Advanced matched-spectrum interferer mode The generated signal is a navigation mode signal that contains continuous wave (CW) interference signals for all space vehicles of a given satellite constellation. These signals have no navigation message data.
		"""
		param = Conversions.enum_scalar_to_str(smode, enums.SimMode2)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TMODe {param}')

	def clone(self) -> 'GnssCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GnssCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
