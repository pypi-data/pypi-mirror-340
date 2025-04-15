from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GvectorCls:
	"""Gvector commands group definition. 131 total commands, 66 Subgroups, 1 group commands
	Repeated Capability: GainVector, default value after init: GainVector.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gvector", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_gainVector_get', 'repcap_gainVector_set', repcap.GainVector.Nr1)

	def repcap_gainVector_set(self, gainVector: repcap.GainVector) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to GainVector.Default.
		Default value after init: GainVector.Nr1"""
		self._cmd_group.set_repcap_enum_value(gainVector)

	def repcap_gainVector_get(self) -> repcap.GainVector:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def aa(self):
		"""aa commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_aa'):
			from .Aa import AaCls
			self._aa = AaCls(self._core, self._cmd_group)
		return self._aa

	@property
	def ab(self):
		"""ab commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ab'):
			from .Ab import AbCls
			self._ab = AbCls(self._core, self._cmd_group)
		return self._ab

	@property
	def ac(self):
		"""ac commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ac'):
			from .Ac import AcCls
			self._ac = AcCls(self._core, self._cmd_group)
		return self._ac

	@property
	def ad(self):
		"""ad commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ad'):
			from .Ad import AdCls
			self._ad = AdCls(self._core, self._cmd_group)
		return self._ad

	@property
	def ae(self):
		"""ae commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ae'):
			from .Ae import AeCls
			self._ae = AeCls(self._core, self._cmd_group)
		return self._ae

	@property
	def af(self):
		"""af commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_af'):
			from .Af import AfCls
			self._af = AfCls(self._core, self._cmd_group)
		return self._af

	@property
	def ag(self):
		"""ag commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ag'):
			from .Ag import AgCls
			self._ag = AgCls(self._core, self._cmd_group)
		return self._ag

	@property
	def ah(self):
		"""ah commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ah'):
			from .Ah import AhCls
			self._ah = AhCls(self._core, self._cmd_group)
		return self._ah

	@property
	def ba(self):
		"""ba commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ba'):
			from .Ba import BaCls
			self._ba = BaCls(self._core, self._cmd_group)
		return self._ba

	@property
	def bb(self):
		"""bb commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_bb'):
			from .Bb import BbCls
			self._bb = BbCls(self._core, self._cmd_group)
		return self._bb

	@property
	def bc(self):
		"""bc commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_bc'):
			from .Bc import BcCls
			self._bc = BcCls(self._core, self._cmd_group)
		return self._bc

	@property
	def bd(self):
		"""bd commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_bd'):
			from .Bd import BdCls
			self._bd = BdCls(self._core, self._cmd_group)
		return self._bd

	@property
	def be(self):
		"""be commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_be'):
			from .Be import BeCls
			self._be = BeCls(self._core, self._cmd_group)
		return self._be

	@property
	def bf(self):
		"""bf commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_bf'):
			from .Bf import BfCls
			self._bf = BfCls(self._core, self._cmd_group)
		return self._bf

	@property
	def bg(self):
		"""bg commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_bg'):
			from .Bg import BgCls
			self._bg = BgCls(self._core, self._cmd_group)
		return self._bg

	@property
	def bh(self):
		"""bh commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_bh'):
			from .Bh import BhCls
			self._bh = BhCls(self._core, self._cmd_group)
		return self._bh

	@property
	def ca(self):
		"""ca commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ca'):
			from .Ca import CaCls
			self._ca = CaCls(self._core, self._cmd_group)
		return self._ca

	@property
	def cb(self):
		"""cb commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cb'):
			from .Cb import CbCls
			self._cb = CbCls(self._core, self._cmd_group)
		return self._cb

	@property
	def cc(self):
		"""cc commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cc'):
			from .Cc import CcCls
			self._cc = CcCls(self._core, self._cmd_group)
		return self._cc

	@property
	def cd(self):
		"""cd commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cd'):
			from .Cd import CdCls
			self._cd = CdCls(self._core, self._cmd_group)
		return self._cd

	@property
	def ce(self):
		"""ce commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ce'):
			from .Ce import CeCls
			self._ce = CeCls(self._core, self._cmd_group)
		return self._ce

	@property
	def cf(self):
		"""cf commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cf'):
			from .Cf import CfCls
			self._cf = CfCls(self._core, self._cmd_group)
		return self._cf

	@property
	def cg(self):
		"""cg commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cg'):
			from .Cg import CgCls
			self._cg = CgCls(self._core, self._cmd_group)
		return self._cg

	@property
	def ch(self):
		"""ch commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ch'):
			from .Ch import ChCls
			self._ch = ChCls(self._core, self._cmd_group)
		return self._ch

	@property
	def da(self):
		"""da commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_da'):
			from .Da import DaCls
			self._da = DaCls(self._core, self._cmd_group)
		return self._da

	@property
	def db(self):
		"""db commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_db'):
			from .Db import DbCls
			self._db = DbCls(self._core, self._cmd_group)
		return self._db

	@property
	def dc(self):
		"""dc commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dc'):
			from .Dc import DcCls
			self._dc = DcCls(self._core, self._cmd_group)
		return self._dc

	@property
	def dd(self):
		"""dd commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dd'):
			from .Dd import DdCls
			self._dd = DdCls(self._core, self._cmd_group)
		return self._dd

	@property
	def de(self):
		"""de commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_de'):
			from .De import DeCls
			self._de = DeCls(self._core, self._cmd_group)
		return self._de

	@property
	def df(self):
		"""df commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_df'):
			from .Df import DfCls
			self._df = DfCls(self._core, self._cmd_group)
		return self._df

	@property
	def dg(self):
		"""dg commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dg'):
			from .Dg import DgCls
			self._dg = DgCls(self._core, self._cmd_group)
		return self._dg

	@property
	def dh(self):
		"""dh commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dh'):
			from .Dh import DhCls
			self._dh = DhCls(self._core, self._cmd_group)
		return self._dh

	@property
	def ea(self):
		"""ea commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ea'):
			from .Ea import EaCls
			self._ea = EaCls(self._core, self._cmd_group)
		return self._ea

	@property
	def eb(self):
		"""eb commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_eb'):
			from .Eb import EbCls
			self._eb = EbCls(self._core, self._cmd_group)
		return self._eb

	@property
	def ec(self):
		"""ec commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ec'):
			from .Ec import EcCls
			self._ec = EcCls(self._core, self._cmd_group)
		return self._ec

	@property
	def ed(self):
		"""ed commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ed'):
			from .Ed import EdCls
			self._ed = EdCls(self._core, self._cmd_group)
		return self._ed

	@property
	def ee(self):
		"""ee commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ee'):
			from .Ee import EeCls
			self._ee = EeCls(self._core, self._cmd_group)
		return self._ee

	@property
	def ef(self):
		"""ef commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ef'):
			from .Ef import EfCls
			self._ef = EfCls(self._core, self._cmd_group)
		return self._ef

	@property
	def eg(self):
		"""eg commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_eg'):
			from .Eg import EgCls
			self._eg = EgCls(self._core, self._cmd_group)
		return self._eg

	@property
	def eh(self):
		"""eh commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_eh'):
			from .Eh import EhCls
			self._eh = EhCls(self._core, self._cmd_group)
		return self._eh

	@property
	def fa(self):
		"""fa commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fa'):
			from .Fa import FaCls
			self._fa = FaCls(self._core, self._cmd_group)
		return self._fa

	@property
	def fb(self):
		"""fb commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fb'):
			from .Fb import FbCls
			self._fb = FbCls(self._core, self._cmd_group)
		return self._fb

	@property
	def fc(self):
		"""fc commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fc'):
			from .Fc import FcCls
			self._fc = FcCls(self._core, self._cmd_group)
		return self._fc

	@property
	def fd(self):
		"""fd commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fd'):
			from .Fd import FdCls
			self._fd = FdCls(self._core, self._cmd_group)
		return self._fd

	@property
	def fe(self):
		"""fe commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fe'):
			from .Fe import FeCls
			self._fe = FeCls(self._core, self._cmd_group)
		return self._fe

	@property
	def ff(self):
		"""ff commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ff'):
			from .Ff import FfCls
			self._ff = FfCls(self._core, self._cmd_group)
		return self._ff

	@property
	def fg(self):
		"""fg commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fg'):
			from .Fg import FgCls
			self._fg = FgCls(self._core, self._cmd_group)
		return self._fg

	@property
	def fh(self):
		"""fh commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fh'):
			from .Fh import FhCls
			self._fh = FhCls(self._core, self._cmd_group)
		return self._fh

	@property
	def ga(self):
		"""ga commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ga'):
			from .Ga import GaCls
			self._ga = GaCls(self._core, self._cmd_group)
		return self._ga

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gain'):
			from .Gain import GainCls
			self._gain = GainCls(self._core, self._cmd_group)
		return self._gain

	@property
	def gb(self):
		"""gb commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gb'):
			from .Gb import GbCls
			self._gb = GbCls(self._core, self._cmd_group)
		return self._gb

	@property
	def gc(self):
		"""gc commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gc'):
			from .Gc import GcCls
			self._gc = GcCls(self._core, self._cmd_group)
		return self._gc

	@property
	def gd(self):
		"""gd commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gd'):
			from .Gd import GdCls
			self._gd = GdCls(self._core, self._cmd_group)
		return self._gd

	@property
	def ge(self):
		"""ge commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ge'):
			from .Ge import GeCls
			self._ge = GeCls(self._core, self._cmd_group)
		return self._ge

	@property
	def gf(self):
		"""gf commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gf'):
			from .Gf import GfCls
			self._gf = GfCls(self._core, self._cmd_group)
		return self._gf

	@property
	def gg(self):
		"""gg commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gg'):
			from .Gg import GgCls
			self._gg = GgCls(self._core, self._cmd_group)
		return self._gg

	@property
	def gh(self):
		"""gh commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gh'):
			from .Gh import GhCls
			self._gh = GhCls(self._core, self._cmd_group)
		return self._gh

	@property
	def ha(self):
		"""ha commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ha'):
			from .Ha import HaCls
			self._ha = HaCls(self._core, self._cmd_group)
		return self._ha

	@property
	def hb(self):
		"""hb commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_hb'):
			from .Hb import HbCls
			self._hb = HbCls(self._core, self._cmd_group)
		return self._hb

	@property
	def hc(self):
		"""hc commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_hc'):
			from .Hc import HcCls
			self._hc = HcCls(self._core, self._cmd_group)
		return self._hc

	@property
	def hd(self):
		"""hd commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_hd'):
			from .Hd import HdCls
			self._hd = HdCls(self._core, self._cmd_group)
		return self._hd

	@property
	def he(self):
		"""he commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_he'):
			from .He import HeCls
			self._he = HeCls(self._core, self._cmd_group)
		return self._he

	@property
	def hf(self):
		"""hf commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_hf'):
			from .Hf import HfCls
			self._hf = HfCls(self._core, self._cmd_group)
		return self._hf

	@property
	def hg(self):
		"""hg commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_hg'):
			from .Hg import HgCls
			self._hg = HgCls(self._core, self._cmd_group)
		return self._hg

	@property
	def hh(self):
		"""hh commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_hh'):
			from .Hh import HhCls
			self._hh = HhCls(self._core, self._cmd_group)
		return self._hh

	@property
	def phase(self):
		"""phase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_phase'):
			from .Phase import PhaseCls
			self._phase = PhaseCls(self._core, self._cmd_group)
		return self._phase

	def preset(self, mimoTap=repcap.MimoTap.Default) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:MIMO:TAP<CH>:GVECtor:PRESet \n
		Snippet: driver.source.fsimulator.mimo.tap.gvector.preset(mimoTap = repcap.MimoTap.Default) \n
		Presets the vector matrix to a unitary matrix. \n
			:param mimoTap: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tap')
		"""
		mimoTap_cmd_val = self._cmd_group.get_repcap_cmd_value(mimoTap, repcap.MimoTap)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:MIMO:TAP{mimoTap_cmd_val}:GVECtor:PRESet')

	def preset_with_opc(self, mimoTap=repcap.MimoTap.Default, opc_timeout_ms: int = -1) -> None:
		mimoTap_cmd_val = self._cmd_group.get_repcap_cmd_value(mimoTap, repcap.MimoTap)
		"""SCPI: [SOURce<HW>]:FSIMulator:MIMO:TAP<CH>:GVECtor:PRESet \n
		Snippet: driver.source.fsimulator.mimo.tap.gvector.preset_with_opc(mimoTap = repcap.MimoTap.Default) \n
		Presets the vector matrix to a unitary matrix. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param mimoTap: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tap')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:FSIMulator:MIMO:TAP{mimoTap_cmd_val}:GVECtor:PRESet', opc_timeout_ms)

	def clone(self) -> 'GvectorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GvectorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
