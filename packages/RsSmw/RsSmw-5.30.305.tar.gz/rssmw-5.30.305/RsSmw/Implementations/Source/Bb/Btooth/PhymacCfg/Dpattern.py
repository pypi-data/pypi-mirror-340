from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DpatternCls:
	"""Dpattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dpattern", core, parent)

	def set(self, dpattern: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PHYMacCfg:DPAttern \n
		Snippet: driver.source.bb.btooth.phymacCfg.dpattern.set(dpattern = rawAbc, bitcount = 1) \n
		No command help available \n
			:param dpattern: No help available
			:param bitcount: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('dpattern', dpattern, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PHYMacCfg:DPAttern {param}'.rstrip())

	# noinspection PyTypeChecker
	class DpatternStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Dpattern: str: No parameter help available
			- 2 Bitcount: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Dpattern'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dpattern: str = None
			self.Bitcount: int = None

	def get(self) -> DpatternStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PHYMacCfg:DPAttern \n
		Snippet: value: DpatternStruct = driver.source.bb.btooth.phymacCfg.dpattern.get() \n
		No command help available \n
			:return: structure: for return value, see the help for DpatternStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:PHYMacCfg:DPAttern?', self.__class__.DpatternStruct())
