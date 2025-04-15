from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ClusterCls:
	"""Cluster commands group definition. 9 total commands, 5 Subgroups, 0 group commands
	Repeated Capability: Cluster, default value after init: Cluster.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cluster", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_cluster_get', 'repcap_cluster_set', repcap.Cluster.Nr1)

	def repcap_cluster_set(self, cluster: repcap.Cluster) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Cluster.Default.
		Default value after init: Cluster.Nr1"""
		self._cmd_group.set_repcap_enum_value(cluster)

	def repcap_cluster_get(self) -> repcap.Cluster:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def arrival(self):
		"""arrival commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_arrival'):
			from .Arrival import ArrivalCls
			self._arrival = ArrivalCls(self._core, self._cmd_group)
		return self._arrival

	@property
	def departure(self):
		"""departure commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_departure'):
			from .Departure import DepartureCls
			self._departure = DepartureCls(self._core, self._cmd_group)
		return self._departure

	@property
	def distribution(self):
		"""distribution commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_distribution'):
			from .Distribution import DistributionCls
			self._distribution = DistributionCls(self._core, self._cmd_group)
		return self._distribution

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gain'):
			from .Gain import GainCls
			self._gain = GainCls(self._core, self._cmd_group)
		return self._gain

	@property
	def tap(self):
		"""tap commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tap'):
			from .Tap import TapCls
			self._tap = TapCls(self._core, self._cmd_group)
		return self._tap

	def clone(self) -> 'ClusterCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ClusterCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
