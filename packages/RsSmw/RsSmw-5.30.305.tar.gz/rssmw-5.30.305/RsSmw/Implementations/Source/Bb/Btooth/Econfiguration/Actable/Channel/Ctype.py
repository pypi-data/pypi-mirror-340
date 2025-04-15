from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CtypeCls:
	"""Ctype commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ctype", core, parent)

	# noinspection PyTypeChecker
	def get(self, channelNull=repcap.ChannelNull.Default) -> enums.BtoChnnelTypeAdv:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:ACTable:CHANnel<CH0>:CTYPe \n
		Snippet: value: enums.BtoChnnelTypeAdv = driver.source.bb.btooth.econfiguration.actable.channel.ctype.get(channelNull = repcap.ChannelNull.Default) \n
		Queries the channel type for advertising or data channels. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')
			:return: channel_type: DATA"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:ACTable:CHANnel{channelNull_cmd_val}:CTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoChnnelTypeAdv)
