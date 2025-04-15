from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, scram_state: bool, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH0>:SCRambling:STATe \n
		Snippet: driver.source.bb.eutra.downlink.emtc.alloc.scrambling.state.set(scram_state = False, allocationNull = repcap.AllocationNull.Default) \n
		Enables scrambling. \n
			:param scram_state: 1| ON| 0| OFF
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
		"""
		param = Conversions.bool_to_str(scram_state)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{allocationNull_cmd_val}:SCRambling:STATe {param}')

	def get(self, allocationNull=repcap.AllocationNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH0>:SCRambling:STATe \n
		Snippet: value: bool = driver.source.bb.eutra.downlink.emtc.alloc.scrambling.state.get(allocationNull = repcap.AllocationNull.Default) \n
		Enables scrambling. \n
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: scram_state: 1| ON| 0| OFF"""
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{allocationNull_cmd_val}:SCRambling:STATe?')
		return Conversions.str_to_bool(response)
