from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RowCls:
	"""Row commands group definition. 1 total commands, 0 Subgroups, 1 group commands
	Repeated Capability: RowNull, default value after init: RowNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("row", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_rowNull_get', 'repcap_rowNull_set', repcap.RowNull.Nr0)

	def repcap_rowNull_set(self, rowNull: repcap.RowNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to RowNull.Default.
		Default value after init: RowNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(rowNull)

	def repcap_rowNull_get(self) -> repcap.RowNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	def set(self, map_cell_sel: bool, carrierNull=repcap.CarrierNull.Default, rowNull=repcap.RowNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CARMapping:CARRier<ST0>:[ROW<APR(CH0)>] \n
		Snippet: driver.source.bb.nr5G.node.carMapping.carrier.row.set(map_cell_sel = False, carrierNull = repcap.CarrierNull.Default, rowNull = repcap.RowNull.Default) \n
		Maps the NR 5G carriers to certain baseband outputs. \n
			:param map_cell_sel: 1| ON| 0| OFF ON | 1 Carrier st0 is mapped to baseband output ch0. OFF | 0 Carrier st0 is not mapped to baseband output ch0.
			:param carrierNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Carrier')
			:param rowNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')
		"""
		param = Conversions.bool_to_str(map_cell_sel)
		carrierNull_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierNull, repcap.CarrierNull)
		rowNull_cmd_val = self._cmd_group.get_repcap_cmd_value(rowNull, repcap.RowNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CARMapping:CARRier{carrierNull_cmd_val}:ROW{rowNull_cmd_val} {param}')

	def get(self, carrierNull=repcap.CarrierNull.Default, rowNull=repcap.RowNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CARMapping:CARRier<ST0>:[ROW<APR(CH0)>] \n
		Snippet: value: bool = driver.source.bb.nr5G.node.carMapping.carrier.row.get(carrierNull = repcap.CarrierNull.Default, rowNull = repcap.RowNull.Default) \n
		Maps the NR 5G carriers to certain baseband outputs. \n
			:param carrierNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Carrier')
			:param rowNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')
			:return: map_cell_sel: 1| ON| 0| OFF ON | 1 Carrier st0 is mapped to baseband output ch0. OFF | 0 Carrier st0 is not mapped to baseband output ch0."""
		carrierNull_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierNull, repcap.CarrierNull)
		rowNull_cmd_val = self._cmd_group.get_repcap_cmd_value(rowNull, repcap.RowNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CARMapping:CARRier{carrierNull_cmd_val}:ROW{rowNull_cmd_val}?')
		return Conversions.str_to_bool(response)

	def clone(self) -> 'RowCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RowCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
