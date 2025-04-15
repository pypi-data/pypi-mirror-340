from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AllCls:
	"""All commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("all", core, parent)

	def set(self) -> None:
		"""SCPI: SCONfiguration:EXTernal:REMote:DISConnect:[ALL] \n
		Snippet: driver.sconfiguration.external.remote.disconnect.all.set() \n
		Triggers the instrument to establish the connections to all configured external instruments or to disconnect all existing
		connections. \n
		"""
		self._core.io.write(f'SCONfiguration:EXTernal:REMote:DISConnect:ALL')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SCONfiguration:EXTernal:REMote:DISConnect:[ALL] \n
		Snippet: driver.sconfiguration.external.remote.disconnect.all.set_with_opc() \n
		Triggers the instrument to establish the connections to all configured external instruments or to disconnect all existing
		connections. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SCONfiguration:EXTernal:REMote:DISConnect:ALL', opc_timeout_ms)
