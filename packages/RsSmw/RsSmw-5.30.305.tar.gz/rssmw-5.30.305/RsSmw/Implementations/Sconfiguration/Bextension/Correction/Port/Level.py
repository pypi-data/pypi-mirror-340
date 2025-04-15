from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LevelCls:
	"""Level commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	def get(self, port=repcap.Port.Default) -> float:
		"""SCPI: SCONfiguration:BEXTension:CORRection:PORT<CH>:LEVel \n
		Snippet: value: float = driver.sconfiguration.bextension.correction.port.level.get(port = repcap.Port.Default) \n
		Queries the power level of the RF signal at the selected RF port. \n
			:param port: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Port')
			:return: level: float"""
		port_cmd_val = self._cmd_group.get_repcap_cmd_value(port, repcap.Port)
		response = self._core.io.query_str(f'SCONfiguration:BEXTension:CORRection:PORT{port_cmd_val}:LEVel?')
		return Conversions.str_to_float(response)
