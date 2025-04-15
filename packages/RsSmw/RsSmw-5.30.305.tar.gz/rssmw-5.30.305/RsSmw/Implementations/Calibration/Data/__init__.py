from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DataCls:
	"""Data commands group definition. 4 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("data", core, parent)

	@property
	def factory(self):
		"""factory commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_factory'):
			from .Factory import FactoryCls
			self._factory = FactoryCls(self._core, self._cmd_group)
		return self._factory

	@property
	def update(self):
		"""update commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_update'):
			from .Update import UpdateCls
			self._update = UpdateCls(self._core, self._cmd_group)
		return self._update

	def export(self) -> None:
		"""SCPI: CALibration:DATA:EXPort \n
		Snippet: driver.calibration.data.export() \n
		Collects the internal adjustment data and provides the data for export in a zip file. You can export the data for service
		and evaluation purposes. \n
		"""
		self._core.io.write(f'CALibration:DATA:EXPort')

	def export_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: CALibration:DATA:EXPort \n
		Snippet: driver.calibration.data.export_with_opc() \n
		Collects the internal adjustment data and provides the data for export in a zip file. You can export the data for service
		and evaluation purposes. \n
		Same as export, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'CALibration:DATA:EXPort', opc_timeout_ms)

	def clone(self) -> 'DataCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DataCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
