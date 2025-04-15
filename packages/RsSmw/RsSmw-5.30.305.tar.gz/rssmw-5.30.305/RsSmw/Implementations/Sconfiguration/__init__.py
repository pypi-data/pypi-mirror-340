from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SconfigurationCls:
	"""Sconfiguration commands group definition. 235 total commands, 11 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sconfiguration", core, parent)

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Apply import ApplyCls
			self._apply = ApplyCls(self._core, self._cmd_group)
		return self._apply

	@property
	def baseband(self):
		"""baseband commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_baseband'):
			from .Baseband import BasebandCls
			self._baseband = BasebandCls(self._core, self._cmd_group)
		return self._baseband

	@property
	def bextension(self):
		"""bextension commands group. 5 Sub-classes, 2 commands."""
		if not hasattr(self, '_bextension'):
			from .Bextension import BextensionCls
			self._bextension = BextensionCls(self._core, self._cmd_group)
		return self._bextension

	@property
	def diq(self):
		"""diq commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_diq'):
			from .Diq import DiqCls
			self._diq = DiqCls(self._core, self._cmd_group)
		return self._diq

	@property
	def duplicate(self):
		"""duplicate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duplicate'):
			from .Duplicate import DuplicateCls
			self._duplicate = DuplicateCls(self._core, self._cmd_group)
		return self._duplicate

	@property
	def external(self):
		"""external commands group. 8 Sub-classes, 3 commands."""
		if not hasattr(self, '_external'):
			from .External import ExternalCls
			self._external = ExternalCls(self._core, self._cmd_group)
		return self._external

	@property
	def gnss(self):
		"""gnss commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_gnss'):
			from .Gnss import GnssCls
			self._gnss = GnssCls(self._core, self._cmd_group)
		return self._gnss

	@property
	def multiInstrument(self):
		"""multiInstrument commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_multiInstrument'):
			from .MultiInstrument import MultiInstrumentCls
			self._multiInstrument = MultiInstrumentCls(self._core, self._cmd_group)
		return self._multiInstrument

	@property
	def output(self):
		"""output commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	@property
	def rfAlignment(self):
		"""rfAlignment commands group. 4 Sub-classes, 1 commands."""
		if not hasattr(self, '_rfAlignment'):
			from .RfAlignment import RfAlignmentCls
			self._rfAlignment = RfAlignmentCls(self._core, self._cmd_group)
		return self._rfAlignment

	@property
	def siso(self):
		"""siso commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_siso'):
			from .Siso import SisoCls
			self._siso = SisoCls(self._core, self._cmd_group)
		return self._siso

	# noinspection PyTypeChecker
	def get_bb_bw(self) -> enums.SystConfBbBandwidth:
		"""SCPI: SCONfiguration:BBBW \n
		Snippet: value: enums.SystConfBbBandwidth = driver.sconfiguration.get_bb_bw() \n
		Sets the bandwidth of the baseband signal at the inputs of the fading simulator. The available values depend on the
		selected MIMO configuration.
			INTRO_CMD_HELP: For example: \n
			- In MIMO configurations with fewer than 8 channels, the max. baseband bandwidth is 400 MHz.
			- In MIMO configurations with fewer than 4 channels, the max. baseband bandwidth is 800 MHz. \n
			:return: bandwidth: BB040| BB050| BB080| BB100| BB160| BB200| BB800| BB400| BB500| BB1G| BB2G| BB120| BBOUTDEF| BB240 BB040|BB050 ... Bandwidth in MHz, e.g. 40 MHz. BB1G|BB2G 1 GHz, 2 GHz bandwidth. Available in SISO configurations. BBOUTDEF Bandwidth determined by the signal at the HS DIG I/Q.
		"""
		response = self._core.io.query_str('SCONfiguration:BBBW?')
		return Conversions.str_to_scalar_enum(response, enums.SystConfBbBandwidth)

	def set_bb_bw(self, bandwidth: enums.SystConfBbBandwidth) -> None:
		"""SCPI: SCONfiguration:BBBW \n
		Snippet: driver.sconfiguration.set_bb_bw(bandwidth = enums.SystConfBbBandwidth.BB040) \n
		Sets the bandwidth of the baseband signal at the inputs of the fading simulator. The available values depend on the
		selected MIMO configuration.
			INTRO_CMD_HELP: For example: \n
			- In MIMO configurations with fewer than 8 channels, the max. baseband bandwidth is 400 MHz.
			- In MIMO configurations with fewer than 4 channels, the max. baseband bandwidth is 800 MHz. \n
			:param bandwidth: BB040| BB050| BB080| BB100| BB160| BB200| BB800| BB400| BB500| BB1G| BB2G| BB120| BBOUTDEF| BB240 BB040|BB050 ... Bandwidth in MHz, e.g. 40 MHz. BB1G|BB2G 1 GHz, 2 GHz bandwidth. Available in SISO configurations. BBOUTDEF Bandwidth determined by the signal at the HS DIG I/Q.
		"""
		param = Conversions.enum_scalar_to_str(bandwidth, enums.SystConfBbBandwidth)
		self._core.io.write(f'SCONfiguration:BBBW {param}')

	# noinspection PyTypeChecker
	def get_cabw(self) -> enums.SystConfBbBandwidth:
		"""SCPI: SCONfiguration:CABW \n
		Snippet: value: enums.SystConfBbBandwidth = driver.sconfiguration.get_cabw() \n
		Queries the resulting channel aggregation bandwidth, i.e. the signal bandwidth at the outputs of the stream mapper. The
		value is calculated automatically and depends on the selected configuration, the installed options and the selected
		baseband bandwidth (method RsSmw.Sconfiguration.bbBw) . \n
			:return: bandwidth: BB800| BB200
		"""
		response = self._core.io.query_str('SCONfiguration:CABW?')
		return Conversions.str_to_scalar_enum(response, enums.SystConfBbBandwidth)

	# noinspection PyTypeChecker
	def get_fading(self) -> enums.SystConfFadConf:
		"""SCPI: SCONfiguration:FADing \n
		Snippet: value: enums.SystConfFadConf = driver.sconfiguration.get_fading() \n
		Defines the signal routing for standard and advanced system configuration modes. The availability of specific
		configurations of these modes depends on installed options. For more information, refer to the specifications document.
			Table Header: method RsSmw.Sconfiguration.mode / <FadConfig> \n
			- STANdard / FAAFBNone | FANFBB | FAAFBB | FAAFBA | FABFBB | FAABFBN | FANFBAB | FAABFBAB
			- ADVanced / MIMO1X2 | MIMO2X2 | MIMO2X3 | MIMO2X4 | MIMO3X2 | MIMO3X3 | MIMO3X4 | MIMO4X2 | MIMO4X3 | MIMO4X4 | MIMO1X8 | MIMO8X1 | MIMO2X8 | MIMO8X2 | MIMO2X1 | MIMO2X1X2 | MIMO2X2X1 | MIMO2X1X3 | MIMO2X1X4 | MIMO2X2X2 | MIMO1X3 | MIMO3X1 | MIMO1X4 | MIMO4X1 | MIMO3X1X2 | MIMO3X2X1 | MIMO4X1X2 | MIMO3X2X2 | MIMO4X2X2 | MIMO4X2X1 | SISO2X1X1 | SISO3X1X1 | SISO4X1X1 | SISO5X1X1 | SISO6X1X1 | SISO7X1X1 | SISO8X1X1 | MIMO2X2X4 | MIMO2X4X2 | MIMO2X2X3 | MIMO2X3X1 | MIMO2X3X2 | MIMO2X4X1 MIMO4X8 | MIMO8X4 | MIMO2X4X4 | MIMO2X3X3| MIMO2X3X4 | MIMO2X4X3 MIMO8X8 \n
			:return: fad_config: FAAFBNone| FANFBB| FAAFBB| SISO2X1X1| FAAFBA| FABFBB| FAABFBN| FANFBAB| FAABFBAB| MIMO1X2| MIMO2X2| MIMO2X3| MIMO2X4| MIMO3X2| MIMO3X3| MIMO3X4| MIMO4X2| MIMO4X3| MIMO4X4| MIMO1X8| MIMO8X1| MIMO2X8| MIMO8X2| MIMO2X1| MIMO2X1X2| MIMO2X2X1| MIMO2X2X2| MIMO1X3| MIMO3X1| MIMO1X4| MIMO4X1| MIMO3X1X2| MIMO3X2X1| MIMO4X1X2| MIMO3X2X2| MIMO4X2X2| MIMO4X2X1| SISO3X1X1| SISO4X1X1| SISO5X1X1| SISO6X1X1| SISO7X1X1| SISO8X1X1| MIMO2X2X4| MIMO2X4X2| MIMO4X8| MIMO8X4| MIMO2X1X3| MIMO2X1X4| MIMO2X2X3| MIMO2X3X1| MIMO2X3X2| MIMO2X4X1| MIMO2X4X4| MIMO2X3X3| MIMO2X3X4| MIMO2X4X3| MIMO8X8
		"""
		response = self._core.io.query_str('SCONfiguration:FADing?')
		return Conversions.str_to_scalar_enum(response, enums.SystConfFadConf)

	def set_fading(self, fad_config: enums.SystConfFadConf) -> None:
		"""SCPI: SCONfiguration:FADing \n
		Snippet: driver.sconfiguration.set_fading(fad_config = enums.SystConfFadConf.FAABFBAB) \n
		Defines the signal routing for standard and advanced system configuration modes. The availability of specific
		configurations of these modes depends on installed options. For more information, refer to the specifications document.
			Table Header: method RsSmw.Sconfiguration.mode / <FadConfig> \n
			- STANdard / FAAFBNone | FANFBB | FAAFBB | FAAFBA | FABFBB | FAABFBN | FANFBAB | FAABFBAB
			- ADVanced / MIMO1X2 | MIMO2X2 | MIMO2X3 | MIMO2X4 | MIMO3X2 | MIMO3X3 | MIMO3X4 | MIMO4X2 | MIMO4X3 | MIMO4X4 | MIMO1X8 | MIMO8X1 | MIMO2X8 | MIMO8X2 | MIMO2X1 | MIMO2X1X2 | MIMO2X2X1 | MIMO2X1X3 | MIMO2X1X4 | MIMO2X2X2 | MIMO1X3 | MIMO3X1 | MIMO1X4 | MIMO4X1 | MIMO3X1X2 | MIMO3X2X1 | MIMO4X1X2 | MIMO3X2X2 | MIMO4X2X2 | MIMO4X2X1 | SISO2X1X1 | SISO3X1X1 | SISO4X1X1 | SISO5X1X1 | SISO6X1X1 | SISO7X1X1 | SISO8X1X1 | MIMO2X2X4 | MIMO2X4X2 | MIMO2X2X3 | MIMO2X3X1 | MIMO2X3X2 | MIMO2X4X1 MIMO4X8 | MIMO8X4 | MIMO2X4X4 | MIMO2X3X3| MIMO2X3X4 | MIMO2X4X3 MIMO8X8 \n
			:param fad_config: FAAFBNone| FANFBB| FAAFBB| SISO2X1X1| FAAFBA| FABFBB| FAABFBN| FANFBAB| FAABFBAB| MIMO1X2| MIMO2X2| MIMO2X3| MIMO2X4| MIMO3X2| MIMO3X3| MIMO3X4| MIMO4X2| MIMO4X3| MIMO4X4| MIMO1X8| MIMO8X1| MIMO2X8| MIMO8X2| MIMO2X1| MIMO2X1X2| MIMO2X2X1| MIMO2X2X2| MIMO1X3| MIMO3X1| MIMO1X4| MIMO4X1| MIMO3X1X2| MIMO3X2X1| MIMO4X1X2| MIMO3X2X2| MIMO4X2X2| MIMO4X2X1| SISO3X1X1| SISO4X1X1| SISO5X1X1| SISO6X1X1| SISO7X1X1| SISO8X1X1| MIMO2X2X4| MIMO2X4X2| MIMO4X8| MIMO8X4| MIMO2X1X3| MIMO2X1X4| MIMO2X2X3| MIMO2X3X1| MIMO2X3X2| MIMO2X4X1| MIMO2X4X4| MIMO2X3X3| MIMO2X3X4| MIMO2X4X3| MIMO8X8
		"""
		param = Conversions.enum_scalar_to_str(fad_config, enums.SystConfFadConf)
		self._core.io.write(f'SCONfiguration:FADing {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.SystConfMode:
		"""SCPI: SCONfiguration:MODE \n
		Snippet: value: enums.SystConfMode = driver.sconfiguration.get_mode() \n
		Switches between the operating modes. \n
			:return: mode: ADVanced| STANdard| REGenerator | GNSS | ESEQuencer | BWEXtension ADVanced|STANdard Switches between the and . REGenerator Enables the R&S SMW200A to work as a radar echo generator. The fading simulator is disabled. See 'Welcome to the Option'. GNSS Enables the R&S SMW200A to work in GNSS advanced mode. The fading simulator is disabled. See 'Welcome to the GNSS Satellite Navigation Options'. ESEQuencer Enables the R&S SMW200A to work in an advanced extended sequencer mode. The fading simulator, the AWGN, the BB input and all baseband digital standards are disabled. See 'Welcome to the Extended Sequencer'. BEXTension Enables the R&S SMW200A to generate RF signals with extended bandwidth. These signals typically have bandwidths above 2.4 GHz. See 'Welcome to the option'.
		"""
		response = self._core.io.query_str('SCONfiguration:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.SystConfMode)

	def set_mode(self, mode: enums.SystConfMode) -> None:
		"""SCPI: SCONfiguration:MODE \n
		Snippet: driver.sconfiguration.set_mode(mode = enums.SystConfMode.ADVanced) \n
		Switches between the operating modes. \n
			:param mode: ADVanced| STANdard| REGenerator | GNSS | ESEQuencer | BWEXtension ADVanced|STANdard Switches between the and . REGenerator Enables the R&S SMW200A to work as a radar echo generator. The fading simulator is disabled. See 'Welcome to the Option'. GNSS Enables the R&S SMW200A to work in GNSS advanced mode. The fading simulator is disabled. See 'Welcome to the GNSS Satellite Navigation Options'. ESEQuencer Enables the R&S SMW200A to work in an advanced extended sequencer mode. The fading simulator, the AWGN, the BB input and all baseband digital standards are disabled. See 'Welcome to the Extended Sequencer'. BEXTension Enables the R&S SMW200A to generate RF signals with extended bandwidth. These signals typically have bandwidths above 2.4 GHz. See 'Welcome to the option'.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.SystConfMode)
		self._core.io.write(f'SCONfiguration:MODE {param}')

	def preset(self) -> None:
		"""SCPI: SCONfiguration:PRESet \n
		Snippet: driver.sconfiguration.preset() \n
		Presets the signal routing in the baseband section and the fading configuration to the default state. \n
		"""
		self._core.io.write(f'SCONfiguration:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SCONfiguration:PRESet \n
		Snippet: driver.sconfiguration.preset_with_opc() \n
		Presets the signal routing in the baseband section and the fading configuration to the default state. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SCONfiguration:PRESet', opc_timeout_ms)

	def clone(self) -> 'SconfigurationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SconfigurationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
