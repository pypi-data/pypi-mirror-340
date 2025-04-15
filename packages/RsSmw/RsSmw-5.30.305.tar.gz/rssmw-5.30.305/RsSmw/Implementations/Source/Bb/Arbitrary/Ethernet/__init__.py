from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EthernetCls:
	"""Ethernet commands group definition. 15 total commands, 3 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ethernet", core, parent)

	@property
	def statistics(self):
		"""statistics commands group. 8 Sub-classes, 1 commands."""
		if not hasattr(self, '_statistics'):
			from .Statistics import StatisticsCls
			self._statistics = StatisticsCls(self._core, self._cmd_group)
		return self._statistics

	@property
	def waveform(self):
		"""waveform commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_waveform'):
			from .Waveform import WaveformCls
			self._waveform = WaveformCls(self._core, self._cmd_group)
		return self._waveform

	@property
	def streaming(self):
		"""streaming commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_streaming'):
			from .Streaming import StreamingCls
			self._streaming = StreamingCls(self._core, self._cmd_group)
		return self._streaming

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ArbEthMode:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:ETHernet:MODE \n
		Snippet: value: enums.ArbEthMode = driver.source.bb.arbitrary.ethernet.get_mode() \n
		Sets the Ethernet mode for the waveform data upload via the Ethernet connection. \n
			:return: mode: M10G| M40G M10G 10 Gbit Ethernet mode M40G 40 Gbit Ethernet mode
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:ETHernet:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ArbEthMode)

	def set_mode(self, mode: enums.ArbEthMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:ETHernet:MODE \n
		Snippet: driver.source.bb.arbitrary.ethernet.set_mode(mode = enums.ArbEthMode.M10G) \n
		Sets the Ethernet mode for the waveform data upload via the Ethernet connection. \n
			:param mode: M10G| M40G M10G 10 Gbit Ethernet mode M40G 40 Gbit Ethernet mode
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ArbEthMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:ETHernet:MODE {param}')

	def clone(self) -> 'EthernetCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EthernetCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
