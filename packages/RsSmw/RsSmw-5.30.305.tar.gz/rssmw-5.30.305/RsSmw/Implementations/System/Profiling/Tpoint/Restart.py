from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RestartCls:
	"""Restart commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("restart", core, parent)

	def set(self, module_name: str, test_point_name: str) -> None:
		"""SCPI: SYSTem:PROFiling:TPOint:RESTart \n
		Snippet: driver.system.profiling.tpoint.restart.set(module_name = 'abc', test_point_name = 'abc') \n
		No command help available \n
			:param module_name: No help available
			:param test_point_name: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('module_name', module_name, DataType.String), ArgSingle('test_point_name', test_point_name, DataType.String))
		self._core.io.write(f'SYSTem:PROFiling:TPOint:RESTart {param}'.rstrip())

	# noinspection PyTypeChecker
	class RestartStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Module_Name: str: No parameter help available
			- 2 Test_Point_Name: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_str('Module_Name'),
			ArgStruct.scalar_str('Test_Point_Name')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Module_Name: str = None
			self.Test_Point_Name: str = None

	def get(self) -> RestartStruct:
		"""SCPI: SYSTem:PROFiling:TPOint:RESTart \n
		Snippet: value: RestartStruct = driver.system.profiling.tpoint.restart.get() \n
		No command help available \n
			:return: structure: for return value, see the help for RestartStruct structure arguments."""
		return self._core.io.query_struct(f'SYSTem:PROFiling:TPOint:RESTart?', self.__class__.RestartStruct())
