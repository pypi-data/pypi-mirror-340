from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReleaseCls:
	"""Release commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("release", core, parent)

	def set(self, release: enums.UeRelease, userEquipment=repcap.UserEquipment.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:RELease \n
		Snippet: driver.source.bb.eutra.uplink.ue.release.set(release = enums.UeRelease.EMTC, userEquipment = repcap.UserEquipment.Default) \n
		Sets which LTE release version the UE supports. \n
			:param release: R89| LADV | EMTC| NIOT
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
		"""
		param = Conversions.enum_scalar_to_str(release, enums.UeRelease)
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{userEquipment_cmd_val}:RELease {param}')

	# noinspection PyTypeChecker
	def get(self, userEquipment=repcap.UserEquipment.Default) -> enums.UeRelease:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:RELease \n
		Snippet: value: enums.UeRelease = driver.source.bb.eutra.uplink.ue.release.get(userEquipment = repcap.UserEquipment.Default) \n
		Sets which LTE release version the UE supports. \n
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: release: R89| LADV | EMTC| NIOT"""
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{userEquipment_cmd_val}:RELease?')
		return Conversions.str_to_scalar_enum(response, enums.UeRelease)
