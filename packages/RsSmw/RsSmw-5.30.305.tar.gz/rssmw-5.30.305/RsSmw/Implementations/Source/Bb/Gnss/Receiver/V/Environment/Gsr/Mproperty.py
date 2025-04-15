from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MpropertyCls:
	"""Mproperty commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mproperty", core, parent)

	def set(self, material_propert: enums.MatProp, vehicle=repcap.Vehicle.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:GSR:MPRoperty \n
		Snippet: driver.source.bb.gnss.receiver.v.environment.gsr.mproperty.set(material_propert = enums.MatProp.PERM, vehicle = repcap.Vehicle.Default) \n
		Specifies, if the material is defined by its permittivity/conductivity or by its power loss characteristic. \n
			:param material_propert: PLOSS| PERM
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
		"""
		param = Conversions.enum_scalar_to_str(material_propert, enums.MatProp)
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:ENVironment:GSR:MPRoperty {param}')

	# noinspection PyTypeChecker
	def get(self, vehicle=repcap.Vehicle.Default) -> enums.MatProp:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:GSR:MPRoperty \n
		Snippet: value: enums.MatProp = driver.source.bb.gnss.receiver.v.environment.gsr.mproperty.get(vehicle = repcap.Vehicle.Default) \n
		Specifies, if the material is defined by its permittivity/conductivity or by its power loss characteristic. \n
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: material_propert: PLOSS| PERM"""
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:ENVironment:GSR:MPRoperty?')
		return Conversions.str_to_scalar_enum(response, enums.MatProp)
