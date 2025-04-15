from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	def set(self, fid: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBX:GHConfig:FID:PATTern \n
		Snippet: driver.source.bb.dvb.dvbx.ghConfig.fid.pattern.set(fid = rawAbc, bitcount = 1) \n
		Sets the PDU fragment ID. \n
			:param fid: numeric
			:param bitcount: integer Range: 8 to 8
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('fid', fid, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBX:GHConfig:FID:PATTern {param}'.rstrip())

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Fid: str: numeric
			- 2 Bitcount: int: integer Range: 8 to 8"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Fid'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Fid: str = None
			self.Bitcount: int = None

	def get(self) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBX:GHConfig:FID:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.dvb.dvbx.ghConfig.fid.pattern.get() \n
		Sets the PDU fragment ID. \n
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:DVB:DVBX:GHConfig:FID:PATTern?', self.__class__.PatternStruct())
