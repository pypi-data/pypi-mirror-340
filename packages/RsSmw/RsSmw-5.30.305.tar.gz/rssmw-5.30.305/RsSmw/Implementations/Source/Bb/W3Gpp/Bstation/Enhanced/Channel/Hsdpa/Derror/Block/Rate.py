from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RateCls:
	"""Rate commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rate", core, parent)

	def set(self, rate: float, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:[ENHanced]:CHANnel<CH0>:HSDPa:DERRor:BLOCk:RATE \n
		Snippet: driver.source.bb.w3Gpp.bstation.enhanced.channel.hsdpa.derror.block.rate.set(rate = 1.0, channelNull = repcap.ChannelNull.Default) \n
		The command sets the block error rate. \n
			:param rate: float Range: 1E-4 to 5E-1
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')
		"""
		param = Conversions.decimal_value_to_str(rate)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channelNull_cmd_val}:HSDPa:DERRor:BLOCk:RATE {param}')

	def get(self, channelNull=repcap.ChannelNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:[ENHanced]:CHANnel<CH0>:HSDPa:DERRor:BLOCk:RATE \n
		Snippet: value: float = driver.source.bb.w3Gpp.bstation.enhanced.channel.hsdpa.derror.block.rate.get(channelNull = repcap.ChannelNull.Default) \n
		The command sets the block error rate. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')
			:return: rate: float Range: 1E-4 to 5E-1"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channelNull_cmd_val}:HSDPa:DERRor:BLOCk:RATE?')
		return Conversions.str_to_float(response)
