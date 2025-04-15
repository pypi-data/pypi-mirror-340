from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PucchCls:
	"""Pucch commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pucch", core, parent)

	def set(self, con_sub_frames: int, userEquipment=repcap.UserEquipment.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:UE<ST>:CONSubframes:PUCCh \n
		Snippet: driver.source.bb.oneweb.uplink.ue.conSubFrames.pucch.set(con_sub_frames = 1, userEquipment = repcap.UserEquipment.Default) \n
		Sets the number of configurable subframes. \n
			:param con_sub_frames: integer Range: 1 to 40
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
		"""
		param = Conversions.decimal_value_to_str(con_sub_frames)
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:UL:UE{userEquipment_cmd_val}:CONSubframes:PUCCh {param}')

	def get(self, userEquipment=repcap.UserEquipment.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:UE<ST>:CONSubframes:PUCCh \n
		Snippet: value: int = driver.source.bb.oneweb.uplink.ue.conSubFrames.pucch.get(userEquipment = repcap.UserEquipment.Default) \n
		Sets the number of configurable subframes. \n
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: con_sub_frames: No help available"""
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ONEWeb:UL:UE{userEquipment_cmd_val}:CONSubframes:PUCCh?')
		return Conversions.str_to_int(response)
