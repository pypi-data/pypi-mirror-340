from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConnectionCls:
	"""Connection commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("connection", core, parent)

	@property
	def config(self):
		"""config commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_config'):
			from .Config import ConfigCls
			self._config = ConfigCls(self._core, self._cmd_group)
		return self._config

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:EFRontend:CONNection:STATe \n
		Snippet: value: bool = driver.source.efrontend.connection.get_state() \n
		Queries the state of the connection between R&S SMW200A and external frontend. \n
			:return: conn_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:CONNection:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, conn_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:EFRontend:CONNection:STATe \n
		Snippet: driver.source.efrontend.connection.set_state(conn_state = False) \n
		Queries the state of the connection between R&S SMW200A and external frontend. \n
			:param conn_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(conn_state)
		self._core.io.write(f'SOURce<HwInstance>:EFRontend:CONNection:STATe {param}')

	def clone(self) -> 'ConnectionCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ConnectionCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
