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

	def get(self, userNull=repcap.UserNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:SSCH:INITpattern \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.user.ssch.initPattern.get(userNull = repcap.UserNull.Default) \n
		Defines the initial value when the PSSCH data source is a pseudo-random sequence.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select one of the pseudo-random sequences as data source ([:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:SSCH:DATA) . \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: ssch_pattern_init: No help available"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:SSCH:INITpattern?')
		return Conversions.str_to_int(response)
