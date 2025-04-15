from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HsTrainCls:
	"""HsTrain commands group definition. 11 total commands, 3 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hsTrain", core, parent)

	@property
	def distance(self):
		"""distance commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_distance'):
			from .Distance import DistanceCls
			self._distance = DistanceCls(self._core, self._cmd_group)
		return self._distance

	@property
	def downlink(self):
		"""downlink commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_downlink'):
			from .Downlink import DownlinkCls
			self._downlink = DownlinkCls(self._core, self._cmd_group)
		return self._downlink

	@property
	def path(self):
		"""path commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_path'):
			from .Path import PathCls
			self._path = PathCls(self._core, self._cmd_group)
		return self._path

	def get_fdoppler(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:FDOPpler \n
		Snippet: value: float = driver.source.cemulation.hsTrain.get_fdoppler() \n
		No command help available \n
			:return: fdoppler: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:HSTRain:FDOPpler?')
		return Conversions.str_to_float(response)

	def get_kfactor(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:KFACtor \n
		Snippet: value: float = driver.source.cemulation.hsTrain.get_kfactor() \n
		No command help available \n
			:return: kfactor: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:HSTRain:KFACtor?')
		return Conversions.str_to_float(response)

	def set_kfactor(self, kfactor: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:KFACtor \n
		Snippet: driver.source.cemulation.hsTrain.set_kfactor(kfactor = 1.0) \n
		No command help available \n
			:param kfactor: No help available
		"""
		param = Conversions.decimal_value_to_str(kfactor)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:HSTRain:KFACtor {param}')

	# noinspection PyTypeChecker
	def get_profile(self) -> enums.FadingProfileB:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:PROFile \n
		Snippet: value: enums.FadingProfileB = driver.source.cemulation.hsTrain.get_profile() \n
		No command help available \n
			:return: profile: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:HSTRain:PROFile?')
		return Conversions.str_to_scalar_enum(response, enums.FadingProfileB)

	def set_profile(self, profile: enums.FadingProfileB) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:PROFile \n
		Snippet: driver.source.cemulation.hsTrain.set_profile(profile = enums.FadingProfileB.BELLindoor) \n
		No command help available \n
			:param profile: No help available
		"""
		param = Conversions.enum_scalar_to_str(profile, enums.FadingProfileB)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:HSTRain:PROFile {param}')

	def get_soffset(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:SOFFset \n
		Snippet: value: float = driver.source.cemulation.hsTrain.get_soffset() \n
		No command help available \n
			:return: start_offset: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:HSTRain:SOFFset?')
		return Conversions.str_to_float(response)

	def set_soffset(self, start_offset: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:SOFFset \n
		Snippet: driver.source.cemulation.hsTrain.set_soffset(start_offset = 1.0) \n
		No command help available \n
			:param start_offset: No help available
		"""
		param = Conversions.decimal_value_to_str(start_offset)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:HSTRain:SOFFset {param}')

	def get_speed(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:SPEed \n
		Snippet: value: float = driver.source.cemulation.hsTrain.get_speed() \n
		No command help available \n
			:return: speed: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:HSTRain:SPEed?')
		return Conversions.str_to_float(response)

	def set_speed(self, speed: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:SPEed \n
		Snippet: driver.source.cemulation.hsTrain.set_speed(speed = 1.0) \n
		No command help available \n
			:param speed: No help available
		"""
		param = Conversions.decimal_value_to_str(speed)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:HSTRain:SPEed {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:STATe \n
		Snippet: value: bool = driver.source.cemulation.hsTrain.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:HSTRain:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:STATe \n
		Snippet: driver.source.cemulation.hsTrain.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:HSTRain:STATe {param}')

	def clone(self) -> 'HsTrainCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HsTrainCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
