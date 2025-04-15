from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserCls:
	"""User commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("user", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:UCONfig:USER:STATe \n
		Snippet: value: bool = driver.source.bb.wlay.pconfig.uconfig.user.get_state() \n
		Activates the respective user. The current firmware provides one user (one spatial stream) that is active. There are no
		suffixes to specify more users. An SU PPDU is transmitted. \n
			:return: usr_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:UCONfig:USER:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, usr_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:UCONfig:USER:STATe \n
		Snippet: driver.source.bb.wlay.pconfig.uconfig.user.set_state(usr_state = False) \n
		Activates the respective user. The current firmware provides one user (one spatial stream) that is active. There are no
		suffixes to specify more users. An SU PPDU is transmitted. \n
			:param usr_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(usr_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:UCONfig:USER:STATe {param}')
