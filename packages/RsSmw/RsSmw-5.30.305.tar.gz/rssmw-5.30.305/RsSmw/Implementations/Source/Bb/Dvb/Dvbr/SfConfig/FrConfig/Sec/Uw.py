from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UwCls:
	"""Uw commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("uw", core, parent)

	def set(self, uw: str, bitcount: int, sfCfgIxNull=repcap.SfCfgIxNull.Default, frCfgIxNull=repcap.FrCfgIxNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBR:SFConfig<CH0>:FRConfig<ST0>:SEC<DI0>:UW \n
		Snippet: driver.source.bb.dvb.dvbr.sfConfig.frConfig.sec.uw.set(uw = rawAbc, bitcount = 1, sfCfgIxNull = repcap.SfCfgIxNull.Default, frCfgIxNull = repcap.FrCfgIxNull.Default, indexNull = repcap.IndexNull.Default) \n
		Queries the content of the unique word (UW) . \n
			:param uw: numeric
			:param bitcount: integer Range: 1 to 512
			:param sfCfgIxNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'SfConfig')
			:param frCfgIxNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'FrConfig')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sec')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('uw', uw, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		sfCfgIxNull_cmd_val = self._cmd_group.get_repcap_cmd_value(sfCfgIxNull, repcap.SfCfgIxNull)
		frCfgIxNull_cmd_val = self._cmd_group.get_repcap_cmd_value(frCfgIxNull, repcap.FrCfgIxNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBR:SFConfig{sfCfgIxNull_cmd_val}:FRConfig{frCfgIxNull_cmd_val}:SEC{indexNull_cmd_val}:UW {param}'.rstrip())

	# noinspection PyTypeChecker
	class UwStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Uw: str: numeric
			- 2 Bitcount: int: integer Range: 1 to 512"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Uw'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Uw: str = None
			self.Bitcount: int = None

	def get(self, sfCfgIxNull=repcap.SfCfgIxNull.Default, frCfgIxNull=repcap.FrCfgIxNull.Default, indexNull=repcap.IndexNull.Default) -> UwStruct:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBR:SFConfig<CH0>:FRConfig<ST0>:SEC<DI0>:UW \n
		Snippet: value: UwStruct = driver.source.bb.dvb.dvbr.sfConfig.frConfig.sec.uw.get(sfCfgIxNull = repcap.SfCfgIxNull.Default, frCfgIxNull = repcap.FrCfgIxNull.Default, indexNull = repcap.IndexNull.Default) \n
		Queries the content of the unique word (UW) . \n
			:param sfCfgIxNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'SfConfig')
			:param frCfgIxNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'FrConfig')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sec')
			:return: structure: for return value, see the help for UwStruct structure arguments."""
		sfCfgIxNull_cmd_val = self._cmd_group.get_repcap_cmd_value(sfCfgIxNull, repcap.SfCfgIxNull)
		frCfgIxNull_cmd_val = self._cmd_group.get_repcap_cmd_value(frCfgIxNull, repcap.FrCfgIxNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:DVB:DVBR:SFConfig{sfCfgIxNull_cmd_val}:FRConfig{frCfgIxNull_cmd_val}:SEC{indexNull_cmd_val}:UW?', self.__class__.UwStruct())
