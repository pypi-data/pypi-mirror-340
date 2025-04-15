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

	def get(self, digitalIq=repcap.DigitalIq.Default) -> str:
		"""SCPI: SCONfiguration:EXTernal:FADer<CH>:REMote:DETect \n
		Snippet: value: str = driver.sconfiguration.external.fader.remote.detect.get(digitalIq = repcap.DigitalIq.Default) \n
		Searches for external instruments connected to the particular digital interfaces. \n
			:param digitalIq: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fader')
			:return: detected_instr: string If the detection fails, the query returns 'None'."""
		digitalIq_cmd_val = self._cmd_group.get_repcap_cmd_value(digitalIq, repcap.DigitalIq)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:FADer{digitalIq_cmd_val}:REMote:DETect?')
		return trim_str_response(response)
