from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GhDisableCls:
	"""GhDisable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ghDisable", core, parent)

	def set(self, nbiot_dis_gh: bool, userEquipment=repcap.UserEquipment.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:GHDisable \n
		Snippet: driver.source.bb.eutra.uplink.ue.niot.ghDisable.set(nbiot_dis_gh = False, userEquipment = repcap.UserEquipment.Default) \n
		Disables NDRS group hopping for the selected UE. \n
			:param nbiot_dis_gh: 1| ON| 0| OFF
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
		"""
		param = Conversions.bool_to_str(nbiot_dis_gh)
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{userEquipment_cmd_val}:NIOT:GHDisable {param}')

	def get(self, userEquipment=repcap.UserEquipment.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:GHDisable \n
		Snippet: value: bool = driver.source.bb.eutra.uplink.ue.niot.ghDisable.get(userEquipment = repcap.UserEquipment.Default) \n
		Disables NDRS group hopping for the selected UE. \n
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: nbiot_dis_gh: 1| ON| 0| OFF"""
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{userEquipment_cmd_val}:NIOT:GHDisable?')
		return Conversions.str_to_bool(response)
