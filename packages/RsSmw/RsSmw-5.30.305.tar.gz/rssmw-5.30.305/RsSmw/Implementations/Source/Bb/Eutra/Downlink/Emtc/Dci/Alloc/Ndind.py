from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NdindCls:
	"""Ndind commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ndind", core, parent)

	def set(self, dci_new_data_ind: bool, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:DCI:ALLoc<CH0>:NDINd \n
		Snippet: driver.source.bb.eutra.downlink.emtc.dci.alloc.ndind.set(dci_new_data_ind = False, allocationNull = repcap.AllocationNull.Default) \n
		Sets the DCI field new data indicator. \n
			:param dci_new_data_ind: 1| ON| 0| OFF
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
		"""
		param = Conversions.bool_to_str(dci_new_data_ind)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:DCI:ALLoc{allocationNull_cmd_val}:NDINd {param}')

	def get(self, allocationNull=repcap.AllocationNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:DCI:ALLoc<CH0>:NDINd \n
		Snippet: value: bool = driver.source.bb.eutra.downlink.emtc.dci.alloc.ndind.get(allocationNull = repcap.AllocationNull.Default) \n
		Sets the DCI field new data indicator. \n
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: dci_new_data_ind: 1| ON| 0| OFF"""
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:DCI:ALLoc{allocationNull_cmd_val}:NDINd?')
		return Conversions.str_to_bool(response)
