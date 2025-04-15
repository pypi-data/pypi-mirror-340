from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BwCls:
	"""Bw commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bw", core, parent)

	def set(self, bandwidth: enums.EutraCaChannelBandwidth, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:CA:CELL<CH0>:BW \n
		Snippet: driver.source.bb.eutra.downlink.ca.cell.bw.set(bandwidth = enums.EutraCaChannelBandwidth.BW1_40, cellNull = repcap.CellNull.Default) \n
		Sets the bandwidth of the corresponding component carrier/SCell. \n
			:param bandwidth: BW1_40| BW3_00| BW5_00| BW10_00| BW15_00| BW20_00
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.enum_scalar_to_str(bandwidth, enums.EutraCaChannelBandwidth)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CA:CELL{cellNull_cmd_val}:BW {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default) -> enums.EutraCaChannelBandwidth:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:CA:CELL<CH0>:BW \n
		Snippet: value: enums.EutraCaChannelBandwidth = driver.source.bb.eutra.downlink.ca.cell.bw.get(cellNull = repcap.CellNull.Default) \n
		Sets the bandwidth of the corresponding component carrier/SCell. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: bandwidth: BW1_40| BW3_00| BW5_00| BW10_00| BW15_00| BW20_00"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CA:CELL{cellNull_cmd_val}:BW?')
		return Conversions.str_to_scalar_enum(response, enums.EutraCaChannelBandwidth)
