from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModulationCls:
	"""Modulation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("modulation", core, parent)

	# noinspection PyTypeChecker
	def get(self, userEquipment=repcap.UserEquipment.Default, cellNull=repcap.CellNull.Default) -> enums.ModulationB:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:FRC:MODulation \n
		Snippet: value: enums.ModulationB = driver.source.bb.eutra.uplink.ue.cell.frc.modulation.get(userEquipment = repcap.UserEquipment.Default, cellNull = repcap.CellNull.Default) \n
		Queries the modulation for the selected FRC ([:SOURce<hw>]:BB:EUTRa:UL:UE<st>[:CELL<ccidx>]:FRC:TYPE) . \n
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: modulation: QPSK| QAM16| QAM64| QAM256"""
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{userEquipment_cmd_val}:CELL{cellNull_cmd_val}:FRC:MODulation?')
		return Conversions.str_to_scalar_enum(response, enums.ModulationB)
