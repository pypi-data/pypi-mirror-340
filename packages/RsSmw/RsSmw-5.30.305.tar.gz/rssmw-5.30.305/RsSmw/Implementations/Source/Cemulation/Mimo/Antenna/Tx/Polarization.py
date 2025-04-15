from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PolarizationCls:
	"""Polarization commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("polarization", core, parent)

	# noinspection PyTypeChecker
	def get_angle(self) -> enums.AntModPolAngle:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:ANTenna:TX:POLarization:ANGLe \n
		Snippet: value: enums.AntModPolAngle = driver.source.cemulation.mimo.antenna.tx.polarization.get_angle() \n
		No command help available \n
			:return: ant_tx_pol_angle: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:MIMO:ANTenna:TX:POLarization:ANGLe?')
		return Conversions.str_to_scalar_enum(response, enums.AntModPolAngle)

	def set_angle(self, ant_tx_pol_angle: enums.AntModPolAngle) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:ANTenna:TX:POLarization:ANGLe \n
		Snippet: driver.source.cemulation.mimo.antenna.tx.polarization.set_angle(ant_tx_pol_angle = enums.AntModPolAngle.POLCO0) \n
		No command help available \n
			:param ant_tx_pol_angle: No help available
		"""
		param = Conversions.enum_scalar_to_str(ant_tx_pol_angle, enums.AntModPolAngle)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MIMO:ANTenna:TX:POLarization:ANGLe {param}')
