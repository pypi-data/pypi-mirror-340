from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IdcceCls:
	"""Idcce commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("idcce", core, parent)

	def set(self, dci_cce_index: int, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:DCI:ALLoc<CH0>:IDCCe \n
		Snippet: driver.source.bb.eutra.downlink.emtc.dci.alloc.idcce.set(dci_cce_index = 1, allocationNull = repcap.AllocationNull.Default) \n
		For UE-specific search space, sets the ECCE start index. \n
			:param dci_cce_index: integer Range: 0 to 24
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
		"""
		param = Conversions.decimal_value_to_str(dci_cce_index)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:DCI:ALLoc{allocationNull_cmd_val}:IDCCe {param}')

	def get(self, allocationNull=repcap.AllocationNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:DCI:ALLoc<CH0>:IDCCe \n
		Snippet: value: int = driver.source.bb.eutra.downlink.emtc.dci.alloc.idcce.get(allocationNull = repcap.AllocationNull.Default) \n
		For UE-specific search space, sets the ECCE start index. \n
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: dci_cce_index: integer Range: 0 to 24"""
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:DCI:ALLoc{allocationNull_cmd_val}:IDCCe?')
		return Conversions.str_to_int(response)
