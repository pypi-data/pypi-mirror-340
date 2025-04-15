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

	def set(self, ack_nack_pattern: str, bitcount: str, subframeNull=repcap.SubframeNull.Default, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST0>]:ALLoc<CH0>:PUCCh:HARQ:ANPattern \n
		Snippet: driver.source.bb.eutra.uplink.subf.alloc.pucch.harq.anPattern.set(ack_nack_pattern = rawAbc, bitcount = rawAbc, subframeNull = repcap.SubframeNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		No command help available \n
			:param ack_nack_pattern: No help available
			:param bitcount: No help available
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('ack_nack_pattern', ack_nack_pattern, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.RawString))
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{subframeNull_cmd_val}:ALLoc{allocationNull_cmd_val}:PUCCh:HARQ:ANPattern {param}'.rstrip())

	# noinspection PyTypeChecker
	class AnPatternStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Ack_Nack_Pattern: str: No parameter help available
			- 2 Bitcount: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Ack_Nack_Pattern'),
			ArgStruct.scalar_raw_str('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ack_Nack_Pattern: str = None
			self.Bitcount: str = None

	def get(self, subframeNull=repcap.SubframeNull.Default, allocationNull=repcap.AllocationNull.Default) -> AnPatternStruct:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST0>]:ALLoc<CH0>:PUCCh:HARQ:ANPattern \n
		Snippet: value: AnPatternStruct = driver.source.bb.eutra.uplink.subf.alloc.pucch.harq.anPattern.get(subframeNull = repcap.SubframeNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		No command help available \n
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: structure: for return value, see the help for AnPatternStruct structure arguments."""
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{subframeNull_cmd_val}:ALLoc{allocationNull_cmd_val}:PUCCh:HARQ:ANPattern?', self.__class__.AnPatternStruct())
