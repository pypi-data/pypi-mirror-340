from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AsequencingCls:
	"""Asequencing commands group definition. 17 total commands, 4 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("asequencing", core, parent)

	@property
	def qsfp(self):
		"""qsfp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_qsfp'):
			from .Qsfp import QsfpCls
			self._qsfp = QsfpCls(self._core, self._cmd_group)
		return self._qsfp

	@property
	def wave(self):
		"""wave commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_wave'):
			from .Wave import WaveCls
			self._wave = WaveCls(self._core, self._cmd_group)
		return self._wave

	@property
	def wlist(self):
		"""wlist commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_wlist'):
			from .Wlist import WlistCls
			self._wlist = WlistCls(self._core, self._cmd_group)
		return self._wlist

	@property
	def sequencer(self):
		"""sequencer commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_sequencer'):
			from .Sequencer import SequencerCls
			self._sequencer = SequencerCls(self._core, self._cmd_group)
		return self._sequencer

	# noinspection PyTypeChecker
	def get_omode(self) -> enums.ExtSeqAdwMode:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:ASEQuencing:OMODe \n
		Snippet: value: enums.ExtSeqAdwMode = driver.source.bb.esequencer.asequencing.get_omode() \n
		Selects the operation mode. \n
			:return: operation_mode: INSTant| DETerministic INSTant The generator plays back prestored ARB segments according to the ADW with low latency. DETerministic The generator plays back prestored ARB segments according to the ADW after a 'ready' signal is acknowledged and the next ARB segment is triggered.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ESEQuencer:ASEQuencing:OMODe?')
		return Conversions.str_to_scalar_enum(response, enums.ExtSeqAdwMode)

	def set_omode(self, operation_mode: enums.ExtSeqAdwMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:ASEQuencing:OMODe \n
		Snippet: driver.source.bb.esequencer.asequencing.set_omode(operation_mode = enums.ExtSeqAdwMode.DETerministic) \n
		Selects the operation mode. \n
			:param operation_mode: INSTant| DETerministic INSTant The generator plays back prestored ARB segments according to the ADW with low latency. DETerministic The generator plays back prestored ARB segments according to the ADW after a 'ready' signal is acknowledged and the next ARB segment is triggered.
		"""
		param = Conversions.enum_scalar_to_str(operation_mode, enums.ExtSeqAdwMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:ESEQuencer:ASEQuencing:OMODe {param}')

	def clone(self) -> 'AsequencingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AsequencingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
