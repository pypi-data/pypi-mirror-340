from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LoscillatorCls:
	"""Loscillator commands group definition. 4 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("loscillator", core, parent)

	@property
	def inputPy(self):
		"""inputPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_inputPy'):
			from .InputPy import InputPyCls
			self._inputPy = InputPyCls(self._core, self._cmd_group)
		return self._inputPy

	@property
	def output(self):
		"""output commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.SourceInt:
		"""SCPI: [SOURce<HW>]:EFRontend:LOSCillator:MODE \n
		Snippet: value: enums.SourceInt = driver.source.efrontend.loscillator.get_mode() \n
		Selects the LO input source for the connected external frontend. \n
			:return: mode: INTernal| EXTernal INTernal Uses the internally generated LO signal. EXTernal Uses an externally supplied LO signal.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:LOSCillator:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.SourceInt)

	def set_mode(self, mode: enums.SourceInt) -> None:
		"""SCPI: [SOURce<HW>]:EFRontend:LOSCillator:MODE \n
		Snippet: driver.source.efrontend.loscillator.set_mode(mode = enums.SourceInt.EXTernal) \n
		Selects the LO input source for the connected external frontend. \n
			:param mode: INTernal| EXTernal INTernal Uses the internally generated LO signal. EXTernal Uses an externally supplied LO signal.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.SourceInt)
		self._core.io.write(f'SOURce<HwInstance>:EFRontend:LOSCillator:MODE {param}')

	def clone(self) -> 'LoscillatorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LoscillatorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
