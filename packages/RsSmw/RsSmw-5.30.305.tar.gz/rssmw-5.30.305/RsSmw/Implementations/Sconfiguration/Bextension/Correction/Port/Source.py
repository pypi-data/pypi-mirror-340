from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	def get(self, port=repcap.Port.Default) -> str:
		"""SCPI: SCONfiguration:BEXTension:CORRection:PORT<CH>:SOURce \n
		Snippet: value: str = driver.sconfiguration.bextension.correction.port.source.get(port = repcap.Port.Default) \n
		Queries the RF source of the RF port. \n
			:param port: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Port')
			:return: rf_source_name: string"""
		port_cmd_val = self._cmd_group.get_repcap_cmd_value(port, repcap.Port)
		response = self._core.io.query_str(f'SCONfiguration:BEXTension:CORRection:PORT{port_cmd_val}:SOURce?')
		return trim_str_response(response)
