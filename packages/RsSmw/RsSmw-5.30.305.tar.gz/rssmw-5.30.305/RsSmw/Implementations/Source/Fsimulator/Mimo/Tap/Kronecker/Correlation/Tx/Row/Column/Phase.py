from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PhaseCls:
	"""Phase commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("phase", core, parent)

	def set(self, phase: float, mimoTap=repcap.MimoTap.Default, row=repcap.Row.Default, column=repcap.Column.Default) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:MIMO:TAP<CH>:KRONecker:CORRelation:TX:ROW<DI>:COLumn<ST>:PHASe \n
		Snippet: driver.source.fsimulator.mimo.tap.kronecker.correlation.tx.row.column.phase.set(phase = 1.0, mimoTap = repcap.MimoTap.Default, row = repcap.Row.Default, column = repcap.Column.Default) \n
		Sets the value for the phase of the receiver/transmitter correlation. Note: If the values for the real part and the
		imaginary part are both set to 0, the phase value is set to 0 when changing the data format. \n
			:param phase: float Range: 0 to 360
			:param mimoTap: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tap')
			:param row: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:param column: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Column')
		"""
		param = Conversions.decimal_value_to_str(phase)
		mimoTap_cmd_val = self._cmd_group.get_repcap_cmd_value(mimoTap, repcap.MimoTap)
		row_cmd_val = self._cmd_group.get_repcap_cmd_value(row, repcap.Row)
		column_cmd_val = self._cmd_group.get_repcap_cmd_value(column, repcap.Column)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:MIMO:TAP{mimoTap_cmd_val}:KRONecker:CORRelation:TX:ROW{row_cmd_val}:COLumn{column_cmd_val}:PHASe {param}')

	def get(self, mimoTap=repcap.MimoTap.Default, row=repcap.Row.Default, column=repcap.Column.Default) -> float:
		"""SCPI: [SOURce<HW>]:FSIMulator:MIMO:TAP<CH>:KRONecker:CORRelation:TX:ROW<DI>:COLumn<ST>:PHASe \n
		Snippet: value: float = driver.source.fsimulator.mimo.tap.kronecker.correlation.tx.row.column.phase.get(mimoTap = repcap.MimoTap.Default, row = repcap.Row.Default, column = repcap.Column.Default) \n
		Sets the value for the phase of the receiver/transmitter correlation. Note: If the values for the real part and the
		imaginary part are both set to 0, the phase value is set to 0 when changing the data format. \n
			:param mimoTap: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tap')
			:param row: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:param column: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Column')
			:return: phase: float Range: 0 to 360"""
		mimoTap_cmd_val = self._cmd_group.get_repcap_cmd_value(mimoTap, repcap.MimoTap)
		row_cmd_val = self._cmd_group.get_repcap_cmd_value(row, repcap.Row)
		column_cmd_val = self._cmd_group.get_repcap_cmd_value(column, repcap.Column)
		response = self._core.io.query_str(f'SOURce<HwInstance>:FSIMulator:MIMO:TAP{mimoTap_cmd_val}:KRONecker:CORRelation:TX:ROW{row_cmd_val}:COLumn{column_cmd_val}:PHASe?')
		return Conversions.str_to_float(response)
