from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PhysBitsCls:
	"""PhysBits commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("physBits", core, parent)

	def get(self, userEquipment=repcap.UserEquipment.Default, allocationNull=repcap.AllocationNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:ALLoc<CH0>:PHYSbits \n
		Snippet: value: int = driver.source.bb.eutra.uplink.ue.sl.alloc.physBits.get(userEquipment = repcap.UserEquipment.Default, allocationNull = repcap.AllocationNull.Default) \n
		Queries the number of physical bits occupied by the channel. \n
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: phys_bits: integer Range: 0 to 1E5"""
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{userEquipment_cmd_val}:SL:ALLoc{allocationNull_cmd_val}:PHYSbits?')
		return Conversions.str_to_int(response)
