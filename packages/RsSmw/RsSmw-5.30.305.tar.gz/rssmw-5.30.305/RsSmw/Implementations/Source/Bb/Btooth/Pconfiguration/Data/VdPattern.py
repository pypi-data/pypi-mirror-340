from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class VdPatternCls:
	"""VdPattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("vdPattern", core, parent)

	def set(self, vd_pattern: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PCONfiguration:DATA:VDPAttern \n
		Snippet: driver.source.bb.btooth.pconfiguration.data.vdPattern.set(vd_pattern = rawAbc, bitcount = 1) \n
		Sets the bit pattern for the voice data. \n
			:param vd_pattern: numeric
			:param bitcount: integer Range: 1 to 64
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('vd_pattern', vd_pattern, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DATA:VDPAttern {param}'.rstrip())

	# noinspection PyTypeChecker
	class VdPatternStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Vd_Pattern: str: numeric
			- 2 Bitcount: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Vd_Pattern'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Vd_Pattern: str = None
			self.Bitcount: int = None

	def get(self) -> VdPatternStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PCONfiguration:DATA:VDPAttern \n
		Snippet: value: VdPatternStruct = driver.source.bb.btooth.pconfiguration.data.vdPattern.get() \n
		Sets the bit pattern for the voice data. \n
			:return: structure: for return value, see the help for VdPatternStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DATA:VDPAttern?', self.__class__.VdPatternStruct())
