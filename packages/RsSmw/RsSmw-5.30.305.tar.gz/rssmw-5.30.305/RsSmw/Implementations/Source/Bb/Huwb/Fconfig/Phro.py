from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PhroCls:
	"""Phro commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("phro", core, parent)

	# noinspection PyTypeChecker
	class CwordStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Dpattern: str: No parameter help available
			- Bitcount: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Dpattern'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dpattern: str = None
			self.Bitcount: int = None

	def get_cword(self) -> CwordStruct:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:PHRO:CWORd \n
		Snippet: value: CwordStruct = driver.source.bb.huwb.fconfig.phro.get_cword() \n
		No command help available \n
			:return: structure: for return value, see the help for CwordStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:HUWB:FCONfig:PHRO:CWORd?', self.__class__.CwordStruct())
