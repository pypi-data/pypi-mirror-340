from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BdaLapCls:
	"""BdaLap commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bdaLap", core, parent)

	def set(self, bda_lap: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PCONfiguration:BDALap \n
		Snippet: driver.source.bb.btooth.pconfiguration.bdaLap.set(bda_lap = rawAbc, bitcount = 1) \n
		Sets the lower address part of Bluetooth Device Address. The length of LAP is 24 bits or 6 hexadecimal figures. \n
			:param bda_lap: numeric Range: #H000000 to #HFFFFFF
			:param bitcount: integer Range: 8 to 24
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('bda_lap', bda_lap, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:BDALap {param}'.rstrip())

	# noinspection PyTypeChecker
	class BdaLapStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Bda_Lap: str: numeric Range: #H000000 to #HFFFFFF
			- 2 Bitcount: int: integer Range: 8 to 24"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Bda_Lap'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Bda_Lap: str = None
			self.Bitcount: int = None

	def get(self) -> BdaLapStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PCONfiguration:BDALap \n
		Snippet: value: BdaLapStruct = driver.source.bb.btooth.pconfiguration.bdaLap.get() \n
		Sets the lower address part of Bluetooth Device Address. The length of LAP is 24 bits or 6 hexadecimal figures. \n
			:return: structure: for return value, see the help for BdaLapStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:BDALap?', self.__class__.BdaLapStruct())
