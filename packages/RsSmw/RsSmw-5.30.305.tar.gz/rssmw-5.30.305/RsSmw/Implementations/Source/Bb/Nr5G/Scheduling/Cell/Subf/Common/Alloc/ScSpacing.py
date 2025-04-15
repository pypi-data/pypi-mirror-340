from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScSpacingCls:
	"""ScSpacing commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scSpacing", core, parent)

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, allocationNull=repcap.AllocationNull.Default) -> enums.Numerology:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CC(CH0)>:SUBF<SF(ST0)>:COMMon:ALLoc<AL(DIR0)>:SCSPacing \n
		Snippet: value: enums.Numerology = driver.source.bb.nr5G.scheduling.cell.subf.common.alloc.scSpacing.get(cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Defines the subcarrier spacing for the selected allocation.
			INTRO_CMD_HELP: To define the subcarrier spacings for the complete bandwidth part and thus its user allocations in the various link directions, use the following commands: \n
			- Downlink: [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:DL:BWP<bwp>:SCSPacing
			- Uplink: [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:UL:BWP<bwp>:SCSPacing
			- Sidelink: [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:SL:BWP<bwp>:SCSPacing \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: rep_com_alloc_num: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:COMMon:ALLoc{allocationNull_cmd_val}:SCSPacing?')
		return Conversions.str_to_scalar_enum(response, enums.Numerology)
