from ................Internal.Core import Core
from ................Internal.CommandsGroup import CommandsGroup
from ................Internal.RepeatedCapability import RepeatedCapability
from ................ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApCls:
	"""Ap commands group definition. 4 total commands, 1 Subgroups, 0 group commands
	Repeated Capability: AccessPointNull, default value after init: AccessPointNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ap", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_accessPointNull_get', 'repcap_accessPointNull_set', repcap.AccessPointNull.Nr0)

	def repcap_accessPointNull_set(self, accessPointNull: repcap.AccessPointNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AccessPointNull.Default.
		Default value after init: AccessPointNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(accessPointNull)

	def repcap_accessPointNull_get(self) -> repcap.AccessPointNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def row(self):
		"""row commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_row'):
			from .Row import RowCls
			self._row = RowCls(self._core, self._cmd_group)
		return self._row

	def clone(self) -> 'ApCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ApCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
