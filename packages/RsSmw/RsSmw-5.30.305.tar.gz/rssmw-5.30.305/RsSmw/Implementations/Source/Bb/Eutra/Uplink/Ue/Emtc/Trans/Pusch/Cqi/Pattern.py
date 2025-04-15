from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal.Types import DataType
from ...........Internal.StructBase import StructBase
from ...........Internal.ArgStruct import ArgStruct
from ...........Internal.ArgSingleList import ArgSingleList
from ...........Internal.ArgSingle import ArgSingle
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	def set(self, emtc_cqi_pat: str, bitcount: int, userEquipment=repcap.UserEquipment.Default, transmission=repcap.Transmission.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:EMTC:TRANs<CH>:PUSCh:CQI:PATTern \n
		Snippet: driver.source.bb.eutra.uplink.ue.emtc.trans.pusch.cqi.pattern.set(emtc_cqi_pat = rawAbc, bitcount = 1, userEquipment = repcap.UserEquipment.Default, transmission = repcap.Transmission.Default) \n
		Sets the CQI pattern for the PUSCH. The length of the pattern is determined by the number of CQI bits as set with the
		command [:SOURce<hw>]:BB:EUTRa:UL:UE<st>:EMTC:TRANs<ch>:PUSCh:CQI:BITS. \n
			:param emtc_cqi_pat: numeric
			:param bitcount: integer Range: 1 to 1024
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param transmission: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('emtc_cqi_pat', emtc_cqi_pat, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		transmission_cmd_val = self._cmd_group.get_repcap_cmd_value(transmission, repcap.Transmission)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{userEquipment_cmd_val}:EMTC:TRANs{transmission_cmd_val}:PUSCh:CQI:PATTern {param}'.rstrip())

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Emtc_Cqi_Pat: str: numeric
			- 2 Bitcount: int: integer Range: 1 to 1024"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Emtc_Cqi_Pat'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Emtc_Cqi_Pat: str = None
			self.Bitcount: int = None

	def get(self, userEquipment=repcap.UserEquipment.Default, transmission=repcap.Transmission.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:EMTC:TRANs<CH>:PUSCh:CQI:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.eutra.uplink.ue.emtc.trans.pusch.cqi.pattern.get(userEquipment = repcap.UserEquipment.Default, transmission = repcap.Transmission.Default) \n
		Sets the CQI pattern for the PUSCH. The length of the pattern is determined by the number of CQI bits as set with the
		command [:SOURce<hw>]:BB:EUTRa:UL:UE<st>:EMTC:TRANs<ch>:PUSCh:CQI:BITS. \n
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param transmission: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		transmission_cmd_val = self._cmd_group.get_repcap_cmd_value(transmission, repcap.Transmission)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{userEquipment_cmd_val}:EMTC:TRANs{transmission_cmd_val}:PUSCh:CQI:PATTern?', self.__class__.PatternStruct())
