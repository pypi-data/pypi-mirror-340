from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardCls:
	"""Standard commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("standard", core, parent)

	def get_reference(self) -> str:
		"""SCPI: [SOURce<HW>]:CEMulation:STANdard:REFerence \n
		Snippet: value: str = driver.source.cemulation.standard.get_reference() \n
		No command help available \n
			:return: reference: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:STANdard:REFerence?')
		return trim_str_response(response)

	def set_reference(self, reference: str) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:STANdard:REFerence \n
		Snippet: driver.source.cemulation.standard.set_reference(reference = 'abc') \n
		No command help available \n
			:param reference: No help available
		"""
		param = Conversions.value_to_quoted_str(reference)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:STANdard:REFerence {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.FadStan:
		"""SCPI: [SOURce<HW>]:CEMulation:STANdard \n
		Snippet: value: enums.FadStan = driver.source.cemulation.standard.get_value() \n
		No command help available \n
			:return: standard: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:STANdard?')
		return Conversions.str_to_scalar_enum(response, enums.FadStan)

	def set_value(self, standard: enums.FadStan) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:STANdard \n
		Snippet: driver.source.cemulation.standard.set_value(standard = enums.FadStan.BD1) \n
		No command help available \n
			:param standard: No help available
		"""
		param = Conversions.enum_scalar_to_str(standard, enums.FadStan)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:STANdard {param}')
