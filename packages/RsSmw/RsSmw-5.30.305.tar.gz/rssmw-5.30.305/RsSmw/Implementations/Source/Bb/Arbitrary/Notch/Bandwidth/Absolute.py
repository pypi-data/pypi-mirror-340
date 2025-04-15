from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AbsoluteCls:
	"""Absolute commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("absolute", core, parent)

	def set(self, no_bw: float, notchFilter=repcap.NotchFilter.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:NOTCh<CH>:BWIDth:[ABSolute] \n
		Snippet: driver.source.bb.arbitrary.notch.bandwidth.absolute.set(no_bw = 1.0, notchFilter = repcap.NotchFilter.Default) \n
		Sets the absolute notch bandwidth. The value is interdependent with the relative bandwidth value, set with the command
		[:SOURce<hw>]:BB:ARBitrary:NOTCh<ch>:BWIDth:RELative. That is, you cna set the notch bandwidth in either way. \n
			:param no_bw: float Range: 0 to dynamic
			:param notchFilter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
		"""
		param = Conversions.decimal_value_to_str(no_bw)
		notchFilter_cmd_val = self._cmd_group.get_repcap_cmd_value(notchFilter, repcap.NotchFilter)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:NOTCh{notchFilter_cmd_val}:BWIDth:ABSolute {param}')

	def get(self, notchFilter=repcap.NotchFilter.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:NOTCh<CH>:BWIDth:[ABSolute] \n
		Snippet: value: float = driver.source.bb.arbitrary.notch.bandwidth.absolute.get(notchFilter = repcap.NotchFilter.Default) \n
		Sets the absolute notch bandwidth. The value is interdependent with the relative bandwidth value, set with the command
		[:SOURce<hw>]:BB:ARBitrary:NOTCh<ch>:BWIDth:RELative. That is, you cna set the notch bandwidth in either way. \n
			:param notchFilter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
			:return: no_bw: float Range: 0 to dynamic"""
		notchFilter_cmd_val = self._cmd_group.get_repcap_cmd_value(notchFilter, repcap.NotchFilter)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ARBitrary:NOTCh{notchFilter_cmd_val}:BWIDth:ABSolute?')
		return Conversions.str_to_float(response)
