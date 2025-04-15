from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LdirectionCls:
	"""Ldirection commands group definition. 18 total commands, 14 Subgroups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ldirection", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def repcap_channel_set(self, channel: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default.
		Default value after init: Channel.Nr1"""
		self._cmd_group.set_repcap_enum_value(channel)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def amode(self):
		"""amode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_amode'):
			from .Amode import AmodeCls
			self._amode = AmodeCls(self._core, self._cmd_group)
		return self._amode

	@property
	def apf1(self):
		"""apf1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apf1'):
			from .Apf1 import Apf1Cls
			self._apf1 = Apf1Cls(self._core, self._cmd_group)
		return self._apf1

	@property
	def apf2(self):
		"""apf2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apf2'):
			from .Apf2 import Apf2Cls
			self._apf2 = Apf2Cls(self._core, self._cmd_group)
		return self._apf2

	@property
	def apHeader(self):
		"""apHeader commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apHeader'):
			from .ApHeader import ApHeaderCls
			self._apHeader = ApHeaderCls(self._core, self._cmd_group)
		return self._apHeader

	@property
	def bsAttenuation(self):
		"""bsAttenuation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bsAttenuation'):
			from .BsAttenuation import BsAttenuationCls
			self._bsAttenuation = BsAttenuationCls(self._core, self._cmd_group)
		return self._bsAttenuation

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def lcType(self):
		"""lcType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lcType'):
			from .LcType import LcTypeCls
			self._lcType = LcTypeCls(self._core, self._cmd_group)
		return self._lcType

	@property
	def scrambling(self):
		"""scrambling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scrambling'):
			from .Scrambling import ScramblingCls
			self._scrambling = ScramblingCls(self._core, self._cmd_group)
		return self._scrambling

	@property
	def sdata(self):
		"""sdata commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_sdata'):
			from .Sdata import SdataCls
			self._sdata = SdataCls(self._core, self._cmd_group)
		return self._sdata

	@property
	def slevel(self):
		"""slevel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slevel'):
			from .Slevel import SlevelCls
			self._slevel = SlevelCls(self._core, self._cmd_group)
		return self._slevel

	@property
	def ssAttenuation(self):
		"""ssAttenuation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssAttenuation'):
			from .SsAttenuation import SsAttenuationCls
			self._ssAttenuation = SsAttenuationCls(self._core, self._cmd_group)
		return self._ssAttenuation

	@property
	def ssLevel(self):
		"""ssLevel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssLevel'):
			from .SsLevel import SsLevelCls
			self._ssLevel = SsLevelCls(self._core, self._cmd_group)
		return self._ssLevel

	@property
	def tpattern(self):
		"""tpattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpattern'):
			from .Tpattern import TpatternCls
			self._tpattern = TpatternCls(self._core, self._cmd_group)
		return self._tpattern

	@property
	def tsource(self):
		"""tsource commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tsource'):
			from .Tsource import TsourceCls
			self._tsource = TsourceCls(self._core, self._cmd_group)
		return self._tsource

	def clone(self) -> 'LdirectionCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LdirectionCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
