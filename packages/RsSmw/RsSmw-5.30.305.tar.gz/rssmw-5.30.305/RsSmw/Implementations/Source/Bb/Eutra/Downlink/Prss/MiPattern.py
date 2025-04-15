from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MiPatternCls:
	"""MiPattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("miPattern", core, parent)

	def set(self, prs_muting_info: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:PRSS:MIPattern \n
		Snippet: driver.source.bb.eutra.downlink.prss.miPattern.set(prs_muting_info = rawAbc, bitcount = 1) \n
		Specifies a bit pattern that defines the muted and not muted PRS. \n
			:param prs_muting_info: numeric Each bit defines the PRS state of one PRS occasion 0 PRS is muted 1 PRS is transmitted
			:param bitcount: integer 2, 4, 8 or 16 bits Range: 2 to 16
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('prs_muting_info', prs_muting_info, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:PRSS:MIPattern {param}'.rstrip())

	# noinspection PyTypeChecker
	class MiPatternStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Prs_Muting_Info: str: numeric Each bit defines the PRS state of one PRS occasion 0 PRS is muted 1 PRS is transmitted
			- 2 Bitcount: int: integer 2, 4, 8 or 16 bits Range: 2 to 16"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Prs_Muting_Info'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Prs_Muting_Info: str = None
			self.Bitcount: int = None

	def get(self) -> MiPatternStruct:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:PRSS:MIPattern \n
		Snippet: value: MiPatternStruct = driver.source.bb.eutra.downlink.prss.miPattern.get() \n
		Specifies a bit pattern that defines the muted and not muted PRS. \n
			:return: structure: for return value, see the help for MiPatternStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:EUTRa:DL:PRSS:MIPattern?', self.__class__.MiPatternStruct())
