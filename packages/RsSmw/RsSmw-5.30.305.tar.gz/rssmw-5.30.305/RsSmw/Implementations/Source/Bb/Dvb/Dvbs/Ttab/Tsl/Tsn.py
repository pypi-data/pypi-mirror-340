from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TsnCls:
	"""Tsn commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tsn", core, parent)

	def set(self, tsn: str, bitcount: int, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:TTAB:TSL<CH0>:TSN \n
		Snippet: driver.source.bb.dvb.dvbs.ttab.tsl.tsn.set(tsn = rawAbc, bitcount = 1, channelNull = repcap.ChannelNull.Default) \n
		Sets the 8-bit sized time-slice number in hexadecimal representation. Syntax to enter the hexadecimal value of the time
		slice number:#H<value>,8 \n
			:param tsn: numeric
			:param bitcount: integer Range: 8 to 8
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tsl')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('tsn', tsn, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:TTAB:TSL{channelNull_cmd_val}:TSN {param}'.rstrip())

	# noinspection PyTypeChecker
	class TsnStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Tsn: str: numeric
			- 2 Bitcount: int: integer Range: 8 to 8"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Tsn'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Tsn: str = None
			self.Bitcount: int = None

	def get(self, channelNull=repcap.ChannelNull.Default) -> TsnStruct:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:TTAB:TSL<CH0>:TSN \n
		Snippet: value: TsnStruct = driver.source.bb.dvb.dvbs.ttab.tsl.tsn.get(channelNull = repcap.ChannelNull.Default) \n
		Sets the 8-bit sized time-slice number in hexadecimal representation. Syntax to enter the hexadecimal value of the time
		slice number:#H<value>,8 \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tsl')
			:return: structure: for return value, see the help for TsnStruct structure arguments."""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:DVB:DVBS:TTAB:TSL{channelNull_cmd_val}:TSN?', self.__class__.TsnStruct())
