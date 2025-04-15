from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RealCls:
	"""Real commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("real", core, parent)

	def set(self, real: float, mimoTap=repcap.MimoTap.Default, row=repcap.Row.Default, column=repcap.Column.Default) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:TAP<CH>:KRONecker:CORRelation:RX:ROW<DI>:COLumn<ST>:REAL \n
		Snippet: driver.source.cemulation.mimo.tap.kronecker.correlation.rx.row.column.real.set(real = 1.0, mimoTap = repcap.MimoTap.Default, row = repcap.Row.Default, column = repcap.Column.Default) \n
		No command help available \n
			:param real: No help available
			:param mimoTap: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tap')
			:param row: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:param column: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Column')
		"""
		param = Conversions.decimal_value_to_str(real)
		mimoTap_cmd_val = self._cmd_group.get_repcap_cmd_value(mimoTap, repcap.MimoTap)
		row_cmd_val = self._cmd_group.get_repcap_cmd_value(row, repcap.Row)
		column_cmd_val = self._cmd_group.get_repcap_cmd_value(column, repcap.Column)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MIMO:TAP{mimoTap_cmd_val}:KRONecker:CORRelation:RX:ROW{row_cmd_val}:COLumn{column_cmd_val}:REAL {param}')

	def get(self, mimoTap=repcap.MimoTap.Default, row=repcap.Row.Default, column=repcap.Column.Default) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:TAP<CH>:KRONecker:CORRelation:RX:ROW<DI>:COLumn<ST>:REAL \n
		Snippet: value: float = driver.source.cemulation.mimo.tap.kronecker.correlation.rx.row.column.real.get(mimoTap = repcap.MimoTap.Default, row = repcap.Row.Default, column = repcap.Column.Default) \n
		No command help available \n
			:param mimoTap: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tap')
			:param row: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:param column: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Column')
			:return: real: No help available"""
		mimoTap_cmd_val = self._cmd_group.get_repcap_cmd_value(mimoTap, repcap.MimoTap)
		row_cmd_val = self._cmd_group.get_repcap_cmd_value(row, repcap.Row)
		column_cmd_val = self._cmd_group.get_repcap_cmd_value(column, repcap.Column)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CEMulation:MIMO:TAP{mimoTap_cmd_val}:KRONecker:CORRelation:RX:ROW{row_cmd_val}:COLumn{column_cmd_val}:REAL?')
		return Conversions.str_to_float(response)
