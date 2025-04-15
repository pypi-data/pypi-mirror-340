from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SyncCls:
	"""Sync commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sync", core, parent)

	def get_ppower(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:SYNC:PPOWer \n
		Snippet: value: float = driver.source.bb.oneweb.downlink.sync.get_ppower() \n
		Sets the power of the primary synchronization signal (P-SYNC) . \n
			:return: ppower: float Range: -80 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:DL:SYNC:PPOWer?')
		return Conversions.str_to_float(response)

	def set_ppower(self, ppower: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:SYNC:PPOWer \n
		Snippet: driver.source.bb.oneweb.downlink.sync.set_ppower(ppower = 1.0) \n
		Sets the power of the primary synchronization signal (P-SYNC) . \n
			:param ppower: float Range: -80 to 10
		"""
		param = Conversions.decimal_value_to_str(ppower)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:DL:SYNC:PPOWer {param}')

	def get_pstate(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:SYNC:PSTate \n
		Snippet: value: bool = driver.source.bb.oneweb.downlink.sync.get_pstate() \n
		Sets the P-SYNC signal transmission state. \n
			:return: psync_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:DL:SYNC:PSTate?')
		return Conversions.str_to_bool(response)

	def set_pstate(self, psync_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:SYNC:PSTate \n
		Snippet: driver.source.bb.oneweb.downlink.sync.set_pstate(psync_state = False) \n
		Sets the P-SYNC signal transmission state. \n
			:param psync_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(psync_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:DL:SYNC:PSTate {param}')

	# noinspection PyTypeChecker
	def get_tx_antenna(self) -> enums.TxAntennaGnss:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:SYNC:TXANtenna \n
		Snippet: value: enums.TxAntennaGnss = driver.source.bb.oneweb.downlink.sync.get_tx_antenna() \n
		No command help available \n
			:return: tx_antenna: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:DL:SYNC:TXANtenna?')
		return Conversions.str_to_scalar_enum(response, enums.TxAntennaGnss)

	def set_tx_antenna(self, tx_antenna: enums.TxAntennaGnss) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:SYNC:TXANtenna \n
		Snippet: driver.source.bb.oneweb.downlink.sync.set_tx_antenna(tx_antenna = enums.TxAntennaGnss.ALL) \n
		No command help available \n
			:param tx_antenna: No help available
		"""
		param = Conversions.enum_scalar_to_str(tx_antenna, enums.TxAntennaGnss)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:DL:SYNC:TXANtenna {param}')
