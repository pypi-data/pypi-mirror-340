from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UpdateCls:
	"""Update commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("update", core, parent)

	@property
	def needed(self):
		"""needed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_needed'):
			from .Needed import NeededCls
			self._needed = NeededCls(self._core, self._cmd_group)
		return self._needed

	def set(self) -> None:
		"""SCPI: SYSTem:PCIFpga:UPDate \n
		Snippet: driver.system.pciFpga.update.set() \n
		No command help available \n
		"""
		self._core.io.write(f'SYSTem:PCIFpga:UPDate')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SYSTem:PCIFpga:UPDate \n
		Snippet: driver.system.pciFpga.update.set_with_opc() \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SYSTem:PCIFpga:UPDate', opc_timeout_ms)

	def clone(self) -> 'UpdateCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UpdateCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
