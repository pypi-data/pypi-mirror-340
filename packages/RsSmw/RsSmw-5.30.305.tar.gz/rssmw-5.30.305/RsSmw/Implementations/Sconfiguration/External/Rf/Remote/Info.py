from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InfoCls:
	"""Info commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("info", core, parent)

	def get(self, path=repcap.Path.Default) -> List[str]:
		"""SCPI: SCONfiguration:EXTernal:RF<CH>:REMote:INFO \n
		Snippet: value: List[str] = driver.sconfiguration.external.rf.remote.info.get(path = repcap.Path.Default) \n
		Queries information on the external instrument. \n
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: id_pi_db_ext_dev_rem_inst_info: No help available"""
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:RF{path_cmd_val}:REMote:INFO?')
		return Conversions.str_to_str_list(response)
