from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OutputCls:
	"""Output commands group definition. 14 total commands, 10 Subgroups, 0 group commands
	Repeated Capability: Output, default value after init: Output.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("output", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_output_get', 'repcap_output_set', repcap.Output.Nr1)

	def repcap_output_set(self, output: repcap.Output) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Output.Default.
		Default value after init: Output.Nr1"""
		self._cmd_group.set_repcap_enum_value(output)

	def repcap_output_get(self) -> repcap.Output:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def delay(self):
		"""delay commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_delay'):
			from .Delay import DelayCls
			self._delay = DelayCls(self._core, self._cmd_group)
		return self._delay

	@property
	def fbIndex(self):
		"""fbIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fbIndex'):
			from .FbIndex import FbIndexCls
			self._fbIndex = FbIndexCls(self._core, self._cmd_group)
		return self._fbIndex

	@property
	def feShift(self):
		"""feShift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_feShift'):
			from .FeShift import FeShiftCls
			self._feShift = FeShiftCls(self._core, self._cmd_group)
		return self._feShift

	@property
	def findex(self):
		"""findex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_findex'):
			from .Findex import FindexCls
			self._findex = FindexCls(self._core, self._cmd_group)
		return self._findex

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def offTime(self):
		"""offTime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offTime'):
			from .OffTime import OffTimeCls
			self._offTime = OffTimeCls(self._core, self._cmd_group)
		return self._offTime

	@property
	def ontime(self):
		"""ontime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ontime'):
			from .Ontime import OntimeCls
			self._ontime = OntimeCls(self._core, self._cmd_group)
		return self._ontime

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	@property
	def pulse(self):
		"""pulse commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pulse'):
			from .Pulse import PulseCls
			self._pulse = PulseCls(self._core, self._cmd_group)
		return self._pulse

	@property
	def reShift(self):
		"""reShift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reShift'):
			from .ReShift import ReShiftCls
			self._reShift = ReShiftCls(self._core, self._cmd_group)
		return self._reShift

	def clone(self) -> 'OutputCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OutputCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
