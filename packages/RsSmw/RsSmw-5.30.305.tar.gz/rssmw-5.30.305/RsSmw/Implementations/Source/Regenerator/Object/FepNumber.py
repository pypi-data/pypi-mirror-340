from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FepNumberCls:
	"""FepNumber commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fepNumber", core, parent)

	def get(self, objectIx=repcap.ObjectIx.Default) -> int:
		"""SCPI: [SOURce<HW>]:REGenerator:OBJect<CH>:FEPNumber \n
		Snippet: value: int = driver.source.regenerator.object.fepNumber.get(objectIx = repcap.ObjectIx.Default) \n
		Queries the number of the first pulse for that an echo signal is generated. \n
			:param objectIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Object')
			:return: first_echo_to_puls: integer Range: 0 to 100E6"""
		objectIx_cmd_val = self._cmd_group.get_repcap_cmd_value(objectIx, repcap.ObjectIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:REGenerator:OBJect{objectIx_cmd_val}:FEPNumber?')
		return Conversions.str_to_int(response)
