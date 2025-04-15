from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DetectCls:
	"""Detect commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("detect", core, parent)

	def get(self, iqConnector=repcap.IqConnector.Default) -> str:
		"""SCPI: SCONfiguration:EXTernal:BBMM<CH>:REMote:DETect \n
		Snippet: value: str = driver.sconfiguration.external.bbmm.remote.detect.get(iqConnector = repcap.IqConnector.Default) \n
		Searches for external instruments connected to the particular digital interfaces. \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bbmm')
			:return: detected_instr: string If the detection fails, the query returns 'None'."""
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:BBMM{iqConnector_cmd_val}:REMote:DETect?')
		return trim_str_response(response)
