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

	def get(self, path=repcap.Path.Default) -> bool:
		"""SCPI: SCONfiguration:EXTernal:RF<CH>:RCONnection:STATe \n
		Snippet: value: bool = driver.sconfiguration.external.rf.rconnection.state.get(path = repcap.Path.Default) \n
		Queries the status of the remote connection. \n
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: state: 1| ON| 0| OFF"""
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:RF{path_cmd_val}:RCONnection:STATe?')
		return Conversions.str_to_bool(response)
