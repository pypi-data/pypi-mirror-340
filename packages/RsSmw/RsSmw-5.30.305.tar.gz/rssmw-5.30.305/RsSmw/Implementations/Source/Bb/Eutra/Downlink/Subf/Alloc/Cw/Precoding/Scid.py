from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScidCls:
	"""Scid commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scid", core, parent)

	def set(self, scramb_identity: int, subframeNull=repcap.SubframeNull.Default, allocationNull=repcap.AllocationNull.Default, codeword=repcap.Codeword.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST0>]:ALLoc<CH0>:[CW<USER>]:PRECoding:SCID \n
		Snippet: driver.source.bb.eutra.downlink.subf.alloc.cw.precoding.scid.set(scramb_identity = 1, subframeNull = repcap.SubframeNull.Default, allocationNull = repcap.AllocationNull.Default, codeword = repcap.Codeword.Default) \n
		Sets the scrambling identity according to 36.211, sec. 6.10.3.1. This value is used for initialization of the sequence
		used for generation of the UE-specific reference signals. \n
			:param scramb_identity: integer Range: 0 to 1
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:param codeword: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cw')
		"""
		param = Conversions.decimal_value_to_str(scramb_identity)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		codeword_cmd_val = self._cmd_group.get_repcap_cmd_value(codeword, repcap.Codeword)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{subframeNull_cmd_val}:ALLoc{allocationNull_cmd_val}:CW{codeword_cmd_val}:PRECoding:SCID {param}')

	def get(self, subframeNull=repcap.SubframeNull.Default, allocationNull=repcap.AllocationNull.Default, codeword=repcap.Codeword.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST0>]:ALLoc<CH0>:[CW<USER>]:PRECoding:SCID \n
		Snippet: value: int = driver.source.bb.eutra.downlink.subf.alloc.cw.precoding.scid.get(subframeNull = repcap.SubframeNull.Default, allocationNull = repcap.AllocationNull.Default, codeword = repcap.Codeword.Default) \n
		Sets the scrambling identity according to 36.211, sec. 6.10.3.1. This value is used for initialization of the sequence
		used for generation of the UE-specific reference signals. \n
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:param codeword: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cw')
			:return: scramb_identity: integer Range: 0 to 1"""
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		codeword_cmd_val = self._cmd_group.get_repcap_cmd_value(codeword, repcap.Codeword)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{subframeNull_cmd_val}:ALLoc{allocationNull_cmd_val}:CW{codeword_cmd_val}:PRECoding:SCID?')
		return Conversions.str_to_int(response)
