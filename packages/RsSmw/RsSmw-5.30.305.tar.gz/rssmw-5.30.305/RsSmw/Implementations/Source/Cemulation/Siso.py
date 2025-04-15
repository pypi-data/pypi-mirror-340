from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SisoCls:
	"""Siso commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("siso", core, parent)

	# noinspection PyTypeChecker
	def get_copy(self) -> enums.FadCopyHwdEst:
		"""SCPI: [SOURce<HW>]:CEMulation:SISO:COPY \n
		Snippet: value: enums.FadCopyHwdEst = driver.source.cemulation.siso.get_copy() \n
		No command help available \n
			:return: copy_to_dest: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:SISO:COPY?')
		return Conversions.str_to_scalar_enum(response, enums.FadCopyHwdEst)

	def set_copy(self, copy_to_dest: enums.FadCopyHwdEst) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SISO:COPY \n
		Snippet: driver.source.cemulation.siso.set_copy(copy_to_dest = enums.FadCopyHwdEst.ALL) \n
		No command help available \n
			:param copy_to_dest: No help available
		"""
		param = Conversions.enum_scalar_to_str(copy_to_dest, enums.FadCopyHwdEst)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SISO:COPY {param}')
