from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PhaseCls:
	"""Phase commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("phase", core, parent)

	def set(self, carrier_index: int, phase: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:MCCW:CARRier:PHASe \n
		Snippet: driver.source.bb.mccw.carrier.phase.set(carrier_index = 1, phase = 1.0) \n
		For disabled optimization of the crest factor, sets the start phase of the selected carrier. \n
			:param carrier_index: integer Range: 0 to lastCarrier
			:param phase: float Range: 0 to 359.99, Unit: DEG
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('carrier_index', carrier_index, DataType.Integer), ArgSingle('phase', phase, DataType.Float))
		self._core.io.write(f'SOURce<HwInstance>:BB:MCCW:CARRier:PHASe {param}'.rstrip())

	# noinspection PyTypeChecker
	class PhaseStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Carrier_Index: int: integer Range: 0 to lastCarrier
			- 2 Phase: float: float Range: 0 to 359.99, Unit: DEG"""
		__meta_args_list = [
			ArgStruct.scalar_int('Carrier_Index'),
			ArgStruct.scalar_float('Phase')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Carrier_Index: int = None
			self.Phase: float = None

	def get(self) -> PhaseStruct:
		"""SCPI: [SOURce<HW>]:BB:MCCW:CARRier:PHASe \n
		Snippet: value: PhaseStruct = driver.source.bb.mccw.carrier.phase.get() \n
		For disabled optimization of the crest factor, sets the start phase of the selected carrier. \n
			:return: structure: for return value, see the help for PhaseStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:MCCW:CARRier:PHASe?', self.__class__.PhaseStruct())
