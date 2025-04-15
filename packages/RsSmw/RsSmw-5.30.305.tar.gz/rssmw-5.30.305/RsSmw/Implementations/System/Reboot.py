from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RebootCls:
	"""Reboot commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("reboot", core, parent)

	def set(self) -> None:
		"""SCPI: SYSTem:REBoot \n
		Snippet: driver.system.reboot.set() \n
		Reboots the instrument including the operating system. \n
		"""
		self._core.io.write(f'SYSTem:REBoot')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SYSTem:REBoot \n
		Snippet: driver.system.reboot.set_with_opc() \n
		Reboots the instrument including the operating system. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SYSTem:REBoot', opc_timeout_ms)
