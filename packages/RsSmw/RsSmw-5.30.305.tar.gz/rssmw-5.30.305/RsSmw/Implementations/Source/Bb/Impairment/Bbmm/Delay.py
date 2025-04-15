from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DelayCls:
	"""Delay commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delay", core, parent)

	def set(self, delay: float, iqConnector=repcap.IqConnector.Default) -> None:
		"""SCPI: [SOURce]:BB:IMPairment:BBMM<CH>:DELay \n
		Snippet: driver.source.bb.impairment.bbmm.delay.set(delay = 1.0, iqConnector = repcap.IqConnector.Default) \n
		Defines the time delay of both I and Q vectors between the marker signal at the marker outputs relative to the signal
		generation start. A positive value means that the I and Q vectors delay relative to the marker/trigger and vice versa.
		Value range
			Table Header: Output / Min /s / Max /s / Increment \n
			- RF<ch> / 0 / 10E-6 / 1E-12
			- FADer<ch> / 0 / 500E-9 / 1E-12
			- IQOutput<ch> / 500E-9 / 500E-9 / 1E-12
			- BBMM<ch> / 500E-9 / 500E-9 / 1E-12 \n
			:param delay: float Range: 0 to 10E-6
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bbmm')
		"""
		param = Conversions.decimal_value_to_str(delay)
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		self._core.io.write(f'SOURce:BB:IMPairment:BBMM{iqConnector_cmd_val}:DELay {param}')

	def get(self, iqConnector=repcap.IqConnector.Default) -> float:
		"""SCPI: [SOURce]:BB:IMPairment:BBMM<CH>:DELay \n
		Snippet: value: float = driver.source.bb.impairment.bbmm.delay.get(iqConnector = repcap.IqConnector.Default) \n
		Defines the time delay of both I and Q vectors between the marker signal at the marker outputs relative to the signal
		generation start. A positive value means that the I and Q vectors delay relative to the marker/trigger and vice versa.
		Value range
			Table Header: Output / Min /s / Max /s / Increment \n
			- RF<ch> / 0 / 10E-6 / 1E-12
			- FADer<ch> / 0 / 500E-9 / 1E-12
			- IQOutput<ch> / 500E-9 / 500E-9 / 1E-12
			- BBMM<ch> / 500E-9 / 500E-9 / 1E-12 \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bbmm')
			:return: delay: float Range: 0 to 10E-6"""
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		response = self._core.io.query_str(f'SOURce:BB:IMPairment:BBMM{iqConnector_cmd_val}:DELay?')
		return Conversions.str_to_float(response)
