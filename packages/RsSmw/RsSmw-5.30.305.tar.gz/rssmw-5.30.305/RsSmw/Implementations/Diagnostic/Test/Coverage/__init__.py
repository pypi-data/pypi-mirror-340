from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CoverageCls:
	"""Coverage commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("coverage", core, parent)

	@property
	def dump(self):
		"""dump commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dump'):
			from .Dump import DumpCls
			self._dump = DumpCls(self._core, self._cmd_group)
		return self._dump

	def reset(self) -> None:
		"""SCPI: DIAGnostic<HW>:TEST:COVerage:RESet \n
		Snippet: driver.diagnostic.test.coverage.reset() \n
		No command help available \n
		"""
		self._core.io.write(f'DIAGnostic<HwInstance>:TEST:COVerage:RESet')

	def reset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: DIAGnostic<HW>:TEST:COVerage:RESet \n
		Snippet: driver.diagnostic.test.coverage.reset_with_opc() \n
		No command help available \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'DIAGnostic<HwInstance>:TEST:COVerage:RESet', opc_timeout_ms)

	def clone(self) -> 'CoverageCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CoverageCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
