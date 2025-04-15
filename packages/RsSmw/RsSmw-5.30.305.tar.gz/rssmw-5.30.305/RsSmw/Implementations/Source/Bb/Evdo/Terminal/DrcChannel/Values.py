from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ValuesCls:
	"""Values commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("values", core, parent)

	def set(self, values: str, terminal=repcap.Terminal.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TERMinal<ST>:DRCChannel:VALues \n
		Snippet: driver.source.bb.evdo.terminal.drcChannel.values.set(values = rawAbc, terminal = repcap.Terminal.Default) \n
		(enabled for an access terminal working in traffic mode) Specifies the pattern transmitted on the Data Rate Control (DRC)
		Channel. The sequence starts at frame 0 and slot 0 and is repeated with the length of the pattern. Each specified value
		is used for DRC length slots. \n
			:param values: integer
			:param terminal: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
		"""
		param = Conversions.value_to_str(values)
		terminal_cmd_val = self._cmd_group.get_repcap_cmd_value(terminal, repcap.Terminal)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{terminal_cmd_val}:DRCChannel:VALues {param}')

	def get(self, terminal=repcap.Terminal.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TERMinal<ST>:DRCChannel:VALues \n
		Snippet: value: str = driver.source.bb.evdo.terminal.drcChannel.values.get(terminal = repcap.Terminal.Default) \n
		(enabled for an access terminal working in traffic mode) Specifies the pattern transmitted on the Data Rate Control (DRC)
		Channel. The sequence starts at frame 0 and slot 0 and is repeated with the length of the pattern. Each specified value
		is used for DRC length slots. \n
			:param terminal: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:return: values: integer"""
		terminal_cmd_val = self._cmd_group.get_repcap_cmd_value(terminal, repcap.Terminal)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{terminal_cmd_val}:DRCChannel:VALues?')
		return trim_str_response(response)
