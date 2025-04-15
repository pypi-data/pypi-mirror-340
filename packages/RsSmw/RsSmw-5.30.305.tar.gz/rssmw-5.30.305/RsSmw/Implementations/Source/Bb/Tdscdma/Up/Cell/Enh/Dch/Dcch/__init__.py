from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DcchCls:
	"""Dcch commands group definition. 12 total commands, 10 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dcch", core, parent)

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
	def eprotection(self):
		"""eprotection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eprotection'):
			from .Eprotection import EprotectionCls
			self._eprotection = EprotectionCls(self._core, self._cmd_group)
		return self._eprotection

	@property
	def ione(self):
		"""ione commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ione'):
			from .Ione import IoneCls
			self._ione = IoneCls(self._core, self._cmd_group)
		return self._ione

	@property
	def itwo(self):
		"""itwo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_itwo'):
			from .Itwo import ItwoCls
			self._itwo = ItwoCls(self._core, self._cmd_group)
		return self._itwo

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

	def clone(self) -> 'DcchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DcchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
