from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal.StructBase import StructBase
from ..Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MemoryCls:
	"""Memory commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("memory", core, parent)

	# noinspection PyTypeChecker
	class HfreeStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Total_Phys_Mem_Kb: int: integer Total physical memory.
			- Applic_Mem_Kb: int: integer Application memory.
			- Heap_Used_Kb: int: integer Used heap memory.
			- Heap_Available_Kb: int: integer Available heap memory."""
		__meta_args_list = [
			ArgStruct.scalar_int('Total_Phys_Mem_Kb'),
			ArgStruct.scalar_int('Applic_Mem_Kb'),
			ArgStruct.scalar_int('Heap_Used_Kb'),
			ArgStruct.scalar_int('Heap_Available_Kb')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Total_Phys_Mem_Kb: int = None
			self.Applic_Mem_Kb: int = None
			self.Heap_Used_Kb: int = None
			self.Heap_Available_Kb: int = None

	def get_hfree(self) -> HfreeStruct:
		"""SCPI: MEMory:HFRee \n
		Snippet: value: HfreeStruct = driver.memory.get_hfree() \n
		Returns the used and available memory in Kb. \n
			:return: structure: for return value, see the help for HfreeStruct structure arguments.
		"""
		return self._core.io.query_struct('MEMory:HFRee?', self.__class__.HfreeStruct())
