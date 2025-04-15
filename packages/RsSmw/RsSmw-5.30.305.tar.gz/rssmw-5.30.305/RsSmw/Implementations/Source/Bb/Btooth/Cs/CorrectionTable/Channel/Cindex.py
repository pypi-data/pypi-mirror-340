from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CindexCls:
	"""Cindex commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cindex", core, parent)

	def get(self, channelNull=repcap.ChannelNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CTABle:[CHANnel<CH0>]:CINDex \n
		Snippet: value: int = driver.source.bb.btooth.cs.correctionTable.channel.cindex.get(channelNull = repcap.ChannelNull.Default) \n
		Queries the channel index of the channel. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')
			:return: cs_channel_index: integer For a description, see also table Table 'CS channel index and allowed channels'. Range: 0 to 78"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:CTABle:CHANnel{channelNull_cmd_val}:CINDex?')
		return Conversions.str_to_int(response)
