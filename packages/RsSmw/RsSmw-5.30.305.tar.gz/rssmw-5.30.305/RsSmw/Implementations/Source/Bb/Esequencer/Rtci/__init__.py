from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RtciCls:
	"""Rtci commands group definition. 26 total commands, 3 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rtci", core, parent)

	@property
	def wave(self):
		"""wave commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_wave'):
			from .Wave import WaveCls
			self._wave = WaveCls(self._core, self._cmd_group)
		return self._wave

	@property
	def wlist(self):
		"""wlist commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_wlist'):
			from .Wlist import WlistCls
			self._wlist = WlistCls(self._core, self._cmd_group)
		return self._wlist

	@property
	def sequencer(self):
		"""sequencer commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_sequencer'):
			from .Sequencer import SequencerCls
			self._sequencer = SequencerCls(self._core, self._cmd_group)
		return self._sequencer

	# noinspection PyTypeChecker
	def get_pdw_format(self) -> enums.ExtSeqPdwVariant:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:RTCI:PDWFormat \n
		Snippet: value: enums.ExtSeqPdwVariant = driver.source.bb.esequencer.rtci.get_pdw_format() \n
		Selects the PDW format. \n
			:return: format_py: BASic| EXPert
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ESEQuencer:RTCI:PDWFormat?')
		return Conversions.str_to_scalar_enum(response, enums.ExtSeqPdwVariant)

	def set_pdw_format(self, format_py: enums.ExtSeqPdwVariant) -> None:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:RTCI:PDWFormat \n
		Snippet: driver.source.bb.esequencer.rtci.set_pdw_format(format_py = enums.ExtSeqPdwVariant.BASic) \n
		Selects the PDW format. \n
			:param format_py: BASic| EXPert
		"""
		param = Conversions.enum_scalar_to_str(format_py, enums.ExtSeqPdwVariant)
		self._core.io.write(f'SOURce<HwInstance>:BB:ESEQuencer:RTCI:PDWFormat {param}')

	# noinspection PyTypeChecker
	def get_pdw_rate(self) -> enums.ExtSeqPdwRateMode:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:RTCI:PDWRate \n
		Snippet: value: enums.ExtSeqPdwRateMode = driver.source.bb.esequencer.rtci.get_pdw_rate() \n
		Sets the mode for the PDW streaming rate. \n
			:return: rate_mode: STANdard| HSPeed STANdard For fast HIL response time, less than 100 us. Supports PDW streaming rates up to 1.5 MPDW/s. HSPeed For high PDW streaming rates up to 2 MPDW/s.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ESEQuencer:RTCI:PDWRate?')
		return Conversions.str_to_scalar_enum(response, enums.ExtSeqPdwRateMode)

	def set_pdw_rate(self, rate_mode: enums.ExtSeqPdwRateMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:RTCI:PDWRate \n
		Snippet: driver.source.bb.esequencer.rtci.set_pdw_rate(rate_mode = enums.ExtSeqPdwRateMode.HSPeed) \n
		Sets the mode for the PDW streaming rate. \n
			:param rate_mode: STANdard| HSPeed STANdard For fast HIL response time, less than 100 us. Supports PDW streaming rates up to 1.5 MPDW/s. HSPeed For high PDW streaming rates up to 2 MPDW/s.
		"""
		param = Conversions.enum_scalar_to_str(rate_mode, enums.ExtSeqPdwRateMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:ESEQuencer:RTCI:PDWRate {param}')

	def clone(self) -> 'RtciCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RtciCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
