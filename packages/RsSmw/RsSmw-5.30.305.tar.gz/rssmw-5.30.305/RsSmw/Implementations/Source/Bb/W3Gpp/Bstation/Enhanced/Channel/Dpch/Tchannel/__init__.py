from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TchannelCls:
	"""Tchannel commands group definition. 12 total commands, 10 Subgroups, 0 group commands
	Repeated Capability: TransportChannelNull, default value after init: TransportChannelNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tchannel", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_transportChannelNull_get', 'repcap_transportChannelNull_set', repcap.TransportChannelNull.Nr0)

	def repcap_transportChannelNull_set(self, transportChannelNull: repcap.TransportChannelNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TransportChannelNull.Default.
		Default value after init: TransportChannelNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(transportChannelNull)

	def repcap_transportChannelNull_get(self) -> repcap.TransportChannelNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def crcSize(self):
		"""crcSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crcSize'):
			from .CrcSize import CrcSizeCls
			self._crcSize = CrcSizeCls(self._core, self._cmd_group)
		return self._crcSize

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def dtx(self):
		"""dtx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dtx'):
			from .Dtx import DtxCls
			self._dtx = DtxCls(self._core, self._cmd_group)
		return self._dtx

	@property
	def eprotection(self):
		"""eprotection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eprotection'):
			from .Eprotection import EprotectionCls
			self._eprotection = EprotectionCls(self._core, self._cmd_group)
		return self._eprotection

	@property
	def interleaver(self):
		"""interleaver commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_interleaver'):
			from .Interleaver import InterleaverCls
			self._interleaver = InterleaverCls(self._core, self._cmd_group)
		return self._interleaver

	@property
	def rmAttribute(self):
		"""rmAttribute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rmAttribute'):
			from .RmAttribute import RmAttributeCls
			self._rmAttribute = RmAttributeCls(self._core, self._cmd_group)
		return self._rmAttribute

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def tbCount(self):
		"""tbCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbCount'):
			from .TbCount import TbCountCls
			self._tbCount = TbCountCls(self._core, self._cmd_group)
		return self._tbCount

	@property
	def tbSize(self):
		"""tbSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbSize'):
			from .TbSize import TbSizeCls
			self._tbSize = TbSizeCls(self._core, self._cmd_group)
		return self._tbSize

	@property
	def ttInterval(self):
		"""ttInterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttInterval'):
			from .TtInterval import TtIntervalCls
			self._ttInterval = TtIntervalCls(self._core, self._cmd_group)
		return self._ttInterval

	def clone(self) -> 'TchannelCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TchannelCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
