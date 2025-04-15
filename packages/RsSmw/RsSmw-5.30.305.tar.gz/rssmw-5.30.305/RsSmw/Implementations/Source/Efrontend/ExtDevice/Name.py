from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Utilities import trim_str_response
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NameCls:
	"""Name commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("name", core, parent)

	def get(self, externalDevice=repcap.ExternalDevice.Default) -> str:
		"""SCPI: [SOURce<HW>]:EFRontend:EXTDevice<ID>:NAME \n
		Snippet: value: str = driver.source.efrontend.extDevice.name.get(externalDevice = repcap.ExternalDevice.Default) \n
		Queries the name of the connected external device. \n
			:param externalDevice: optional repeated capability selector. Default value: Nr1 (settable in the interface 'ExtDevice')
			:return: device_name: string"""
		externalDevice_cmd_val = self._cmd_group.get_repcap_cmd_value(externalDevice, repcap.ExternalDevice)
		response = self._core.io.query_str(f'SOURce<HwInstance>:EFRontend:EXTDevice{externalDevice_cmd_val}:NAME?')
		return trim_str_response(response)
