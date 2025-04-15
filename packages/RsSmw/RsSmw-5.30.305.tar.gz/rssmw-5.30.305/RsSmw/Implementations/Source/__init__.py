from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 12613 total commands, 31 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	@property
	def bextension(self):
		"""bextension commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_bextension'):
			from .Bextension import BextensionCls
			self._bextension = BextensionCls(self._core, self._cmd_group)
		return self._bextension

	@property
	def pgenerator(self):
		"""pgenerator commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_pgenerator'):
			from .Pgenerator import PgeneratorCls
			self._pgenerator = PgeneratorCls(self._core, self._cmd_group)
		return self._pgenerator

	@property
	def rfAlignment(self):
		"""rfAlignment commands group. 4 Sub-classes, 4 commands."""
		if not hasattr(self, '_rfAlignment'):
			from .RfAlignment import RfAlignmentCls
			self._rfAlignment = RfAlignmentCls(self._core, self._cmd_group)
		return self._rfAlignment

	@property
	def am(self):
		"""am commands group. 4 Sub-classes, 2 commands."""
		if not hasattr(self, '_am'):
			from .Am import AmCls
			self._am = AmCls(self._core, self._cmd_group)
		return self._am

	@property
	def areGenerator(self):
		"""areGenerator commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_areGenerator'):
			from .AreGenerator import AreGeneratorCls
			self._areGenerator = AreGeneratorCls(self._core, self._cmd_group)
		return self._areGenerator

	@property
	def awgn(self):
		"""awgn commands group. 5 Sub-classes, 5 commands."""
		if not hasattr(self, '_awgn'):
			from .Awgn import AwgnCls
			self._awgn = AwgnCls(self._core, self._cmd_group)
		return self._awgn

	@property
	def bb(self):
		"""bb commands group. 38 Sub-classes, 7 commands."""
		if not hasattr(self, '_bb'):
			from .Bb import BbCls
			self._bb = BbCls(self._core, self._cmd_group)
		return self._bb

	@property
	def bbin(self):
		"""bbin commands group. 7 Sub-classes, 9 commands."""
		if not hasattr(self, '_bbin'):
			from .Bbin import BbinCls
			self._bbin = BbinCls(self._core, self._cmd_group)
		return self._bbin

	@property
	def cemulation(self):
		"""cemulation commands group. 28 Sub-classes, 14 commands."""
		if not hasattr(self, '_cemulation'):
			from .Cemulation import CemulationCls
			self._cemulation = CemulationCls(self._core, self._cmd_group)
		return self._cemulation

	@property
	def combined(self):
		"""combined commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_combined'):
			from .Combined import CombinedCls
			self._combined = CombinedCls(self._core, self._cmd_group)
		return self._combined

	@property
	def correction(self):
		"""correction commands group. 6 Sub-classes, 2 commands."""
		if not hasattr(self, '_correction'):
			from .Correction import CorrectionCls
			self._correction = CorrectionCls(self._core, self._cmd_group)
		return self._correction

	@property
	def dm(self):
		"""dm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dm'):
			from .Dm import DmCls
			self._dm = DmCls(self._core, self._cmd_group)
		return self._dm

	@property
	def efrontend(self):
		"""efrontend commands group. 13 Sub-classes, 8 commands."""
		if not hasattr(self, '_efrontend'):
			from .Efrontend import EfrontendCls
			self._efrontend = EfrontendCls(self._core, self._cmd_group)
		return self._efrontend

	@property
	def fm(self):
		"""fm commands group. 4 Sub-classes, 3 commands."""
		if not hasattr(self, '_fm'):
			from .Fm import FmCls
			self._fm = FmCls(self._core, self._cmd_group)
		return self._fm

	@property
	def frequency(self):
		"""frequency commands group. 6 Sub-classes, 9 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def fsimulator(self):
		"""fsimulator commands group. 28 Sub-classes, 14 commands."""
		if not hasattr(self, '_fsimulator'):
			from .Fsimulator import FsimulatorCls
			self._fsimulator = FsimulatorCls(self._core, self._cmd_group)
		return self._fsimulator

	@property
	def inputPy(self):
		"""inputPy commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_inputPy'):
			from .InputPy import InputPyCls
			self._inputPy = InputPyCls(self._core, self._cmd_group)
		return self._inputPy

	@property
	def iq(self):
		"""iq commands group. 5 Sub-classes, 5 commands."""
		if not hasattr(self, '_iq'):
			from .Iq import IqCls
			self._iq = IqCls(self._core, self._cmd_group)
		return self._iq

	@property
	def lfOutput(self):
		"""lfOutput commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_lfOutput'):
			from .LfOutput import LfOutputCls
			self._lfOutput = LfOutputCls(self._core, self._cmd_group)
		return self._lfOutput

	@property
	def listPy(self):
		"""listPy commands group. 7 Sub-classes, 9 commands."""
		if not hasattr(self, '_listPy'):
			from .ListPy import ListPyCls
			self._listPy = ListPyCls(self._core, self._cmd_group)
		return self._listPy

	@property
	def modulation(self):
		"""modulation commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import ModulationCls
			self._modulation = ModulationCls(self._core, self._cmd_group)
		return self._modulation

	@property
	def noise(self):
		"""noise commands group. 4 Sub-classes, 1 commands."""
		if not hasattr(self, '_noise'):
			from .Noise import NoiseCls
			self._noise = NoiseCls(self._core, self._cmd_group)
		return self._noise

	@property
	def occupy(self):
		"""occupy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_occupy'):
			from .Occupy import OccupyCls
			self._occupy = OccupyCls(self._core, self._cmd_group)
		return self._occupy

	@property
	def path(self):
		"""path commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_path'):
			from .Path import PathCls
			self._path = PathCls(self._core, self._cmd_group)
		return self._path

	@property
	def phase(self):
		"""phase commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_phase'):
			from .Phase import PhaseCls
			self._phase = PhaseCls(self._core, self._cmd_group)
		return self._phase

	@property
	def pm(self):
		"""pm commands group. 4 Sub-classes, 3 commands."""
		if not hasattr(self, '_pm'):
			from .Pm import PmCls
			self._pm = PmCls(self._core, self._cmd_group)
		return self._pm

	@property
	def power(self):
		"""power commands group. 8 Sub-classes, 11 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def pulm(self):
		"""pulm commands group. 3 Sub-classes, 9 commands."""
		if not hasattr(self, '_pulm'):
			from .Pulm import PulmCls
			self._pulm = PulmCls(self._core, self._cmd_group)
		return self._pulm

	@property
	def regenerator(self):
		"""regenerator commands group. 7 Sub-classes, 5 commands."""
		if not hasattr(self, '_regenerator'):
			from .Regenerator import RegeneratorCls
			self._regenerator = RegeneratorCls(self._core, self._cmd_group)
		return self._regenerator

	@property
	def roscillator(self):
		"""roscillator commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_roscillator'):
			from .Roscillator import RoscillatorCls
			self._roscillator = RoscillatorCls(self._core, self._cmd_group)
		return self._roscillator

	@property
	def sweep(self):
		"""sweep commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_sweep'):
			from .Sweep import SweepCls
			self._sweep = SweepCls(self._core, self._cmd_group)
		return self._sweep

	def preset(self) -> None:
		"""SCPI: SOURce<HW>:PRESet \n
		Snippet: driver.source.preset() \n
			INTRO_CMD_HELP: Supported in 2x1x1 configurations: \n
			- method RsSmw.Sconfiguration.modeSTANdard
			- method RsSmw.Sconfiguration.modeADVanced with method RsSmw.Sconfiguration.fadingFAAFBB
		Presets all parameters which are related to the selected signal path. Fading simulator (if available) and the transient
		recorder are only preset by the command *RST. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SOURce<HW>:PRESet \n
		Snippet: driver.source.preset_with_opc() \n
			INTRO_CMD_HELP: Supported in 2x1x1 configurations: \n
			- method RsSmw.Sconfiguration.modeSTANdard
			- method RsSmw.Sconfiguration.modeADVanced with method RsSmw.Sconfiguration.fadingFAAFBB
		Presets all parameters which are related to the selected signal path. Fading simulator (if available) and the transient
		recorder are only preset by the command *RST. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:PRESet', opc_timeout_ms)

	def clone(self) -> 'SourceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SourceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
