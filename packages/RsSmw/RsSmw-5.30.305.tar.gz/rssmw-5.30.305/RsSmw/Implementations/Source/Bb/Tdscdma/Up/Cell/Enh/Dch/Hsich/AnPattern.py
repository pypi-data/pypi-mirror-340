from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from ..........Internal.ArgSingleList import ArgSingleList
from ..........Internal.ArgSingle import ArgSingle
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AnPatternCls:
	"""AnPattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("anPattern", core, parent)

	def set(self, an_pattern: str, bitcount: int, cell=repcap.Cell.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:HSICh:ANPattern \n
		Snippet: driver.source.bb.tdscdma.up.cell.enh.dch.hsich.anPattern.set(an_pattern = rawAbc, bitcount = 1, cell = repcap.Cell.Default) \n
		Sets the ACK/NACK Pattern and the maximum pattern length. A '1' corresponds to ACK, a '0' to NAK. \n
			:param an_pattern: numeric
			:param bitcount: integer Range: 1 to 36
			:param cell: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('an_pattern', an_pattern, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		cell_cmd_val = self._cmd_group.get_repcap_cmd_value(cell, repcap.Cell)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{cell_cmd_val}:ENH:DCH:HSICh:ANPattern {param}'.rstrip())

	# noinspection PyTypeChecker
	class AnPatternStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 An_Pattern: str: numeric
			- 2 Bitcount: int: integer Range: 1 to 36"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('An_Pattern'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.An_Pattern: str = None
			self.Bitcount: int = None

	def get(self, cell=repcap.Cell.Default) -> AnPatternStruct:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:HSICh:ANPattern \n
		Snippet: value: AnPatternStruct = driver.source.bb.tdscdma.up.cell.enh.dch.hsich.anPattern.get(cell = repcap.Cell.Default) \n
		Sets the ACK/NACK Pattern and the maximum pattern length. A '1' corresponds to ACK, a '0' to NAK. \n
			:param cell: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: structure: for return value, see the help for AnPatternStruct structure arguments."""
		cell_cmd_val = self._cmd_group.get_repcap_cmd_value(cell, repcap.Cell)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{cell_cmd_val}:ENH:DCH:HSICh:ANPattern?', self.__class__.AnPatternStruct())
