from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OffsetIndCls:
	"""OffsetInd commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("offsetInd", core, parent)

	def set(self, offset_indicator: int, userEquipment=repcap.UserEquipment.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:RDATa:OFFSetind \n
		Snippet: driver.source.bb.eutra.uplink.ue.sl.rdata.offsetInd.set(offset_indicator = 1, userEquipment = repcap.UserEquipment.Default) \n
		Sets the offset from the SFN=0 after that the SL control region starts. \n
			:param offset_indicator: integer Range: 0 to 10239
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
		"""
		param = Conversions.decimal_value_to_str(offset_indicator)
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{userEquipment_cmd_val}:SL:RDATa:OFFSetind {param}')

	def get(self, userEquipment=repcap.UserEquipment.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:RDATa:OFFSetind \n
		Snippet: value: int = driver.source.bb.eutra.uplink.ue.sl.rdata.offsetInd.get(userEquipment = repcap.UserEquipment.Default) \n
		Sets the offset from the SFN=0 after that the SL control region starts. \n
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: offset_indicator: integer Range: 0 to 10239"""
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{userEquipment_cmd_val}:SL:RDATa:OFFSetind?')
		return Conversions.str_to_int(response)
