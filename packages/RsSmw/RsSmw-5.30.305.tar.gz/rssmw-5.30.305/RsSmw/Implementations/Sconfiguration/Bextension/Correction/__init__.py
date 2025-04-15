from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CorrectionCls:
	"""Correction commands group definition. 7 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("correction", core, parent)

	@property
	def port(self):
		"""port commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_port'):
			from .Port import PortCls
			self._port = PortCls(self._core, self._cmd_group)
		return self._port

	def reset(self) -> None:
		"""SCPI: SCONfiguration:BEXTension:CORRection:RESet \n
		Snippet: driver.sconfiguration.bextension.correction.reset() \n
		Resets all previous RF ports user-defined correction settings. \n
		"""
		self._core.io.write(f'SCONfiguration:BEXTension:CORRection:RESet')

	def reset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SCONfiguration:BEXTension:CORRection:RESet \n
		Snippet: driver.sconfiguration.bextension.correction.reset_with_opc() \n
		Resets all previous RF ports user-defined correction settings. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SCONfiguration:BEXTension:CORRection:RESet', opc_timeout_ms)

	def clone(self) -> 'CorrectionCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CorrectionCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
