from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IselectCls:
	"""Iselect commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iselect", core, parent)

	def set(self, instr_name: str, rf_path: str = None, index=repcap.Index.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:HSDigital<CH>:REMote:ISELect \n
		Snippet: driver.sconfiguration.external.hsDigital.remote.iselect.set(instr_name = 'abc', rf_path = 'abc', index = repcap.Index.Default) \n
		No command help available \n
			:param instr_name: No help available
			:param rf_path: No help available
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'HsDigital')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('instr_name', instr_name, DataType.String), ArgSingle('rf_path', rf_path, DataType.String, None, is_optional=True))
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SCONfiguration:EXTernal:HSDigital{index_cmd_val}:REMote:ISELect {param}'.rstrip())

	# noinspection PyTypeChecker
	class IselectStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Instr_Name: str: No parameter help available
			- 2 Rf_Path: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_str('Instr_Name'),
			ArgStruct.scalar_str('Rf_Path')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Instr_Name: str = None
			self.Rf_Path: str = None

	def get(self, index=repcap.Index.Default) -> IselectStruct:
		"""SCPI: SCONfiguration:EXTernal:HSDigital<CH>:REMote:ISELect \n
		Snippet: value: IselectStruct = driver.sconfiguration.external.hsDigital.remote.iselect.get(index = repcap.Index.Default) \n
		No command help available \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'HsDigital')
			:return: structure: for return value, see the help for IselectStruct structure arguments."""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		return self._core.io.query_struct(f'SCONfiguration:EXTernal:HSDigital{index_cmd_val}:REMote:ISELect?', self.__class__.IselectStruct())
