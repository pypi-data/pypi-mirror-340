from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PilotsCls:
	"""Pilots commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pilots", core, parent)

	def set(self, pilots: bool, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBX:TTAB:TSL<CH0>:PILots \n
		Snippet: driver.source.bb.dvb.dvbx.ttab.tsl.pilots.set(pilots = False, channelNull = repcap.ChannelNull.Default) \n
		Enables or disables the pilots in the FEC frame of the respective time slice. \n
			:param pilots: 1| ON| 0| OFF
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tsl')
		"""
		param = Conversions.bool_to_str(pilots)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBX:TTAB:TSL{channelNull_cmd_val}:PILots {param}')

	def get(self, channelNull=repcap.ChannelNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBX:TTAB:TSL<CH0>:PILots \n
		Snippet: value: bool = driver.source.bb.dvb.dvbx.ttab.tsl.pilots.get(channelNull = repcap.ChannelNull.Default) \n
		Enables or disables the pilots in the FEC frame of the respective time slice. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tsl')
			:return: pilots: 1| ON| 0| OFF"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DVB:DVBX:TTAB:TSL{channelNull_cmd_val}:PILots?')
		return Conversions.str_to_bool(response)
