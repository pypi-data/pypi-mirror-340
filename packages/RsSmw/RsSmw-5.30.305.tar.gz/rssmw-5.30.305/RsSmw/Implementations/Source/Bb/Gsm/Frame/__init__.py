from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrameCls:
	"""Frame commands group definition. 38 total commands, 5 Subgroups, 0 group commands
	Repeated Capability: FrameIx, default value after init: FrameIx.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frame", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_frameIx_get', 'repcap_frameIx_set', repcap.FrameIx.Nr1)

	def repcap_frameIx_set(self, frameIx: repcap.FrameIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to FrameIx.Default.
		Default value after init: FrameIx.Nr1"""
		self._cmd_group.set_repcap_enum_value(frameIx)

	def repcap_frameIx_get(self) -> repcap.FrameIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def repetitions(self):
		"""repetitions commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repetitions'):
			from .Repetitions import RepetitionsCls
			self._repetitions = RepetitionsCls(self._core, self._cmd_group)
		return self._repetitions

	@property
	def ulist(self):
		"""ulist commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_ulist'):
			from .Ulist import UlistCls
			self._ulist = UlistCls(self._core, self._cmd_group)
		return self._ulist

	@property
	def multiSlot(self):
		"""multiSlot commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_multiSlot'):
			from .MultiSlot import MultiSlotCls
			self._multiSlot = MultiSlotCls(self._core, self._cmd_group)
		return self._multiSlot

	@property
	def predefined(self):
		"""predefined commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_predefined'):
			from .Predefined import PredefinedCls
			self._predefined = PredefinedCls(self._core, self._cmd_group)
		return self._predefined

	@property
	def slot(self):
		"""slot commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_slot'):
			from .Slot import SlotCls
			self._slot = SlotCls(self._core, self._cmd_group)
		return self._slot

	def clone(self) -> 'FrameCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FrameCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
