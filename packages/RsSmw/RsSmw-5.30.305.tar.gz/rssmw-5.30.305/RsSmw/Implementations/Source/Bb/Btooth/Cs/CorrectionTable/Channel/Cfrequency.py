from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CfrequencyCls:
	"""Cfrequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cfrequency", core, parent)

	def get(self, channelNull=repcap.ChannelNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CTABle:[CHANnel<CH0>]:CFRequency \n
		Snippet: value: float = driver.source.bb.btooth.cs.correctionTable.channel.cfrequency.get(channelNull = repcap.ChannelNull.Default) \n
		Queries the center frequency of the channel. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')
			:return: center_freq: float For a description, see also table Table 'CS channel index and allowed channels'. Range: 2402 to 2480"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:CTABle:CHANnel{channelNull_cmd_val}:CFRequency?')
		return Conversions.str_to_float(response)
