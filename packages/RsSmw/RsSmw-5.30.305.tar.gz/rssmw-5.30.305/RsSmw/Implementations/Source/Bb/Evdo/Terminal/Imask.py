from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ImaskCls:
	"""Imask commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("imask", core, parent)

	def set(self, imask: str, terminal=repcap.Terminal.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TERMinal<ST>:IMASk \n
		Snippet: driver.source.bb.evdo.terminal.imask.set(imask = rawAbc, terminal = repcap.Terminal.Default) \n
		Sets the long code mask of the I channel. \n
			:param imask: 44 bits
			:param terminal: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
		"""
		param = Conversions.value_to_str(imask)
		terminal_cmd_val = self._cmd_group.get_repcap_cmd_value(terminal, repcap.Terminal)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{terminal_cmd_val}:IMASk {param}')

	def get(self, terminal=repcap.Terminal.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TERMinal<ST>:IMASk \n
		Snippet: value: str = driver.source.bb.evdo.terminal.imask.get(terminal = repcap.Terminal.Default) \n
		Sets the long code mask of the I channel. \n
			:param terminal: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:return: imask: 44 bits"""
		terminal_cmd_val = self._cmd_group.get_repcap_cmd_value(terminal, repcap.Terminal)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{terminal_cmd_val}:IMASk?')
		return trim_str_response(response)
