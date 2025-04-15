from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AdditionalCls:
	"""Additional commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("additional", core, parent)

	def set(self, additional_delay: float, port=repcap.Port.Default) -> None:
		"""SCPI: SCONfiguration:BEXTension:CORRection:PORT<CH>:IQDelay:ADDitional \n
		Snippet: driver.sconfiguration.bextension.correction.port.iqDelay.additional.set(additional_delay = 1.0, port = repcap.Port.Default) \n
		Sets an additional IQ delay as an offset to the current IQ delay at the selected RF port. \n
			:param additional_delay: float Range: 0 to 1E-9
			:param port: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Port')
		"""
		param = Conversions.decimal_value_to_str(additional_delay)
		port_cmd_val = self._cmd_group.get_repcap_cmd_value(port, repcap.Port)
		self._core.io.write(f'SCONfiguration:BEXTension:CORRection:PORT{port_cmd_val}:IQDelay:ADDitional {param}')

	def get(self, port=repcap.Port.Default) -> float:
		"""SCPI: SCONfiguration:BEXTension:CORRection:PORT<CH>:IQDelay:ADDitional \n
		Snippet: value: float = driver.sconfiguration.bextension.correction.port.iqDelay.additional.get(port = repcap.Port.Default) \n
		Sets an additional IQ delay as an offset to the current IQ delay at the selected RF port. \n
			:param port: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Port')
			:return: additional_delay: float Range: 0 to 1E-9"""
		port_cmd_val = self._cmd_group.get_repcap_cmd_value(port, repcap.Port)
		response = self._core.io.query_str(f'SCONfiguration:BEXTension:CORRection:PORT{port_cmd_val}:IQDelay:ADDitional?')
		return Conversions.str_to_float(response)
