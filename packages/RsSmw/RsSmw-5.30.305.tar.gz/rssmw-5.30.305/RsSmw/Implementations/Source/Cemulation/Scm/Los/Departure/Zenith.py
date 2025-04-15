from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ZenithCls:
	"""Zenith commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("zenith", core, parent)

	def get_angle(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:LOS:DEParture:ZENith:ANGLe \n
		Snippet: value: float = driver.source.cemulation.scm.los.departure.zenith.get_angle() \n
		No command help available \n
			:return: los_zenith_depar: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:SCM:LOS:DEParture:ZENith:ANGLe?')
		return Conversions.str_to_float(response)

	def set_angle(self, los_zenith_depar: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:LOS:DEParture:ZENith:ANGLe \n
		Snippet: driver.source.cemulation.scm.los.departure.zenith.set_angle(los_zenith_depar = 1.0) \n
		No command help available \n
			:param los_zenith_depar: No help available
		"""
		param = Conversions.decimal_value_to_str(los_zenith_depar)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SCM:LOS:DEParture:ZENith:ANGLe {param}')
