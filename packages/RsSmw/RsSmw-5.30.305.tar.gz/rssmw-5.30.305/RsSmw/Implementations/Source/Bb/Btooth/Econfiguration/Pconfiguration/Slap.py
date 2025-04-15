from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SlapCls:
	"""Slap commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("slap", core, parent)

	def set(self, lap: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SLAP \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.slap.set(lap = rawAbc, bitcount = 1) \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner's or
		initiator's target device address to which the advertisement is directed ..:TLAP. \n
			:param lap: numeric
			:param bitcount: integer Range: 24 to 24
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('lap', lap, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SLAP {param}'.rstrip())

	# noinspection PyTypeChecker
	class SlapStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Lap: str: numeric
			- 2 Bitcount: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Lap'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lap: str = None
			self.Bitcount: int = None

	def get(self) -> SlapStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SLAP \n
		Snippet: value: SlapStruct = driver.source.bb.btooth.econfiguration.pconfiguration.slap.get() \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner's or
		initiator's target device address to which the advertisement is directed ..:TLAP. \n
			:return: structure: for return value, see the help for SlapStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SLAP?', self.__class__.SlapStruct())
