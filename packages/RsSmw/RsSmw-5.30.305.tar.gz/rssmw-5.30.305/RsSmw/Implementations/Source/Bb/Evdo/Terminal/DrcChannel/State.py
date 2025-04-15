from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool, terminal=repcap.Terminal.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TERMinal<ST>:DRCChannel:STATe \n
		Snippet: driver.source.bb.evdo.terminal.drcChannel.state.set(state = False, terminal = repcap.Terminal.Default) \n
		(enabled for an access terminal working in traffic mode) Enables or disables the state of the Data Rate Control (DRC)
		channel. \n
			:param state: 1| ON| 0| OFF
			:param terminal: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
		"""
		param = Conversions.bool_to_str(state)
		terminal_cmd_val = self._cmd_group.get_repcap_cmd_value(terminal, repcap.Terminal)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{terminal_cmd_val}:DRCChannel:STATe {param}')

	def get(self, terminal=repcap.Terminal.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TERMinal<ST>:DRCChannel:STATe \n
		Snippet: value: bool = driver.source.bb.evdo.terminal.drcChannel.state.get(terminal = repcap.Terminal.Default) \n
		(enabled for an access terminal working in traffic mode) Enables or disables the state of the Data Rate Control (DRC)
		channel. \n
			:param terminal: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:return: state: 1| ON| 0| OFF"""
		terminal_cmd_val = self._cmd_group.get_repcap_cmd_value(terminal, repcap.Terminal)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{terminal_cmd_val}:DRCChannel:STATe?')
		return Conversions.str_to_bool(response)
