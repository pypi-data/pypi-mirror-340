from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Utilities import trim_str_response
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InameCls:
	"""Iname commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iname", core, parent)

	def get(self, path=repcap.Path.Default) -> str:
		"""SCPI: SCONfiguration:EXTernal:RF<CH>:INAMe \n
		Snippet: value: str = driver.sconfiguration.external.rf.iname.get(path = repcap.Path.Default) \n
		Queries the name of the connected external instrument. \n
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: instr_name: string Returns the name of the connected external instrument. InstrmentName (SerialNumber) Path the instrument name, as retrieved via the DIG I/Q interface InstrmentName[, RfPath] or InstrmentName (SerialNumber) the instrument name, as defined in with the 'Remote Config' settings or as defined by the command method RsSmw.Sconfiguration.External.Remote.Add.set"""
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:RF{path_cmd_val}:INAMe?')
		return trim_str_response(response)
