from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ListPyCls:
	"""ListPy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("listPy", core, parent)

	def get_values(self) -> str:
		"""SCPI: SCONfiguration:RFALignment:SETup:INFO:CALibration:POWer:LIST:VALues \n
		Snippet: value: str = driver.sconfiguration.rfAlignment.setup.info.calibration.power.listPy.get_values() \n
		No command help available \n
			:return: list_of_values: string
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:INFO:CALibration:POWer:LIST:VALues?')
		return trim_str_response(response)
