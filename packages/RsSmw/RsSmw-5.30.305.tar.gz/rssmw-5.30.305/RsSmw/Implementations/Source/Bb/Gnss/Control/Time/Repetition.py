from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RepetitionCls:
	"""Repetition commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("repetition", core, parent)

	def get_actual(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:CONTrol:TIME:REPetition:ACTual \n
		Snippet: value: float = driver.source.bb.gnss.control.time.repetition.get_actual() \n
		Queries the current repetition of the GNSS simulation duration. \n
			:return: current_iter: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:CONTrol:TIME:REPetition:ACTual?')
		return Conversions.str_to_float(response)

	def get_count(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:CONTrol:TIME:REPetition:COUNt \n
		Snippet: value: int = driver.source.bb.gnss.control.time.repetition.get_count() \n
		Sets the number of repetitions of a configured GNSS simulation duration. If you enable infinite repetitions, the number
		of repetitions is also infinite. \n
			:return: numb_repetitions: integer Range: 1 to 1000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:CONTrol:TIME:REPetition:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, numb_repetitions: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:CONTrol:TIME:REPetition:COUNt \n
		Snippet: driver.source.bb.gnss.control.time.repetition.set_count(numb_repetitions = 1) \n
		Sets the number of repetitions of a configured GNSS simulation duration. If you enable infinite repetitions, the number
		of repetitions is also infinite. \n
			:param numb_repetitions: integer Range: 1 to 1000
		"""
		param = Conversions.decimal_value_to_str(numb_repetitions)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:CONTrol:TIME:REPetition:COUNt {param}')

	def get_infinite(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:CONTrol:TIME:REPetition:INFinite \n
		Snippet: value: bool = driver.source.bb.gnss.control.time.repetition.get_infinite() \n
		Enables an infinite number of repetitions of a configured GNSS simulation duration. If enabled, the number of repetitions
		is also infinite. \n
			:return: limited_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:CONTrol:TIME:REPetition:INFinite?')
		return Conversions.str_to_bool(response)

	def set_infinite(self, limited_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:CONTrol:TIME:REPetition:INFinite \n
		Snippet: driver.source.bb.gnss.control.time.repetition.set_infinite(limited_state = False) \n
		Enables an infinite number of repetitions of a configured GNSS simulation duration. If enabled, the number of repetitions
		is also infinite. \n
			:param limited_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(limited_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:CONTrol:TIME:REPetition:INFinite {param}')
