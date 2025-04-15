from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DlistCls:
	"""Dlist commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dlist", core, parent)

	def set(self, data_list: str, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:TTAB:TSL<CH0>:DLISt \n
		Snippet: driver.source.bb.dvb.dvbs.ttab.tsl.dlist.set(data_list = 'abc', channelNull = repcap.ChannelNull.Default) \n
		Requires [:SOURce<hw>]:BB:DVB:DVBS|DVBX:STYPe GP|GC and [:SOURce<hw>]:BB:DVB:DVBS|DVBX:TTAB:TSL<ch0>:DATA DLISt. Selects
		a data list file for the respective time slice. The file extension for data list files is *.dm_iqd. \n
			:param data_list: string
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tsl')
		"""
		param = Conversions.value_to_quoted_str(data_list)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:TTAB:TSL{channelNull_cmd_val}:DLISt {param}')

	def get(self, channelNull=repcap.ChannelNull.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:TTAB:TSL<CH0>:DLISt \n
		Snippet: value: str = driver.source.bb.dvb.dvbs.ttab.tsl.dlist.get(channelNull = repcap.ChannelNull.Default) \n
		Requires [:SOURce<hw>]:BB:DVB:DVBS|DVBX:STYPe GP|GC and [:SOURce<hw>]:BB:DVB:DVBS|DVBX:TTAB:TSL<ch0>:DATA DLISt. Selects
		a data list file for the respective time slice. The file extension for data list files is *.dm_iqd. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tsl')
			:return: data_list: string"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DVB:DVBS:TTAB:TSL{channelNull_cmd_val}:DLISt?')
		return trim_str_response(response)
