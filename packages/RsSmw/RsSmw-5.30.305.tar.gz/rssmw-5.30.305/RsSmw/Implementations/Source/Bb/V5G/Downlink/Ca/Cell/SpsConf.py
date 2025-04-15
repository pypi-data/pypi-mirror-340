from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpsConfCls:
	"""SpsConf commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("spsConf", core, parent)

	def set(self, dlc_atdd_ss_conf: float, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:CA:CELL<CH0>:SPSConf \n
		Snippet: driver.source.bb.v5G.downlink.ca.cell.spsConf.set(dlc_atdd_ss_conf = 1.0, cellNull = repcap.CellNull.Default) \n
		No command help available \n
			:param dlc_atdd_ss_conf: No help available
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(dlc_atdd_ss_conf)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:DL:CA:CELL{cellNull_cmd_val}:SPSConf {param}')

	def get(self, cellNull=repcap.CellNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:CA:CELL<CH0>:SPSConf \n
		Snippet: value: float = driver.source.bb.v5G.downlink.ca.cell.spsConf.get(cellNull = repcap.CellNull.Default) \n
		No command help available \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: dlc_atdd_ss_conf: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:V5G:DL:CA:CELL{cellNull_cmd_val}:SPSConf?')
		return Conversions.str_to_float(response)
