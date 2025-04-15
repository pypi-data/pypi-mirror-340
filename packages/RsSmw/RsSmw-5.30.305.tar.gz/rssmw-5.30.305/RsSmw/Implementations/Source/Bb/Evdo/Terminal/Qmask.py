from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class QmaskCls:
	"""Qmask commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("qmask", core, parent)

	def set(self, qmask: str, terminal=repcap.Terminal.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TERMinal<ST>:QMASk \n
		Snippet: driver.source.bb.evdo.terminal.qmask.set(qmask = rawAbc, terminal = repcap.Terminal.Default) \n
		Sets the long code mask of the Q channel. \n
			:param qmask: 44 bits
			:param terminal: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
		"""
		param = Conversions.value_to_str(qmask)
		terminal_cmd_val = self._cmd_group.get_repcap_cmd_value(terminal, repcap.Terminal)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{terminal_cmd_val}:QMASk {param}')

	def get(self, terminal=repcap.Terminal.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TERMinal<ST>:QMASk \n
		Snippet: value: str = driver.source.bb.evdo.terminal.qmask.get(terminal = repcap.Terminal.Default) \n
		Sets the long code mask of the Q channel. \n
			:param terminal: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:return: qmask: 44 bits"""
		terminal_cmd_val = self._cmd_group.get_repcap_cmd_value(terminal, repcap.Terminal)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{terminal_cmd_val}:QMASk?')
		return trim_str_response(response)
