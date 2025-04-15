from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	def set(self, pattern: str, bitcount: int, userNull=repcap.UserNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:OFDM:USER<CH0>:PATTern \n
		Snippet: driver.source.bb.ofdm.user.pattern.set(pattern = rawAbc, bitcount = 1, userNull = repcap.UserNull.Default) \n
		Sets a bit pattern as a data source. \n
			:param pattern: numeric
			:param bitcount: integer Range: 1 to 64
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('pattern', pattern, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:USER{userNull_cmd_val}:PATTern {param}'.rstrip())

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

	def get(self, userNull=repcap.UserNull.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:OFDM:USER<CH0>:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.ofdm.user.pattern.get(userNull = repcap.UserNull.Default) \n
		Sets a bit pattern as a data source. \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:OFDM:USER{userNull_cmd_val}:PATTern?', self.__class__.PatternStruct())
