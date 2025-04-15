from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DistanceCls:
	"""Distance commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("distance", core, parent)

	def get_rx(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:TGN:ANTenna:DISTance:RX \n
		Snippet: value: float = driver.source.cemulation.mimo.tgn.antenna.distance.get_rx() \n
		No command help available \n
			:return: distance_rx: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:MIMO:TGN:ANTenna:DISTance:RX?')
		return Conversions.str_to_float(response)

	def set_rx(self, distance_rx: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:TGN:ANTenna:DISTance:RX \n
		Snippet: driver.source.cemulation.mimo.tgn.antenna.distance.set_rx(distance_rx = 1.0) \n
		No command help available \n
			:param distance_rx: No help available
		"""
		param = Conversions.decimal_value_to_str(distance_rx)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MIMO:TGN:ANTenna:DISTance:RX {param}')

	def get_tx(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:TGN:ANTenna:DISTance:TX \n
		Snippet: value: float = driver.source.cemulation.mimo.tgn.antenna.distance.get_tx() \n
		No command help available \n
			:return: distance_tx: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:MIMO:TGN:ANTenna:DISTance:TX?')
		return Conversions.str_to_float(response)

	def set_tx(self, distance_tx: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:TGN:ANTenna:DISTance:TX \n
		Snippet: driver.source.cemulation.mimo.tgn.antenna.distance.set_tx(distance_tx = 1.0) \n
		No command help available \n
			:param distance_tx: No help available
		"""
		param = Conversions.decimal_value_to_str(distance_tx)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MIMO:TGN:ANTenna:DISTance:TX {param}')
