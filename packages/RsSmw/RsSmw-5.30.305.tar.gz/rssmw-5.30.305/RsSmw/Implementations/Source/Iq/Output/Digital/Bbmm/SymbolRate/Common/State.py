from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, dig_iq_hs_com_state: bool, iqConnector=repcap.IqConnector.Default) -> None:
		"""SCPI: [SOURce]:IQ:OUTPut:DIGital:BBMM<CH>:SRATe:COMMon:STATe \n
		Snippet: driver.source.iq.output.digital.bbmm.symbolRate.common.state.set(dig_iq_hs_com_state = False, iqConnector = repcap.IqConnector.Default) \n
		If enabled, the same sample rate value is applied to all channels. \n
			:param dig_iq_hs_com_state: 1| ON| 0| OFF
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bbmm')
		"""
		param = Conversions.bool_to_str(dig_iq_hs_com_state)
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		self._core.io.write(f'SOURce:IQ:OUTPut:DIGital:BBMM{iqConnector_cmd_val}:SRATe:COMMon:STATe {param}')

	def get(self, iqConnector=repcap.IqConnector.Default) -> bool:
		"""SCPI: [SOURce]:IQ:OUTPut:DIGital:BBMM<CH>:SRATe:COMMon:STATe \n
		Snippet: value: bool = driver.source.iq.output.digital.bbmm.symbolRate.common.state.get(iqConnector = repcap.IqConnector.Default) \n
		If enabled, the same sample rate value is applied to all channels. \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bbmm')
			:return: dig_iq_hs_com_state: 1| ON| 0| OFF"""
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		response = self._core.io.query_str(f'SOURce:IQ:OUTPut:DIGital:BBMM{iqConnector_cmd_val}:SRATe:COMMon:STATe?')
		return Conversions.str_to_bool(response)
