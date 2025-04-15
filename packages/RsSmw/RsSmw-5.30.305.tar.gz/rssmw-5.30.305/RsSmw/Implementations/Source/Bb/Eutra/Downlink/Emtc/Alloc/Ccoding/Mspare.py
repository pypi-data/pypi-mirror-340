from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Utilities import trim_str_response
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MspareCls:
	"""Mspare commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mspare", core, parent)

	def set(self, mib_spare_bits: str, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH0>:CCODing:MSPare \n
		Snippet: driver.source.bb.eutra.downlink.emtc.alloc.ccoding.mspare.set(mib_spare_bits = rawAbc, allocationNull = repcap.AllocationNull.Default) \n
		Sets the spare bits in the PBCH transmission. \n
			:param mib_spare_bits: 5 bits
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
		"""
		param = Conversions.value_to_str(mib_spare_bits)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{allocationNull_cmd_val}:CCODing:MSPare {param}')

	def get(self, allocationNull=repcap.AllocationNull.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH0>:CCODing:MSPare \n
		Snippet: value: str = driver.source.bb.eutra.downlink.emtc.alloc.ccoding.mspare.get(allocationNull = repcap.AllocationNull.Default) \n
		Sets the spare bits in the PBCH transmission. \n
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: mib_spare_bits: 5 bits"""
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{allocationNull_cmd_val}:CCODing:MSPare?')
		return trim_str_response(response)
