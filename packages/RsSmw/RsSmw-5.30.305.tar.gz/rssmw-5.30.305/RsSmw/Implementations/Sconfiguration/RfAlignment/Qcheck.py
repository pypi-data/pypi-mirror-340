from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class QcheckCls:
	"""Qcheck commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("qcheck", core, parent)

	def get_state(self) -> bool:
		"""SCPI: SCONfiguration:RFALignment:QCHeck:[STATe] \n
		Snippet: value: bool = driver.sconfiguration.rfAlignment.qcheck.get_state() \n
		No command help available \n
			:return: quick_check_state: No help available
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:QCHeck:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, quick_check_state: bool) -> None:
		"""SCPI: SCONfiguration:RFALignment:QCHeck:[STATe] \n
		Snippet: driver.sconfiguration.rfAlignment.qcheck.set_state(quick_check_state = False) \n
		No command help available \n
			:param quick_check_state: No help available
		"""
		param = Conversions.bool_to_str(quick_check_state)
		self._core.io.write(f'SCONfiguration:RFALignment:QCHeck:STATe {param}')
