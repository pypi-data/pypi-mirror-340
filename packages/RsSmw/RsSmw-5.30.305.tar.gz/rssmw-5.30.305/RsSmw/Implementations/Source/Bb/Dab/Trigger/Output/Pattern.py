from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	def set(self, pattern: str, bitcount: int, output=repcap.Output.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:DAB:TRIGger:OUTPut<CH>:PATTern \n
		Snippet: driver.source.bb.dab.trigger.output.pattern.set(pattern = rawAbc, bitcount = 1, output = repcap.Output.Default) \n
		No command help available \n
			:param pattern: No help available
			:param bitcount: No help available
			:param output: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('pattern', pattern, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		output_cmd_val = self._cmd_group.get_repcap_cmd_value(output, repcap.Output)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:TRIGger:OUTPut{output_cmd_val}:PATTern {param}'.rstrip())

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Pattern: str: No parameter help available
			- 2 Bitcount: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Pattern'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: str = None
			self.Bitcount: int = None

	def get(self, output=repcap.Output.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:DAB:TRIGger:OUTPut<CH>:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.dab.trigger.output.pattern.get(output = repcap.Output.Default) \n
		No command help available \n
			:param output: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		output_cmd_val = self._cmd_group.get_repcap_cmd_value(output, repcap.Output)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:DAB:TRIGger:OUTPut{output_cmd_val}:PATTern?', self.__class__.PatternStruct())
