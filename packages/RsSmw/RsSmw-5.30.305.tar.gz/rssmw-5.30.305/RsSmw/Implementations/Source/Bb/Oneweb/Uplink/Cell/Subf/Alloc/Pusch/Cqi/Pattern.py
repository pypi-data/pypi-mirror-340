from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal.Types import DataType
from ...........Internal.StructBase import StructBase
from ...........Internal.ArgStruct import ArgStruct
from ...........Internal.ArgSingleList import ArgSingleList
from ...........Internal.ArgSingle import ArgSingle
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	def set(self, pattern: str, bitcount: int, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:[CELL<CCIDX>]:[SUBF<ST0>]:ALLoc<CH0>:PUSCh:CQI:PATTern \n
		Snippet: driver.source.bb.oneweb.uplink.cell.subf.alloc.pusch.cqi.pattern.set(pattern = rawAbc, bitcount = 1, cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Sets the CQI pattern for the PUSCH. The length of the pattern is determined by the number of CQI bits
		([:SOURce<hw>]:BB:ONEWeb:UL[:CELL<ccidx>][:SUBF<st0>]:ALLoc<ch0>:PUSCh:CQI:CBITs?) . \n
			:param pattern: numeric
			:param bitcount: integer Range: 1 to 1024
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('pattern', pattern, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:UL:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:ALLoc{allocationNull_cmd_val}:PUSCh:CQI:PATTern {param}'.rstrip())

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Pattern: str: numeric
			- 2 Bitcount: int: integer Range: 1 to 1024"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Pattern'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: str = None
			self.Bitcount: int = None

	def get(self, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, allocationNull=repcap.AllocationNull.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:[CELL<CCIDX>]:[SUBF<ST0>]:ALLoc<CH0>:PUSCh:CQI:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.oneweb.uplink.cell.subf.alloc.pusch.cqi.pattern.get(cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Sets the CQI pattern for the PUSCH. The length of the pattern is determined by the number of CQI bits
		([:SOURce<hw>]:BB:ONEWeb:UL[:CELL<ccidx>][:SUBF<st0>]:ALLoc<ch0>:PUSCh:CQI:CBITs?) . \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:ONEWeb:UL:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:ALLoc{allocationNull_cmd_val}:PUSCh:CQI:PATTern?', self.__class__.PatternStruct())
