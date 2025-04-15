from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AlignCls:
	"""Align commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("align", core, parent)

	def set(self) -> None:
		"""SCPI: SCONfiguration:RFALignment:ALIGn \n
		Snippet: driver.sconfiguration.rfAlignment.align.set() \n
		If a valid setup is loaded and RF ports alignment is enabled, sends the multi instrument trigger signal to all
		instruments to synchronize the basebands of the instruments. \n
		"""
		self._core.io.write(f'SCONfiguration:RFALignment:ALIGn')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SCONfiguration:RFALignment:ALIGn \n
		Snippet: driver.sconfiguration.rfAlignment.align.set_with_opc() \n
		If a valid setup is loaded and RF ports alignment is enabled, sends the multi instrument trigger signal to all
		instruments to synchronize the basebands of the instruments. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SCONfiguration:RFALignment:ALIGn', opc_timeout_ms)
