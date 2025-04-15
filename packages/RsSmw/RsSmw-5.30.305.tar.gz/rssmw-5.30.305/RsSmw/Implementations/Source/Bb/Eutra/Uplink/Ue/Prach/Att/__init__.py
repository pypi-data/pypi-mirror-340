from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AttCls:
	"""Att commands group definition. 13 total commands, 2 Subgroups, 0 group commands
	Repeated Capability: AttenuationNull, default value after init: AttenuationNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("att", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_attenuationNull_get', 'repcap_attenuationNull_set', repcap.AttenuationNull.Nr0)

	def repcap_attenuationNull_set(self, attenuationNull: repcap.AttenuationNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AttenuationNull.Default.
		Default value after init: AttenuationNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(attenuationNull)

	def repcap_attenuationNull_get(self) -> repcap.AttenuationNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def emtc(self):
		"""emtc commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_emtc'):
			from .Emtc import EmtcCls
			self._emtc = EmtcCls(self._core, self._cmd_group)
		return self._emtc

	@property
	def niot(self):
		"""niot commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_niot'):
			from .Niot import NiotCls
			self._niot = NiotCls(self._core, self._cmd_group)
		return self._niot

	def clone(self) -> 'AttCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AttCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
