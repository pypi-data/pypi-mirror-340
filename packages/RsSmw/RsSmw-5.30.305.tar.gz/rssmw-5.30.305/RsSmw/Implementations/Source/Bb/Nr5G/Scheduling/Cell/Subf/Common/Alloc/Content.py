from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ContentCls:
	"""Content commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("content", core, parent)

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, allocationNull=repcap.AllocationNull.Default) -> enums.Nr5GcomContent:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CC(CH0)>:SUBF<SF(ST0)>:COMMon:ALLoc<AL(DIR0)>:CONTent \n
		Snippet: value: enums.Nr5GcomContent = driver.source.bb.nr5G.scheduling.cell.subf.common.alloc.content.get(cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Selects the allocation type. Note that the available parameters for this set of commands depends on the allocation you
		want to configure. For example, you can only configure puncturing allocations in the common allocations. Therefore, the
		setting command for common allocations only supports the PUNCturing parameter. Likewise, the commands to configure or
		query user allocation only support the parameters that represent user allocations (e.g. PDSCh, COREset etc.
		) For an overview of all allocation types and their availability, see 'Content'. Note that some allocation types require
		a specific firmware option. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: rep_com_alloc_cont: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:COMMon:ALLoc{allocationNull_cmd_val}:CONTent?')
		return Conversions.str_to_scalar_enum(response, enums.Nr5GcomContent)
