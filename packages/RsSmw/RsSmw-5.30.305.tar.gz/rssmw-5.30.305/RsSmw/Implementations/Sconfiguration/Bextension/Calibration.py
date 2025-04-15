from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CalibrationCls:
	"""Calibration commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("calibration", core, parent)

	def get_state(self) -> bool:
		"""SCPI: SCONfiguration:BEXTension:CALibration:STATe \n
		Snippet: value: bool = driver.sconfiguration.bextension.calibration.get_state() \n
		No command help available \n
			:return: calib_state: No help available
		"""
		response = self._core.io.query_str('SCONfiguration:BEXTension:CALibration:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, calib_state: bool) -> None:
		"""SCPI: SCONfiguration:BEXTension:CALibration:STATe \n
		Snippet: driver.sconfiguration.bextension.calibration.set_state(calib_state = False) \n
		No command help available \n
			:param calib_state: No help available
		"""
		param = Conversions.bool_to_str(calib_state)
		self._core.io.write(f'SCONfiguration:BEXTension:CALibration:STATe {param}')
