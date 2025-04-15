from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class VhtControlCls:
	"""VhtControl commands group definition. 13 total commands, 12 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("vhtControl", core, parent)

	@property
	def acConstraint(self):
		"""acConstraint commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_acConstraint'):
			from .AcConstraint import AcConstraintCls
			self._acConstraint = AcConstraintCls(self._core, self._cmd_group)
		return self._acConstraint

	@property
	def ctype(self):
		"""ctype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ctype'):
			from .Ctype import CtypeCls
			self._ctype = CtypeCls(self._core, self._cmd_group)
		return self._ctype

	@property
	def ftType(self):
		"""ftType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ftType'):
			from .FtType import FtTypeCls
			self._ftType = FtTypeCls(self._core, self._cmd_group)
		return self._ftType

	@property
	def gidh(self):
		"""gidh commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gidh'):
			from .Gidh import GidhCls
			self._gidh = GidhCls(self._core, self._cmd_group)
		return self._gidh

	@property
	def mfb(self):
		"""mfb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mfb'):
			from .Mfb import MfbCls
			self._mfb = MfbCls(self._core, self._cmd_group)
		return self._mfb

	@property
	def mgl(self):
		"""mgl commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mgl'):
			from .Mgl import MglCls
			self._mgl = MglCls(self._core, self._cmd_group)
		return self._mgl

	@property
	def mrq(self):
		"""mrq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mrq'):
			from .Mrq import MrqCls
			self._mrq = MrqCls(self._core, self._cmd_group)
		return self._mrq

	@property
	def msi(self):
		"""msi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_msi'):
			from .Msi import MsiCls
			self._msi = MsiCls(self._core, self._cmd_group)
		return self._msi

	@property
	def rdgMore(self):
		"""rdgMore commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rdgMore'):
			from .RdgMore import RdgMoreCls
			self._rdgMore = RdgMoreCls(self._core, self._cmd_group)
		return self._rdgMore

	@property
	def s1G(self):
		"""s1G commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_s1G'):
			from .S1G import S1GCls
			self._s1G = S1GCls(self._core, self._cmd_group)
		return self._s1G

	@property
	def umfb(self):
		"""umfb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_umfb'):
			from .Umfb import UmfbCls
			self._umfb = UmfbCls(self._core, self._cmd_group)
		return self._umfb

	@property
	def vreserved(self):
		"""vreserved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vreserved'):
			from .Vreserved import VreservedCls
			self._vreserved = VreservedCls(self._core, self._cmd_group)
		return self._vreserved

	def set(self, vht_contol: str, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl \n
		Snippet: driver.source.bb.wlnn.fblock.mac.vhtControl.set(vht_contol = rawAbc, frameBlock = repcap.FrameBlock.Default) \n
		The command sets the value for the VHT control field. \n
			:param vht_contol: integer Range: #H00000000,32 to #HFFFFFFFF,32
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.value_to_str(vht_contol)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:VHTControl {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl \n
		Snippet: value: str = driver.source.bb.wlnn.fblock.mac.vhtControl.get(frameBlock = repcap.FrameBlock.Default) \n
		The command sets the value for the VHT control field. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: vht_contol: integer Range: #H00000000,32 to #HFFFFFFFF,32"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:VHTControl?')
		return trim_str_response(response)

	def clone(self) -> 'VhtControlCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = VhtControlCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
