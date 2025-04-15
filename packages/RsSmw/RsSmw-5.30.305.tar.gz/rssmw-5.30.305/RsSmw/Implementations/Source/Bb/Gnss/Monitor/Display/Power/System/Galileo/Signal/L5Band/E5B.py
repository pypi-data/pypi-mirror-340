from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class E5BCls:
	"""E5B commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("e5B", core, parent)

	def set(self, signal_state: bool, monitorPane=repcap.MonitorPane.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:MONitor<CH>:DISPlay:POWer:SYSTem:GALileo:SIGNal:L5Band:E5B \n
		Snippet: driver.source.bb.gnss.monitor.display.power.system.galileo.signal.l5Band.e5B.set(signal_state = False, monitorPane = repcap.MonitorPane.Default) \n
		Defines the signals to be visualized on the 'Power View' graph. \n
			:param signal_state: 1| ON| 0| OFF
			:param monitorPane: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Monitor')
		"""
		param = Conversions.bool_to_str(signal_state)
		monitorPane_cmd_val = self._cmd_group.get_repcap_cmd_value(monitorPane, repcap.MonitorPane)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:MONitor{monitorPane_cmd_val}:DISPlay:POWer:SYSTem:GALileo:SIGNal:L5Band:E5B {param}')

	def get(self, monitorPane=repcap.MonitorPane.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:MONitor<CH>:DISPlay:POWer:SYSTem:GALileo:SIGNal:L5Band:E5B \n
		Snippet: value: bool = driver.source.bb.gnss.monitor.display.power.system.galileo.signal.l5Band.e5B.get(monitorPane = repcap.MonitorPane.Default) \n
		Defines the signals to be visualized on the 'Power View' graph. \n
			:param monitorPane: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Monitor')
			:return: signal_state: 1| ON| 0| OFF"""
		monitorPane_cmd_val = self._cmd_group.get_repcap_cmd_value(monitorPane, repcap.MonitorPane)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:MONitor{monitorPane_cmd_val}:DISPlay:POWer:SYSTem:GALileo:SIGNal:L5Band:E5B?')
		return Conversions.str_to_bool(response)
