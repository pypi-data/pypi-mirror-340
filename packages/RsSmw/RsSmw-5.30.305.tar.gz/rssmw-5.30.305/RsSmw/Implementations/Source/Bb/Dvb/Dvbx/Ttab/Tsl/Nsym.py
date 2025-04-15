from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NsymCls:
	"""Nsym commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nsym", core, parent)

	def get(self, channelNull=repcap.ChannelNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBX:TTAB:TSL<CH0>:NSYM \n
		Snippet: value: int = driver.source.bb.dvb.dvbx.ttab.tsl.nsym.get(channelNull = repcap.ChannelNull.Default) \n
		Queries the number of symbols of the FEC frame of the respective time slice. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tsl')
			:return: num_of_symbols: integer Range: 8400 to 34000"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DVB:DVBX:TTAB:TSL{channelNull_cmd_val}:NSYM?')
		return Conversions.str_to_int(response)
