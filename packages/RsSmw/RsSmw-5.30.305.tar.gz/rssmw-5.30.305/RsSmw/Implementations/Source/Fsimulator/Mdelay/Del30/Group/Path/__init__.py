from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PathCls:
	"""Path commands group definition. 11 total commands, 10 Subgroups, 0 group commands
	Repeated Capability: Path, default value after init: Path.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("path", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_path_get', 'repcap_path_set', repcap.Path.Nr1)

	def repcap_path_set(self, path: repcap.Path) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Path.Default.
		Default value after init: Path.Nr1"""
		self._cmd_group.set_repcap_enum_value(path)

	def repcap_path_get(self) -> repcap.Path:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def adelay(self):
		"""adelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adelay'):
			from .Adelay import AdelayCls
			self._adelay = AdelayCls(self._core, self._cmd_group)
		return self._adelay

	@property
	def bdelay(self):
		"""bdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bdelay'):
			from .Bdelay import BdelayCls
			self._bdelay = BdelayCls(self._core, self._cmd_group)
		return self._bdelay

	@property
	def cphase(self):
		"""cphase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cphase'):
			from .Cphase import CphaseCls
			self._cphase = CphaseCls(self._core, self._cmd_group)
		return self._cphase

	@property
	def fdoppler(self):
		"""fdoppler commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_fdoppler'):
			from .Fdoppler import FdopplerCls
			self._fdoppler = FdopplerCls(self._core, self._cmd_group)
		return self._fdoppler

	@property
	def fratio(self):
		"""fratio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fratio'):
			from .Fratio import FratioCls
			self._fratio = FratioCls(self._core, self._cmd_group)
		return self._fratio

	@property
	def loss(self):
		"""loss commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_loss'):
			from .Loss import LossCls
			self._loss = LossCls(self._core, self._cmd_group)
		return self._loss

	@property
	def profile(self):
		"""profile commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_profile'):
			from .Profile import ProfileCls
			self._profile = ProfileCls(self._core, self._cmd_group)
		return self._profile

	@property
	def rdelay(self):
		"""rdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rdelay'):
			from .Rdelay import RdelayCls
			self._rdelay = RdelayCls(self._core, self._cmd_group)
		return self._rdelay

	@property
	def speed(self):
		"""speed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_speed'):
			from .Speed import SpeedCls
			self._speed = SpeedCls(self._core, self._cmd_group)
		return self._speed

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'PathCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PathCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
