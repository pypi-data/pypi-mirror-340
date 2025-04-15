from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool, iqConnector=repcap.IqConnector.Default) -> None:
		"""SCPI: [SOURce]:BB:IMPairment:IQOutput<CH>:STATe \n
		Snippet: driver.source.bb.impairment.iqOutput.state.set(state = False, iqConnector = repcap.IqConnector.Default) \n
		Activates the impairment or correction values LEAKage, QUADrature and IQRatio for the corresponding stream. \n
			:param state: 1| ON| 0| OFF
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
		"""
		param = Conversions.bool_to_str(state)
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		self._core.io.write(f'SOURce:BB:IMPairment:IQOutput{iqConnector_cmd_val}:STATe {param}')

	def get(self, iqConnector=repcap.IqConnector.Default) -> bool:
		"""SCPI: [SOURce]:BB:IMPairment:IQOutput<CH>:STATe \n
		Snippet: value: bool = driver.source.bb.impairment.iqOutput.state.get(iqConnector = repcap.IqConnector.Default) \n
		Activates the impairment or correction values LEAKage, QUADrature and IQRatio for the corresponding stream. \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
			:return: state: 1| ON| 0| OFF"""
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		response = self._core.io.query_str(f'SOURce:BB:IMPairment:IQOutput{iqConnector_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
