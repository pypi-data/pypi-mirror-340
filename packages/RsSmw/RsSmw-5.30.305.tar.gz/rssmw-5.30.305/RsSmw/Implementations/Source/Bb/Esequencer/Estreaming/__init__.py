from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EstreamingCls:
	"""Estreaming commands group definition. 19 total commands, 3 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("estreaming", core, parent)

	@property
	def stream(self):
		"""stream commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_stream'):
			from .Stream import StreamCls
			self._stream = StreamCls(self._core, self._cmd_group)
		return self._stream

	@property
	def waveform(self):
		"""waveform commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_waveform'):
			from .Waveform import WaveformCls
			self._waveform = WaveformCls(self._core, self._cmd_group)
		return self._waveform

	@property
	def sequencer(self):
		"""sequencer commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sequencer'):
			from .Sequencer import SequencerCls
			self._sequencer = SequencerCls(self._core, self._cmd_group)
		return self._sequencer

	# noinspection PyTypeChecker
	def get_omode(self) -> enums.ExtSeqEthOper:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:ESTReaming:OMODe \n
		Snippet: value: enums.ExtSeqEthOper = driver.source.bb.esequencer.estreaming.get_omode() \n
		No command help available \n
			:return: operation_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ESEQuencer:ESTReaming:OMODe?')
		return Conversions.str_to_scalar_enum(response, enums.ExtSeqEthOper)

	def set_omode(self, operation_mode: enums.ExtSeqEthOper) -> None:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:ESTReaming:OMODe \n
		Snippet: driver.source.bb.esequencer.estreaming.set_omode(operation_mode = enums.ExtSeqEthOper.INSTant) \n
		No command help available \n
			:param operation_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(operation_mode, enums.ExtSeqEthOper)
		self._core.io.write(f'SOURce<HwInstance>:BB:ESEQuencer:ESTReaming:OMODe {param}')

	def get_status(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:ESTReaming:STATus \n
		Snippet: value: str = driver.source.bb.esequencer.estreaming.get_status() \n
		No command help available \n
			:return: streaming_status: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ESEQuencer:ESTReaming:STATus?')
		return trim_str_response(response)

	def clone(self) -> 'EstreamingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EstreamingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
