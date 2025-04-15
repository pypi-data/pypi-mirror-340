from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HoldCls:
	"""Hold commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hold", core, parent)

	def reset(self) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:OLOad:HOLD:RESet \n
		Snippet: driver.source.bbin.oload.hold.reset() \n
		Reset of the Overload Hold indication. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BBIN:OLOad:HOLD:RESet')

	def reset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:OLOad:HOLD:RESet \n
		Snippet: driver.source.bbin.oload.hold.reset_with_opc() \n
		Reset of the Overload Hold indication. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BBIN:OLOad:HOLD:RESet', opc_timeout_ms)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BBIN:OLOad:HOLD:STATe \n
		Snippet: value: bool = driver.source.bbin.oload.hold.get_state() \n
		Queries an overload since the last reset for evaluating the measurement. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:OLOad:HOLD:STATe?')
		return Conversions.str_to_bool(response)
