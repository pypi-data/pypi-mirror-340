from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	def set(self, pattern: str, bitcount: int, mobileStation=repcap.MobileStation.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:C2K:MSTation<ST>:CHANnel<CH>:DATA:PATTern \n
		Snippet: driver.source.bb.c2K.mstation.channel.data.pattern.set(pattern = rawAbc, bitcount = 1, mobileStation = repcap.MobileStation.Default, channel = repcap.Channel.Default) \n
		Sets the bit pattern for the data component when the PATTern data source is selected. The first parameter determines the
		bit pattern (choice of hexadecimal, octal or binary notation) , the second specifies the number of bits to use. For the
		traffic channels, this value is specific for the selected radio configuration. \n
			:param pattern: numeric
			:param bitcount: integer Range: 1 to 64
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('pattern', pattern, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:MSTation{mobileStation_cmd_val}:CHANnel{channel_cmd_val}:DATA:PATTern {param}'.rstrip())

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Pattern: str: numeric
			- 2 Bitcount: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Pattern'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: str = None
			self.Bitcount: int = None

	def get(self, mobileStation=repcap.MobileStation.Default, channel=repcap.Channel.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:C2K:MSTation<ST>:CHANnel<CH>:DATA:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.c2K.mstation.channel.data.pattern.get(mobileStation = repcap.MobileStation.Default, channel = repcap.Channel.Default) \n
		Sets the bit pattern for the data component when the PATTern data source is selected. The first parameter determines the
		bit pattern (choice of hexadecimal, octal or binary notation) , the second specifies the number of bits to use. For the
		traffic channels, this value is specific for the selected radio configuration. \n
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:C2K:MSTation{mobileStation_cmd_val}:CHANnel{channel_cmd_val}:DATA:PATTern?', self.__class__.PatternStruct())
