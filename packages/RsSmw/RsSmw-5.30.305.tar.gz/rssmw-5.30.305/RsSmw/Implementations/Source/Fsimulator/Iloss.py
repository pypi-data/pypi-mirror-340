from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IlossCls:
	"""Iloss commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iloss", core, parent)

	def get_csamples(self) -> float:
		"""SCPI: [SOURce<HW>]:FSIMulator:ILOSs:CSAMples \n
		Snippet: value: float = driver.source.fsimulator.iloss.get_csamples() \n
		Queries the share of samples which were clipped due to the insertion loss setting. \n
			:return: csamples: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:ILOSs:CSAMples?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FadInsLossMode:
		"""SCPI: [SOURce<HW>]:FSIMulator:ILOSs:MODE \n
		Snippet: value: enums.FadInsLossMode = driver.source.fsimulator.iloss.get_mode() \n
		Sets the insertion loss of the fading simulator. \n
			:return: mode: NORMal| LACP| USER NORMal The minimum insertion loss for a path of the fading simulator is set to a fixed value of 18 dB. LACP The minimum insertion loss is between 6 dB and 12 dB. This value is dependent upon the 'Path Loss' setting of the fading paths which are switched on. 'Low ACP' mode is only recommended for fading paths with Raleigh profile. Only in this case a statistical distribution of level fluctuation is ensured. For other fading profiles, non-statistical level fluctuations occur which lead to an enormous increase of clipping. However, monitoring the percentage of clipped samples is recommended for Raleigh paths also. USER Any value for the minimum insertion loss in the range from 0 dB to 18 dB can be selected. Enter the value using the :SOURce1:FSIMulator:ILOSs:LOSS command.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:ILOSs:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FadInsLossMode)

	def set_mode(self, mode: enums.FadInsLossMode) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:ILOSs:MODE \n
		Snippet: driver.source.fsimulator.iloss.set_mode(mode = enums.FadInsLossMode.LACP) \n
		Sets the insertion loss of the fading simulator. \n
			:param mode: NORMal| LACP| USER NORMal The minimum insertion loss for a path of the fading simulator is set to a fixed value of 18 dB. LACP The minimum insertion loss is between 6 dB and 12 dB. This value is dependent upon the 'Path Loss' setting of the fading paths which are switched on. 'Low ACP' mode is only recommended for fading paths with Raleigh profile. Only in this case a statistical distribution of level fluctuation is ensured. For other fading profiles, non-statistical level fluctuations occur which lead to an enormous increase of clipping. However, monitoring the percentage of clipped samples is recommended for Raleigh paths also. USER Any value for the minimum insertion loss in the range from 0 dB to 18 dB can be selected. Enter the value using the :SOURce1:FSIMulator:ILOSs:LOSS command.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FadInsLossMode)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:ILOSs:MODE {param}')

	def get_loss(self) -> float:
		"""SCPI: [SOURce<HW>]:FSIMulator:ILOSs:[LOSS] \n
		Snippet: value: float = driver.source.fsimulator.iloss.get_loss() \n
		Sets the user-defined insertion loss of the fading simulator when 'User' is selected. In the 'Normal' and 'Low ACP' modes,
		the current setting of the value can be queried. \n
			:return: loss: float Range: -3 to 30, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:ILOSs:LOSS?')
		return Conversions.str_to_float(response)

	def set_loss(self, loss: float) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:ILOSs:[LOSS] \n
		Snippet: driver.source.fsimulator.iloss.set_loss(loss = 1.0) \n
		Sets the user-defined insertion loss of the fading simulator when 'User' is selected. In the 'Normal' and 'Low ACP' modes,
		the current setting of the value can be queried. \n
			:param loss: float Range: -3 to 30, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(loss)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:ILOSs:LOSS {param}')
