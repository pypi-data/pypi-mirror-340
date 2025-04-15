from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InitPatternCls:
	"""InitPattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("initPattern", core, parent)

	def get(self, userNull=repcap.UserNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:PUUCi:INITpattern \n
		Snippet: value: float = driver.source.bb.nr5G.ubwp.user.puuci.initPattern.get(userNull = repcap.UserNull.Default) \n
		Sets an initialization value for the second m-sequence in the PN sequence.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select a PN sequence as data source ([:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:PUUCi:DATA) . \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: pattern_init: No help available"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:PUUCi:INITpattern?')
		return Conversions.str_to_float(response)
