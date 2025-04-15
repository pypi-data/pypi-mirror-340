from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SecurityCls:
	"""Security commands group definition. 18 total commands, 6 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("security", core, parent)

	@property
	def mmem(self):
		"""mmem commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mmem'):
			from .Mmem import MmemCls
			self._mmem = MmemCls(self._core, self._cmd_group)
		return self._mmem

	@property
	def network(self):
		"""network commands group. 12 Sub-classes, 0 commands."""
		if not hasattr(self, '_network'):
			from .Network import NetworkCls
			self._network = NetworkCls(self._core, self._cmd_group)
		return self._network

	@property
	def sanitize(self):
		"""sanitize commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sanitize'):
			from .Sanitize import SanitizeCls
			self._sanitize = SanitizeCls(self._core, self._cmd_group)
		return self._sanitize

	@property
	def suPolicy(self):
		"""suPolicy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_suPolicy'):
			from .SuPolicy import SuPolicyCls
			self._suPolicy = SuPolicyCls(self._core, self._cmd_group)
		return self._suPolicy

	@property
	def usbStorage(self):
		"""usbStorage commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_usbStorage'):
			from .UsbStorage import UsbStorageCls
			self._usbStorage = UsbStorageCls(self._core, self._cmd_group)
		return self._usbStorage

	@property
	def volMode(self):
		"""volMode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_volMode'):
			from .VolMode import VolModeCls
			self._volMode = VolModeCls(self._core, self._cmd_group)
		return self._volMode

	def get_state(self) -> bool:
		"""SCPI: SYSTem:SECurity:[STATe] \n
		Snippet: value: bool = driver.system.security.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SYSTem:SECurity:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: SYSTem:SECurity:[STATe] \n
		Snippet: driver.system.security.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SYSTem:SECurity:STATe {param}')

	def clone(self) -> 'SecurityCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SecurityCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
