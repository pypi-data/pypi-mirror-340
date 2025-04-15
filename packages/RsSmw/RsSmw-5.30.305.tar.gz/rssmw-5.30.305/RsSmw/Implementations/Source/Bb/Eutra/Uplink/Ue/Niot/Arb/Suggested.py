from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SuggestedCls:
	"""Suggested commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("suggested", core, parent)

	def get(self, userEquipment=repcap.UserEquipment.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:ARB:SUGGested \n
		Snippet: value: int = driver.source.bb.eutra.uplink.ue.niot.arb.suggested.get(userEquipment = repcap.UserEquipment.Default) \n
		Queries the ARB sequence length that is required for the selected NPUSCH transmissions. \n
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: nbiot_sugg_seq_len: integer Range: 0 to 1E4"""
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{userEquipment_cmd_val}:NIOT:ARB:SUGGested?')
		return Conversions.str_to_int(response)
