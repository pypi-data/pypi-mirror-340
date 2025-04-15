from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LevelCls:
	"""Level commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	def set(self, level: float, digitalIq=repcap.DigitalIq.Default) -> None:
		"""SCPI: [SOURce]:IQ:OUTPut:DIGital:FADer<CH>:POWer:LEVel \n
		Snippet: driver.source.iq.output.digital.fader.power.level.set(level = 1.0, digitalIq = repcap.DigitalIq.Default) \n
		Enters the RMS level of the output signal. \n
			:param level: float Range: -80 to 0
			:param digitalIq: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fader')
		"""
		param = Conversions.decimal_value_to_str(level)
		digitalIq_cmd_val = self._cmd_group.get_repcap_cmd_value(digitalIq, repcap.DigitalIq)
		self._core.io.write(f'SOURce:IQ:OUTPut:DIGital:FADer{digitalIq_cmd_val}:POWer:LEVel {param}')

	def get(self, digitalIq=repcap.DigitalIq.Default) -> float:
		"""SCPI: [SOURce]:IQ:OUTPut:DIGital:FADer<CH>:POWer:LEVel \n
		Snippet: value: float = driver.source.iq.output.digital.fader.power.level.get(digitalIq = repcap.DigitalIq.Default) \n
		Enters the RMS level of the output signal. \n
			:param digitalIq: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fader')
			:return: level: float Range: -80 to 0"""
		digitalIq_cmd_val = self._cmd_group.get_repcap_cmd_value(digitalIq, repcap.DigitalIq)
		response = self._core.io.query_str(f'SOURce:IQ:OUTPut:DIGital:FADer{digitalIq_cmd_val}:POWer:LEVel?')
		return Conversions.str_to_float(response)
