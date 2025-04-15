from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TxCls:
	"""Tx commands group definition. 116 total commands, 29 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tx", core, parent)

	@property
	def ac(self):
		"""ac commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ac'):
			from .Ac import AcCls
			self._ac = AcCls(self._core, self._cmd_group)
		return self._ac

	@property
	def ad(self):
		"""ad commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ad'):
			from .Ad import AdCls
			self._ad = AdCls(self._core, self._cmd_group)
		return self._ad

	@property
	def ae(self):
		"""ae commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ae'):
			from .Ae import AeCls
			self._ae = AeCls(self._core, self._cmd_group)
		return self._ae

	@property
	def af(self):
		"""af commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_af'):
			from .Af import AfCls
			self._af = AfCls(self._core, self._cmd_group)
		return self._af

	@property
	def ag(self):
		"""ag commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ag'):
			from .Ag import AgCls
			self._ag = AgCls(self._core, self._cmd_group)
		return self._ag

	@property
	def ah(self):
		"""ah commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ah'):
			from .Ah import AhCls
			self._ah = AhCls(self._core, self._cmd_group)
		return self._ah

	@property
	def bc(self):
		"""bc commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_bc'):
			from .Bc import BcCls
			self._bc = BcCls(self._core, self._cmd_group)
		return self._bc

	@property
	def bd(self):
		"""bd commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_bd'):
			from .Bd import BdCls
			self._bd = BdCls(self._core, self._cmd_group)
		return self._bd

	@property
	def be(self):
		"""be commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_be'):
			from .Be import BeCls
			self._be = BeCls(self._core, self._cmd_group)
		return self._be

	@property
	def bf(self):
		"""bf commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_bf'):
			from .Bf import BfCls
			self._bf = BfCls(self._core, self._cmd_group)
		return self._bf

	@property
	def bg(self):
		"""bg commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_bg'):
			from .Bg import BgCls
			self._bg = BgCls(self._core, self._cmd_group)
		return self._bg

	@property
	def bh(self):
		"""bh commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_bh'):
			from .Bh import BhCls
			self._bh = BhCls(self._core, self._cmd_group)
		return self._bh

	@property
	def cd(self):
		"""cd commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_cd'):
			from .Cd import CdCls
			self._cd = CdCls(self._core, self._cmd_group)
		return self._cd

	@property
	def ce(self):
		"""ce commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ce'):
			from .Ce import CeCls
			self._ce = CeCls(self._core, self._cmd_group)
		return self._ce

	@property
	def cf(self):
		"""cf commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_cf'):
			from .Cf import CfCls
			self._cf = CfCls(self._core, self._cmd_group)
		return self._cf

	@property
	def cg(self):
		"""cg commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_cg'):
			from .Cg import CgCls
			self._cg = CgCls(self._core, self._cmd_group)
		return self._cg

	@property
	def ch(self):
		"""ch commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ch'):
			from .Ch import ChCls
			self._ch = ChCls(self._core, self._cmd_group)
		return self._ch

	@property
	def de(self):
		"""de commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_de'):
			from .De import DeCls
			self._de = DeCls(self._core, self._cmd_group)
		return self._de

	@property
	def df(self):
		"""df commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_df'):
			from .Df import DfCls
			self._df = DfCls(self._core, self._cmd_group)
		return self._df

	@property
	def dg(self):
		"""dg commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_dg'):
			from .Dg import DgCls
			self._dg = DgCls(self._core, self._cmd_group)
		return self._dg

	@property
	def dh(self):
		"""dh commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_dh'):
			from .Dh import DhCls
			self._dh = DhCls(self._core, self._cmd_group)
		return self._dh

	@property
	def ef(self):
		"""ef commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ef'):
			from .Ef import EfCls
			self._ef = EfCls(self._core, self._cmd_group)
		return self._ef

	@property
	def eg(self):
		"""eg commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_eg'):
			from .Eg import EgCls
			self._eg = EgCls(self._core, self._cmd_group)
		return self._eg

	@property
	def eh(self):
		"""eh commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_eh'):
			from .Eh import EhCls
			self._eh = EhCls(self._core, self._cmd_group)
		return self._eh

	@property
	def fg(self):
		"""fg commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_fg'):
			from .Fg import FgCls
			self._fg = FgCls(self._core, self._cmd_group)
		return self._fg

	@property
	def fh(self):
		"""fh commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_fh'):
			from .Fh import FhCls
			self._fh = FhCls(self._core, self._cmd_group)
		return self._fh

	@property
	def gh(self):
		"""gh commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_gh'):
			from .Gh import GhCls
			self._gh = GhCls(self._core, self._cmd_group)
		return self._gh

	@property
	def row(self):
		"""row commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_row'):
			from .Row import RowCls
			self._row = RowCls(self._core, self._cmd_group)
		return self._row

	@property
	def ab(self):
		"""ab commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ab'):
			from .Ab import AbCls
			self._ab = AbCls(self._core, self._cmd_group)
		return self._ab

	def clone(self) -> 'TxCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TxCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
