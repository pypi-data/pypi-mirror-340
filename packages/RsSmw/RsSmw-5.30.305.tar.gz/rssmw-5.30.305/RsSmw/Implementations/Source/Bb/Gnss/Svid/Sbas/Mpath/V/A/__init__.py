from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ACls:
	"""A commands group definition. 16 total commands, 3 Subgroups, 0 group commands
	Repeated Capability: Antenna, default value after init: Antenna.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("a", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_antenna_get', 'repcap_antenna_set', repcap.Antenna.Nr1)

	def repcap_antenna_set(self, antenna: repcap.Antenna) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Antenna.Default.
		Default value after init: Antenna.Nr1"""
		self._cmd_group.set_repcap_enum_value(antenna)

	def repcap_antenna_get(self) -> repcap.Antenna:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def echo(self):
		"""echo commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_echo'):
			from .Echo import EchoCls
			self._echo = EchoCls(self._core, self._cmd_group)
		return self._echo

	@property
	def echos(self):
		"""echos commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_echos'):
			from .Echos import EchosCls
			self._echos = EchosCls(self._core, self._cmd_group)
		return self._echos

	@property
	def los(self):
		"""los commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_los'):
			from .Los import LosCls
			self._los = LosCls(self._core, self._cmd_group)
		return self._los

	def clone(self) -> 'ACls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ACls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
