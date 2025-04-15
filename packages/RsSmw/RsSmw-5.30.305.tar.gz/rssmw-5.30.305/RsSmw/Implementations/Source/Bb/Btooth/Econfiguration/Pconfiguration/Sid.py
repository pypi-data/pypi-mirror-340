from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SidCls:
	"""Sid commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sid", core, parent)

	def set(self, sid: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SID \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.sid.set(sid = rawAbc, bitcount = 1) \n
		Specifies the SID in the CtrData field of the LL_PERIODIC_SYNC_IND. \n
			:param sid: numeric
			:param bitcount: integer Range: 4 to 4
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sid', sid, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SID {param}'.rstrip())

	# noinspection PyTypeChecker
	class SidStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Sid: str: numeric
			- 2 Bitcount: int: integer Range: 4 to 4"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Sid'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sid: str = None
			self.Bitcount: int = None

	def get(self) -> SidStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SID \n
		Snippet: value: SidStruct = driver.source.bb.btooth.econfiguration.pconfiguration.sid.get() \n
		Specifies the SID in the CtrData field of the LL_PERIODIC_SYNC_IND. \n
			:return: structure: for return value, see the help for SidStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SID?', self.__class__.SidStruct())
