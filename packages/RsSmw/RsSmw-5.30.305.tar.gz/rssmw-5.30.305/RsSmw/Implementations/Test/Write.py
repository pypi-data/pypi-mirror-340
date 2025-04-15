from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class WriteCls:
	"""Write commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("write", core, parent)

	def set_result(self, result: enums.SelftLevWrite) -> None:
		"""SCPI: TEST:WRITe:RESult \n
		Snippet: driver.test.write.set_result(result = enums.SelftLevWrite.CUSTomer) \n
		No command help available \n
			:param result: No help available
		"""
		param = Conversions.enum_scalar_to_str(result, enums.SelftLevWrite)
		self._core.io.write(f'TEST:WRITe:RESult {param}')
