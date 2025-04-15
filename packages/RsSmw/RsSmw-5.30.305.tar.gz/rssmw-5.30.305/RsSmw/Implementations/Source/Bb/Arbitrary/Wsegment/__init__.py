from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class WsegmentCls:
	"""Wsegment commands group definition. 26 total commands, 3 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("wsegment", core, parent)

	@property
	def configure(self):
		"""configure commands group. 5 Sub-classes, 5 commands."""
		if not hasattr(self, '_configure'):
			from .Configure import ConfigureCls
			self._configure = ConfigureCls(self._core, self._cmd_group)
		return self._configure

	@property
	def next(self):
		"""next commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_next'):
			from .Next import NextCls
			self._next = NextCls(self._core, self._cmd_group)
		return self._next

	@property
	def sequence(self):
		"""sequence commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sequence'):
			from .Sequence import SequenceCls
			self._sequence = SequenceCls(self._core, self._cmd_group)
		return self._sequence

	def set_cload(self, filename_input: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:CLOad \n
		Snippet: driver.source.bb.arbitrary.wsegment.set_cload(filename_input = 'abc') \n
		Creates a multi-segment waveform using the current entries of the specified configuration file (*.inf_mswv) . The ARB
		generator is activated, the new multi-segment waveform (*.wv) is loaded and the first segment is output in accordance to
		the trigger settings. \n
			:param filename_input: string Complete file path, file name of the configuration file and file extension (*.inf_mswv)
		"""
		param = Conversions.value_to_quoted_str(filename_input)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CLOad {param}')

	def set_create(self, filename_input: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:CREate \n
		Snippet: driver.source.bb.arbitrary.wsegment.set_create(filename_input = 'abc') \n
		Creates a multi-segment waveform (*.wv) using the current settings of the specified configuration file (*.inf_mswv) . \n
			:param filename_input: Complete file path, file name of the configuration file and file extension (*.inf_mswv)
		"""
		param = Conversions.value_to_quoted_str(filename_input)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CREate {param}')

	# noinspection PyTypeChecker
	def get_lmode(self) -> enums.ArbLevMode:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:LMODe \n
		Snippet: value: enums.ArbLevMode = driver.source.bb.arbitrary.wsegment.get_lmode() \n
		Sets how the segments are leveled. \n
			:return: level_mode: HIGHest| UNCHanged
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:LMODe?')
		return Conversions.str_to_scalar_enum(response, enums.ArbLevMode)

	def set_lmode(self, level_mode: enums.ArbLevMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:LMODe \n
		Snippet: driver.source.bb.arbitrary.wsegment.set_lmode(level_mode = enums.ArbLevMode.HIGHest) \n
		Sets how the segments are leveled. \n
			:param level_mode: HIGHest| UNCHanged
		"""
		param = Conversions.enum_scalar_to_str(level_mode, enums.ArbLevMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:LMODe {param}')

	def get_name(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:NAME \n
		Snippet: value: str = driver.source.bb.arbitrary.wsegment.get_name() \n
		Queries the name of the waveform of the currently output segment of the multi-segment waveform. \n
			:return: name: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:NAME?')
		return trim_str_response(response)

	def get_value(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment \n
		Snippet: value: int = driver.source.bb.arbitrary.wsegment.get_value() \n
		Queries the index of the currently processed segment. \n
			:return: wsegment: integer Range: 0 to 1023
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'WsegmentCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = WsegmentCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
