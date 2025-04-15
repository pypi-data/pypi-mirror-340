from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GainCls:
	"""Gain commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gain", core, parent)

	def set(self, gain: float, terminal=repcap.Terminal.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TERMinal<ST>:RRIChannel:GAIN \n
		Snippet: driver.source.bb.evdo.terminal.rriChannel.gain.set(gain = 1.0, terminal = repcap.Terminal.Default) \n
		(enabled for an access terminal working in traffic mode) Sets the gain of the Reverse Rate Indicator (RRI) channel
		relative to the pilot channel power. \n
			:param gain: float Range: -80 to 10 dB
			:param terminal: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
		"""
		param = Conversions.decimal_value_to_str(gain)
		terminal_cmd_val = self._cmd_group.get_repcap_cmd_value(terminal, repcap.Terminal)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{terminal_cmd_val}:RRIChannel:GAIN {param}')

	def get(self, terminal=repcap.Terminal.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TERMinal<ST>:RRIChannel:GAIN \n
		Snippet: value: float = driver.source.bb.evdo.terminal.rriChannel.gain.get(terminal = repcap.Terminal.Default) \n
		(enabled for an access terminal working in traffic mode) Sets the gain of the Reverse Rate Indicator (RRI) channel
		relative to the pilot channel power. \n
			:param terminal: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:return: gain: float Range: -80 to 10 dB"""
		terminal_cmd_val = self._cmd_group.get_repcap_cmd_value(terminal, repcap.Terminal)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{terminal_cmd_val}:RRIChannel:GAIN?')
		return Conversions.str_to_float(response)
