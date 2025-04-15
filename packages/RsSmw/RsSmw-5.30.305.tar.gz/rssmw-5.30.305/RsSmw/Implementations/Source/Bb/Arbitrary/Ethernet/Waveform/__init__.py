from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class WaveformCls:
	"""Waveform commands group definition. 4 total commands, 1 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("waveform", core, parent)

	@property
	def tag(self):
		"""tag commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tag'):
			from .Tag import TagCls
			self._tag = TagCls(self._core, self._cmd_group)
		return self._tag

	def get_counter(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:ETHernet:WAVeform:COUNter \n
		Snippet: value: int = driver.source.bb.arbitrary.ethernet.waveform.get_counter() \n
		Queries the number of waveforms that are uploaded to and already played from the ARB memory. \n
			:return: waveform_counter: integer
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:ETHernet:WAVeform:COUNter?')
		return Conversions.str_to_int(response)

	def get_info(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:ETHernet:WAVeform:INFO \n
		Snippet: value: List[str] = driver.source.bb.arbitrary.ethernet.waveform.get_info() \n
		Queries information about the currently played waveform in a comma-separated list. The table below list all parameters
		that are queried.
			Table Header: Parameter / Description \n
			- Waveform counter / Integer number of played waveforms
			- Comment / Waveform name or comment tag
			- Clock / Clock rate in Hz
			- Marker x / Marker mode for marker x. x can be 1 to 3.
			- Peak level / RF signal peak level
			- RMS level / RF signal RMS level
			- Samples / Number of played waveform samples \n
			:return: arb_eth_wave_info: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:ETHernet:WAVeform:INFO?')
		return Conversions.str_to_str_list(response)

	def get_status(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:ETHernet:[WAVeform]:STATus \n
		Snippet: value: str = driver.source.bb.arbitrary.ethernet.waveform.get_status() \n
		Queries the status of the ARB Ethernet upload application. \n
			:return: status: string 'not loaded' No waveform data available as source. 'loading' Loads waveform data into the ARB memory of the R&S SMW200A. The R&S SMW200A receives the data from the external device connected to the QSFP+ network. 'loaded' Waveform data is loaded into the ARB memory and ready for playback.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:ETHernet:WAVeform:STATus?')
		return trim_str_response(response)

	def clone(self) -> 'WaveformCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = WaveformCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
