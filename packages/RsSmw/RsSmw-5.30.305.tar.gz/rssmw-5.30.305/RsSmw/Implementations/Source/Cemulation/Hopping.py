from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HoppingCls:
	"""Hopping commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hopping", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FadHoppMode:
		"""SCPI: [SOURce<HW>]:CEMulation:HOPPing:MODE \n
		Snippet: value: enums.FadHoppMode = driver.source.cemulation.hopping.get_mode() \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:HOPPing:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FadHoppMode)

	def set_mode(self, mode: enums.FadHoppMode) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:HOPPing:MODE \n
		Snippet: driver.source.cemulation.hopping.set_mode(mode = enums.FadHoppMode.IBANd) \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FadHoppMode)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:HOPPing:MODE {param}')
