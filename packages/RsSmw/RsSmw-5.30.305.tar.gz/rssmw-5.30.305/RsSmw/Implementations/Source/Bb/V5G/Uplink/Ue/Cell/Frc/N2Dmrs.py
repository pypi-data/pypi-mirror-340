from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class N2DmrsCls:
	"""N2Dmrs commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("n2Dmrs", core, parent)

	def set(self, n_2_dmrs: int, userEquipment=repcap.UserEquipment.Default, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:UL:UE<ST>:[CELL<CCIDX>]:FRC:N2DMrs \n
		Snippet: driver.source.bb.v5G.uplink.ue.cell.frc.n2Dmrs.set(n_2_dmrs = 1, userEquipment = repcap.UserEquipment.Default, cellNull = repcap.CellNull.Default) \n
		No command help available \n
			:param n_2_dmrs: No help available
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(n_2_dmrs)
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:UL:UE{userEquipment_cmd_val}:CELL{cellNull_cmd_val}:FRC:N2DMrs {param}')

	def get(self, userEquipment=repcap.UserEquipment.Default, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:V5G:UL:UE<ST>:[CELL<CCIDX>]:FRC:N2DMrs \n
		Snippet: value: int = driver.source.bb.v5G.uplink.ue.cell.frc.n2Dmrs.get(userEquipment = repcap.UserEquipment.Default, cellNull = repcap.CellNull.Default) \n
		No command help available \n
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: n_2_dmrs: No help available"""
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:V5G:UL:UE{userEquipment_cmd_val}:CELL{cellNull_cmd_val}:FRC:N2DMrs?')
		return Conversions.str_to_int(response)
