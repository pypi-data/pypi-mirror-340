from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from .............Internal.RepeatedCapability import RepeatedCapability
from ............. import enums
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApSelectCls:
	"""ApSelect commands group definition. 1 total commands, 0 Subgroups, 1 group commands
	Repeated Capability: AntennaPortNull, default value after init: AntennaPortNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("apSelect", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_antennaPortNull_get', 'repcap_antennaPortNull_set', repcap.AntennaPortNull.Nr0)

	def repcap_antennaPortNull_set(self, antennaPortNull: repcap.AntennaPortNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AntennaPortNull.Default.
		Default value after init: AntennaPortNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(antennaPortNull)

	def repcap_antennaPortNull_get(self) -> repcap.AntennaPortNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	def set(self, pusch_ap_sel: enums.Nr5GpuschAp, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, userNull=repcap.UserNull.Default, bwPartNull=repcap.BwPartNull.Default, allocationNull=repcap.AllocationNull.Default, antennaPortNull=repcap.AntennaPortNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CC(CH0)>:SUBF<SF(ST0)>:USER<US(DIR0)>:BWPart<BWP(GR0)>:ALLoc<AL(USER0)>:PUSCh:[DMRS]:APSelect<S2US0> \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pusch.dmrs.apSelect.set(pusch_ap_sel = enums.Nr5GpuschAp.AP0, cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, userNull = repcap.UserNull.Default, bwPartNull = repcap.BwPartNull.Default, allocationNull = repcap.AllocationNull.Default, antennaPortNull = repcap.AntennaPortNull.Default) \n
		Each layer of a PUSCH allocation is mapped to a certain antenna port. By the command the antenna ports are selected which
		are used for the transmission of the PUSCH allocation. \n
			:param pusch_ap_sel: AP0| AP1| AP2| AP3| AP4| AP5| AP6| AP7| AP8| AP9| AP10| AP11
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:param antennaPortNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'ApSelect')
		"""
		param = Conversions.enum_scalar_to_str(pusch_ap_sel, enums.Nr5GpuschAp)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		antennaPortNull_cmd_val = self._cmd_group.get_repcap_cmd_value(antennaPortNull, repcap.AntennaPortNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:USER{userNull_cmd_val}:BWPart{bwPartNull_cmd_val}:ALLoc{allocationNull_cmd_val}:PUSCh:DMRS:APSelect{antennaPortNull_cmd_val} {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, userNull=repcap.UserNull.Default, bwPartNull=repcap.BwPartNull.Default, allocationNull=repcap.AllocationNull.Default, antennaPortNull=repcap.AntennaPortNull.Default) -> enums.Nr5GpuschAp:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CC(CH0)>:SUBF<SF(ST0)>:USER<US(DIR0)>:BWPart<BWP(GR0)>:ALLoc<AL(USER0)>:PUSCh:[DMRS]:APSelect<S2US0> \n
		Snippet: value: enums.Nr5GpuschAp = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pusch.dmrs.apSelect.get(cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, userNull = repcap.UserNull.Default, bwPartNull = repcap.BwPartNull.Default, allocationNull = repcap.AllocationNull.Default, antennaPortNull = repcap.AntennaPortNull.Default) \n
		Each layer of a PUSCH allocation is mapped to a certain antenna port. By the command the antenna ports are selected which
		are used for the transmission of the PUSCH allocation. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:param antennaPortNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'ApSelect')
			:return: pusch_ap_sel: AP0| AP1| AP2| AP3| AP4| AP5| AP6| AP7| AP8| AP9| AP10| AP11"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		antennaPortNull_cmd_val = self._cmd_group.get_repcap_cmd_value(antennaPortNull, repcap.AntennaPortNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:USER{userNull_cmd_val}:BWPart{bwPartNull_cmd_val}:ALLoc{allocationNull_cmd_val}:PUSCh:DMRS:APSelect{antennaPortNull_cmd_val}?')
		return Conversions.str_to_scalar_enum(response, enums.Nr5GpuschAp)

	def clone(self) -> 'ApSelectCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ApSelectCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
