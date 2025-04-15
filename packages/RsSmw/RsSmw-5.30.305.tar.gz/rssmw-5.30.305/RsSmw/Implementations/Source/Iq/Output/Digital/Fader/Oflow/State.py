from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def get(self, digitalIq=repcap.DigitalIq.Default) -> bool:
		"""SCPI: [SOURce]:IQ:OUTPut:DIGital:FADer<CH>:OFLow:STATe \n
		Snippet: value: bool = driver.source.iq.output.digital.fader.oflow.state.get(digitalIq = repcap.DigitalIq.Default) \n
		Queries whether the I/Q output signal is clipped or not. \n
			:param digitalIq: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fader')
			:return: state: 1| ON| 0| OFF"""
		digitalIq_cmd_val = self._cmd_group.get_repcap_cmd_value(digitalIq, repcap.DigitalIq)
		response = self._core.io.query_str(f'SOURce:IQ:OUTPut:DIGital:FADer{digitalIq_cmd_val}:OFLow:STATe?')
		return Conversions.str_to_bool(response)
