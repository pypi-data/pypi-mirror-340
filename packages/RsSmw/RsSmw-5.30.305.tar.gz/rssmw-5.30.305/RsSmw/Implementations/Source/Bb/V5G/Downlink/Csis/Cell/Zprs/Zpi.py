from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Utilities import trim_str_response
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ZpiCls:
	"""Zpi commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("zpi", core, parent)

	def set(self, zero_pow_conf: str, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:CSIS:[CELL<CH0>]:[ZPRS<ST0>]:ZPI \n
		Snippet: driver.source.bb.v5G.downlink.csis.cell.zprs.zpi.set(zero_pow_conf = rawAbc, cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		No command help available \n
			:param zero_pow_conf: No help available
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Zprs')
		"""
		param = Conversions.value_to_str(zero_pow_conf)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:DL:CSIS:CELL{cellNull_cmd_val}:ZPRS{indexNull_cmd_val}:ZPI {param}')

	def get(self, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:CSIS:[CELL<CH0>]:[ZPRS<ST0>]:ZPI \n
		Snippet: value: str = driver.source.bb.v5G.downlink.csis.cell.zprs.zpi.get(cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		No command help available \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Zprs')
			:return: zero_pow_conf: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:V5G:DL:CSIS:CELL{cellNull_cmd_val}:ZPRS{indexNull_cmd_val}:ZPI?')
		return trim_str_response(response)
