from .................Internal.Core import Core
from .................Internal.CommandsGroup import CommandsGroup
from .................Internal.RepeatedCapability import RepeatedCapability
from ................. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RowCls:
	"""Row commands group definition. 4 total commands, 4 Subgroups, 0 group commands
	Repeated Capability: RowNull, default value after init: RowNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("row", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_rowNull_get', 'repcap_rowNull_set', repcap.RowNull.Nr0)

	def repcap_rowNull_set(self, rowNull: repcap.RowNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to RowNull.Default.
		Default value after init: RowNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(rowNull)

	def repcap_rowNull_get(self) -> repcap.RowNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def imaginary(self):
		"""imaginary commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_imaginary'):
			from .Imaginary import ImaginaryCls
			self._imaginary = ImaginaryCls(self._core, self._cmd_group)
		return self._imaginary

	@property
	def magnitude(self):
		"""magnitude commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_magnitude'):
			from .Magnitude import MagnitudeCls
			self._magnitude = MagnitudeCls(self._core, self._cmd_group)
		return self._magnitude

	@property
	def phase(self):
		"""phase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_phase'):
			from .Phase import PhaseCls
			self._phase = PhaseCls(self._core, self._cmd_group)
		return self._phase

	@property
	def real(self):
		"""real commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_real'):
			from .Real import RealCls
			self._real = RealCls(self._core, self._cmd_group)
		return self._real

	def clone(self) -> 'RowCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RowCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
