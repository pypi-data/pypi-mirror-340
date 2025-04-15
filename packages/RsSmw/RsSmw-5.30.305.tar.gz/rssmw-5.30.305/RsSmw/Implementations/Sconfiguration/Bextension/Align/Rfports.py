from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfportsCls:
	"""Rfports commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rfports", core, parent)

	def set(self) -> None:
		"""SCPI: SCONfiguration:BEXTension:ALIGn:RFPorts \n
		Snippet: driver.sconfiguration.bextension.align.rfports.set() \n
		Requires an active measurement device. Triggers alignment of the RF ports and considers phase corrections. If you use an
		analyzer as a measurement device, RF ports alignment also considers cable length corrections. \n
		"""
		self._core.io.write(f'SCONfiguration:BEXTension:ALIGn:RFPorts')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SCONfiguration:BEXTension:ALIGn:RFPorts \n
		Snippet: driver.sconfiguration.bextension.align.rfports.set_with_opc() \n
		Requires an active measurement device. Triggers alignment of the RF ports and considers phase corrections. If you use an
		analyzer as a measurement device, RF ports alignment also considers cable length corrections. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SCONfiguration:BEXTension:ALIGn:RFPorts', opc_timeout_ms)

	def get_state(self) -> bool:
		"""SCPI: SCONfiguration:BEXTension:ALIGn:RFPorts:STATe \n
		Snippet: value: bool = driver.sconfiguration.bextension.align.rfports.get_state() \n
		No command help available \n
			:return: align_state: No help available
		"""
		response = self._core.io.query_str('SCONfiguration:BEXTension:ALIGn:RFPorts:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, align_state: bool) -> None:
		"""SCPI: SCONfiguration:BEXTension:ALIGn:RFPorts:STATe \n
		Snippet: driver.sconfiguration.bextension.align.rfports.set_state(align_state = False) \n
		No command help available \n
			:param align_state: No help available
		"""
		param = Conversions.bool_to_str(align_state)
		self._core.io.write(f'SCONfiguration:BEXTension:ALIGn:RFPorts:STATe {param}')
