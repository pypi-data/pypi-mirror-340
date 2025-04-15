from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePyCls:
	"""TypePy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("typePy", core, parent)

	# noinspection PyTypeChecker
	def get(self, externalDevice=repcap.ExternalDevice.Default) -> enums.DevType:
		"""SCPI: [SOURce<HW>]:EFRontend:EXTDevice<ID>:TYPE \n
		Snippet: value: enums.DevType = driver.source.efrontend.extDevice.typePy.get(externalDevice = repcap.ExternalDevice.Default) \n
		Queries the type of the connected external device. \n
			:param externalDevice: optional repeated capability selector. Default value: Nr1 (settable in the interface 'ExtDevice')
			:return: type_py: FILTer| AMPLifier| ATTenuator| NONE FILTer A filter is connected to the frontend as external device. AMPLifier An amplifier is connected to the frontend as external device. ATTenuator An attenuator is connected to the frontend as external device. NONE No external device is connected to the frontend."""
		externalDevice_cmd_val = self._cmd_group.get_repcap_cmd_value(externalDevice, repcap.ExternalDevice)
		response = self._core.io.query_str(f'SOURce<HwInstance>:EFRontend:EXTDevice{externalDevice_cmd_val}:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.DevType)
