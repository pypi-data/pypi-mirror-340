from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CheckCls:
	"""Check commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("check", core, parent)

	def get(self, iqConnector=repcap.IqConnector.Default) -> List[str]:
		"""SCPI: SCONfiguration:EXTernal:IQOutput<CH>:CONNections:CHECk \n
		Snippet: value: List[str] = driver.sconfiguration.external.iqOutput.connections.check.get(iqConnector = repcap.IqConnector.Default) \n
		Queries the status of the required connections between the R&S SMW200A and the R&S SZU. R&S SZU is connected to the R&S
		SMW200A via USB. \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
			:return: ipartd_pi_db_ext_dev_conn_check: No help available"""
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:IQOutput{iqConnector_cmd_val}:CONNections:CHECk?')
		return Conversions.str_to_str_list(response)
