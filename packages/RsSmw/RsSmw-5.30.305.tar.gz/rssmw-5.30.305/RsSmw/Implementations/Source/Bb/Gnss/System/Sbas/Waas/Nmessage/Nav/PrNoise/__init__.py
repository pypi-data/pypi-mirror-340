from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal.RepeatedCapability import RepeatedCapability
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PrNoiseCls:
	"""PrNoise commands group definition. 1 total commands, 1 Subgroups, 0 group commands
	Repeated Capability: GnssPsRandomNumberNull, default value after init: GnssPsRandomNumberNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("prNoise", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_gnssPsRandomNumberNull_get', 'repcap_gnssPsRandomNumberNull_set', repcap.GnssPsRandomNumberNull.Nr0)

	def repcap_gnssPsRandomNumberNull_set(self, gnssPsRandomNumberNull: repcap.GnssPsRandomNumberNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to GnssPsRandomNumberNull.Default.
		Default value after init: GnssPsRandomNumberNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(gnssPsRandomNumberNull)

	def repcap_gnssPsRandomNumberNull_get(self) -> repcap.GnssPsRandomNumberNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'PrNoiseCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PrNoiseCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
