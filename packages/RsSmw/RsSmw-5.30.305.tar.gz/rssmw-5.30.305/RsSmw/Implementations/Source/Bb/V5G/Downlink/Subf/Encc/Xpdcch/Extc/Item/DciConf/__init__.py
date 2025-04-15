from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DciConfCls:
	"""DciConf commands group definition. 31 total commands, 31 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dciConf", core, parent)

	@property
	def apnLayer(self):
		"""apnLayer commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apnLayer'):
			from .ApnLayer import ApnLayerCls
			self._apnLayer = ApnLayerCls(self._core, self._cmd_group)
		return self._apnLayer

	@property
	def bitData(self):
		"""bitData commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bitData'):
			from .BitData import BitDataCls
			self._bitData = BitDataCls(self._core, self._cmd_group)
		return self._bitData

	@property
	def bmi(self):
		"""bmi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bmi'):
			from .Bmi import BmiCls
			self._bmi = BmiCls(self._core, self._cmd_group)
		return self._bmi

	@property
	def bsi(self):
		"""bsi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bsi'):
			from .Bsi import BsiCls
			self._bsi = BsiCls(self._core, self._cmd_group)
		return self._bsi

	@property
	def cbbRequest(self):
		"""cbbRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbbRequest'):
			from .CbbRequest import CbbRequestCls
			self._cbbRequest = CbbRequestCls(self._core, self._cmd_group)
		return self._cbbRequest

	@property
	def cbProcess(self):
		"""cbProcess commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbProcess'):
			from .CbProcess import CbProcessCls
			self._cbProcess = CbProcessCls(self._core, self._cmd_group)
		return self._cbProcess

	@property
	def cbSymbol(self):
		"""cbSymbol commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbSymbol'):
			from .CbSymbol import CbSymbolCls
			self._cbSymbol = CbSymbolCls(self._core, self._cmd_group)
		return self._cbSymbol

	@property
	def ctrTiming(self):
		"""ctrTiming commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ctrTiming'):
			from .CtrTiming import CtrTimingCls
			self._ctrTiming = CtrTimingCls(self._core, self._cmd_group)
		return self._ctrTiming

	@property
	def cycShift(self):
		"""cycShift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cycShift'):
			from .CycShift import CycShiftCls
			self._cycShift = CycShiftCls(self._core, self._cmd_group)
		return self._cycShift

	@property
	def dlPcrs(self):
		"""dlPcrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlPcrs'):
			from .DlPcrs import DlPcrsCls
			self._dlPcrs = DlPcrsCls(self._core, self._cmd_group)
		return self._dlPcrs

	@property
	def fbi(self):
		"""fbi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fbi'):
			from .Fbi import FbiCls
			self._fbi = FbiCls(self._core, self._cmd_group)
		return self._fbi

	@property
	def hpn(self):
		"""hpn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hpn'):
			from .Hpn import HpnCls
			self._hpn = HpnCls(self._core, self._cmd_group)
		return self._hpn

	@property
	def mcsr(self):
		"""mcsr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcsr'):
			from .Mcsr import McsrCls
			self._mcsr = McsrCls(self._core, self._cmd_group)
		return self._mcsr

	@property
	def ndi(self):
		"""ndi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndi'):
			from .Ndi import NdiCls
			self._ndi = NdiCls(self._core, self._cmd_group)
		return self._ndi

	@property
	def nscid(self):
		"""nscid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nscid'):
			from .Nscid import NscidCls
			self._nscid = NscidCls(self._core, self._cmd_group)
		return self._nscid

	@property
	def occIndicator(self):
		"""occIndicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_occIndicator'):
			from .OccIndicator import OccIndicatorCls
			self._occIndicator = OccIndicatorCls(self._core, self._cmd_group)
		return self._occIndicator

	@property
	def pmi(self):
		"""pmi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmi'):
			from .Pmi import PmiCls
			self._pmi = PmiCls(self._core, self._cmd_group)
		return self._pmi

	@property
	def rba(self):
		"""rba commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rba'):
			from .Rba import RbaCls
			self._rba = RbaCls(self._core, self._cmd_group)
		return self._rba

	@property
	def remap(self):
		"""remap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_remap'):
			from .Remap import RemapCls
			self._remap = RemapCls(self._core, self._cmd_group)
		return self._remap

	@property
	def rv(self):
		"""rv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rv'):
			from .Rv import RvCls
			self._rv = RvCls(self._core, self._cmd_group)
		return self._rv

	@property
	def srsRequest(self):
		"""srsRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srsRequest'):
			from .SrsRequest import SrsRequestCls
			self._srsRequest = SrsRequestCls(self._core, self._cmd_group)
		return self._srsRequest

	@property
	def srsSymbol(self):
		"""srsSymbol commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srsSymbol'):
			from .SrsSymbol import SrsSymbolCls
			self._srsSymbol = SrsSymbolCls(self._core, self._cmd_group)
		return self._srsSymbol

	@property
	def tpc(self):
		"""tpc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpc'):
			from .Tpc import TpcCls
			self._tpc = TpcCls(self._core, self._cmd_group)
		return self._tpc

	@property
	def trtiming(self):
		"""trtiming commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trtiming'):
			from .Trtiming import TrtimingCls
			self._trtiming = TrtimingCls(self._core, self._cmd_group)
		return self._trtiming

	@property
	def uciInd(self):
		"""uciInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uciInd'):
			from .UciInd import UciIndCls
			self._uciInd = UciIndCls(self._core, self._cmd_group)
		return self._uciInd

	@property
	def ufri(self):
		"""ufri commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ufri'):
			from .Ufri import UfriCls
			self._ufri = UfriCls(self._core, self._cmd_group)
		return self._ufri

	@property
	def ulPcrs(self):
		"""ulPcrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ulPcrs'):
			from .UlPcrs import UlPcrsCls
			self._ulPcrs = UlPcrsCls(self._core, self._cmd_group)
		return self._ulPcrs

	@property
	def utrTiming(self):
		"""utrTiming commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_utrTiming'):
			from .UtrTiming import UtrTimingCls
			self._utrTiming = UtrTimingCls(self._core, self._cmd_group)
		return self._utrTiming

	@property
	def xpend(self):
		"""xpend commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_xpend'):
			from .Xpend import XpendCls
			self._xpend = XpendCls(self._core, self._cmd_group)
		return self._xpend

	@property
	def xpRange(self):
		"""xpRange commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_xpRange'):
			from .XpRange import XpRangeCls
			self._xpRange = XpRangeCls(self._core, self._cmd_group)
		return self._xpRange

	@property
	def xpStart(self):
		"""xpStart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_xpStart'):
			from .XpStart import XpStartCls
			self._xpStart = XpStartCls(self._core, self._cmd_group)
		return self._xpStart

	def clone(self) -> 'DciConfCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DciConfCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
