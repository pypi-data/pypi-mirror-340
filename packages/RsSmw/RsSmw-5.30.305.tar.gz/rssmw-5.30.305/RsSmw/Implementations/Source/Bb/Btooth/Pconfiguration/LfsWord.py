from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LfsWordCls:
	"""LfsWord commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lfsWord", core, parent)

	def set(self, lap_for_sw: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PCONfiguration:LFSWord \n
		Snippet: driver.source.bb.btooth.pconfiguration.lfsWord.set(lap_for_sw = rawAbc, bitcount = 1) \n
		Sets the lower address part (LAP) of the sync word for FHS packets. The length of LAP is 24 bits or 6 hexadecimal figures. \n
			:param lap_for_sw: numeric Range: #H000000 to #HFFFFFF
			:param bitcount: integer Range: 8 to 24
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('lap_for_sw', lap_for_sw, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:LFSWord {param}'.rstrip())

	# noinspection PyTypeChecker
	class LfsWordStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Lap_For_Sw: str: numeric Range: #H000000 to #HFFFFFF
			- 2 Bitcount: int: integer Range: 8 to 24"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Lap_For_Sw'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lap_For_Sw: str = None
			self.Bitcount: int = None

	def get(self) -> LfsWordStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PCONfiguration:LFSWord \n
		Snippet: value: LfsWordStruct = driver.source.bb.btooth.pconfiguration.lfsWord.get() \n
		Sets the lower address part (LAP) of the sync word for FHS packets. The length of LAP is 24 bits or 6 hexadecimal figures. \n
			:return: structure: for return value, see the help for LfsWordStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:LFSWord?', self.__class__.LfsWordStruct())
