from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PrttCls:
	"""Prtt commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("prtt", core, parent)

	def set(self, transition_time: float, userEquipment=repcap.UserEquipment.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:PRTT \n
		Snippet: driver.source.bb.eutra.uplink.ue.prach.prtt.set(transition_time = 1.0, userEquipment = repcap.UserEquipment.Default) \n
		Defines the transition time from beginning of the extended preamble to the start of the preamble itself. \n
			:param transition_time: float Range: 0 to 3E-5, Unit: s
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
		"""
		param = Conversions.decimal_value_to_str(transition_time)
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{userEquipment_cmd_val}:PRACh:PRTT {param}')

	def get(self, userEquipment=repcap.UserEquipment.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:PRTT \n
		Snippet: value: float = driver.source.bb.eutra.uplink.ue.prach.prtt.get(userEquipment = repcap.UserEquipment.Default) \n
		Defines the transition time from beginning of the extended preamble to the start of the preamble itself. \n
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: transition_time: float Range: 0 to 3E-5, Unit: s"""
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{userEquipment_cmd_val}:PRACh:PRTT?')
		return Conversions.str_to_float(response)
