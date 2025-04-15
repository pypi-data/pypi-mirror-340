from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApatternCls:
	"""Apattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("apattern", core, parent)

	def set(self, dpattern: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACAD:APATtern \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.acad.apattern.set(dpattern = rawAbc, bitcount = 1) \n
		Specifies user-defined pattern.
		The settings is relevant for [:SOURce<hw>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACADPATTern \n
			:param dpattern: numeric
			:param bitcount: integer Range: 1 to 64
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('dpattern', dpattern, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACAD:APATtern {param}'.rstrip())

	# noinspection PyTypeChecker
	class ApatternStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Dpattern: str: numeric
			- 2 Bitcount: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Dpattern'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dpattern: str = None
			self.Bitcount: int = None

	def get(self) -> ApatternStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACAD:APATtern \n
		Snippet: value: ApatternStruct = driver.source.bb.btooth.econfiguration.pconfiguration.acad.apattern.get() \n
		Specifies user-defined pattern.
		The settings is relevant for [:SOURce<hw>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACADPATTern \n
			:return: structure: for return value, see the help for ApatternStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACAD:APATtern?', self.__class__.ApatternStruct())
