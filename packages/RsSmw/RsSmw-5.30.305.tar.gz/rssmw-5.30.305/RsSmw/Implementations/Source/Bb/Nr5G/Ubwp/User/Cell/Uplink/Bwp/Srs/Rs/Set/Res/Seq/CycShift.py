from ...............Internal.Core import Core
from ...............Internal.CommandsGroup import CommandsGroup
from ...............Internal import Conversions
from ............... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CycShiftCls:
	"""CycShift commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cycShift", core, parent)

	def get(self, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default, resourceSetNull=repcap.ResourceSetNull.Default, resourceNull=repcap.ResourceNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:CELL<CC(ST0)>:UL:BWP<BWP(DIR0)>:SRS:RS:SET<GR0>:RES<USER0>:SEQ:CYCShift \n
		Snippet: value: float = driver.source.bb.nr5G.ubwp.user.cell.uplink.bwp.srs.rs.set.res.seq.cycShift.get(userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default, resourceSetNull = repcap.ResourceSetNull.Default, resourceNull = repcap.ResourceNull.Default) \n
		Sets the number of cyclic shifts, required for the SRS sequence generation. \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param resourceSetNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Set')
			:param resourceNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')
			:return: srs_rs_cyclic_shif: float Range: 0 to 11"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		resourceSetNull_cmd_val = self._cmd_group.get_repcap_cmd_value(resourceSetNull, repcap.ResourceSetNull)
		resourceNull_cmd_val = self._cmd_group.get_repcap_cmd_value(resourceNull, repcap.ResourceNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:UL:BWP{bwPartNull_cmd_val}:SRS:RS:SET{resourceSetNull_cmd_val}:RES{resourceNull_cmd_val}:SEQ:CYCShift?')
		return Conversions.str_to_float(response)
