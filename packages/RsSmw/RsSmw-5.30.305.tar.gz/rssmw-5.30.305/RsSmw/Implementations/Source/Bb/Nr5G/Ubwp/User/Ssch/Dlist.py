from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DlistCls:
	"""Dlist commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dlist", core, parent)

	def get(self, userNull=repcap.UserNull.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:SSCH:DLISt \n
		Snippet: value: str = driver.source.bb.nr5G.ubwp.user.ssch.dlist.get(userNull = repcap.UserNull.Default) \n
		Selects a data list as a PSSCH data source.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select a data list as data source ([:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:SSCH:DATA) . \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: ssch_data_list: No help available"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:SSCH:DLISt?')
		return trim_str_response(response)
