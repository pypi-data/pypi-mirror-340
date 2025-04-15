from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NpatternCls:
	"""Npattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("npattern", core, parent)

	def set(self, notif_pattern: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:NPATtern \n
		Snippet: driver.source.bb.eutra.downlink.mbsfn.ai.mcch.npattern.set(notif_pattern = rawAbc, bitcount = 1) \n
		Sets the pattern for the notification bits sent on PDCCH DCI format 1c. \n
			:param notif_pattern: numeric
			:param bitcount: integer Range: 1 to 64
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('notif_pattern', notif_pattern, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:NPATtern {param}'.rstrip())

	# noinspection PyTypeChecker
	class NpatternStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Notif_Pattern: str: numeric
			- 2 Bitcount: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Notif_Pattern'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Notif_Pattern: str = None
			self.Bitcount: int = None

	def get(self) -> NpatternStruct:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:NPATtern \n
		Snippet: value: NpatternStruct = driver.source.bb.eutra.downlink.mbsfn.ai.mcch.npattern.get() \n
		Sets the pattern for the notification bits sent on PDCCH DCI format 1c. \n
			:return: structure: for return value, see the help for NpatternStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:NPATtern?', self.__class__.NpatternStruct())
