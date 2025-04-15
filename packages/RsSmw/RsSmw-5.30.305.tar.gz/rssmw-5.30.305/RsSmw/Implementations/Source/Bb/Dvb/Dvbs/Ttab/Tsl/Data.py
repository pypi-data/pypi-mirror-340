from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DataCls:
	"""Data commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("data", core, parent)

	def set(self, data_source: enums.DataSourceA, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:TTAB:TSL<CH0>:DATA \n
		Snippet: driver.source.bb.dvb.dvbs.ttab.tsl.data.set(data_source = enums.DataSourceA.DLISt, channelNull = repcap.ChannelNull.Default) \n
		Requires [:SOURce<hw>]:BB:DVB:DVBS|DVBX:STYPe GP|GC. Sets the data source for the payload of the respective time slice. \n
			:param data_source: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt ZERO|ONE An internally generated sequence containing 0 data or 1 data. PATTern An internally generated sequence according to a bit pattern. PNxx An internally generated pseudo-random noise sequence. DLISt Binary data from a list file, internally or externally generated.
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tsl')
		"""
		param = Conversions.enum_scalar_to_str(data_source, enums.DataSourceA)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:TTAB:TSL{channelNull_cmd_val}:DATA {param}')

	# noinspection PyTypeChecker
	def get(self, channelNull=repcap.ChannelNull.Default) -> enums.DataSourceA:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:TTAB:TSL<CH0>:DATA \n
		Snippet: value: enums.DataSourceA = driver.source.bb.dvb.dvbs.ttab.tsl.data.get(channelNull = repcap.ChannelNull.Default) \n
		Requires [:SOURce<hw>]:BB:DVB:DVBS|DVBX:STYPe GP|GC. Sets the data source for the payload of the respective time slice. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tsl')
			:return: data_source: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt ZERO|ONE An internally generated sequence containing 0 data or 1 data. PATTern An internally generated sequence according to a bit pattern. PNxx An internally generated pseudo-random noise sequence. DLISt Binary data from a list file, internally or externally generated."""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DVB:DVBS:TTAB:TSL{channelNull_cmd_val}:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.DataSourceA)
