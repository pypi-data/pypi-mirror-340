from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ViewCls:
	"""View commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("view", core, parent)

	def get_bis(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:V5G:UL:VIEW:BIS \n
		Snippet: value: bool = driver.source.bb.v5G.uplink.view.get_bis() \n
		No command help available \n
			:return: block_info: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:V5G:UL:VIEW:BIS?')
		return Conversions.str_to_bool(response)

	def set_bis(self, block_info: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:UL:VIEW:BIS \n
		Snippet: driver.source.bb.v5G.uplink.view.set_bis(block_info = False) \n
		No command help available \n
			:param block_info: No help available
		"""
		param = Conversions.bool_to_str(block_info)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:UL:VIEW:BIS {param}')

	# noinspection PyTypeChecker
	def get_cindex(self) -> enums.CcIndex:
		"""SCPI: [SOURce<HW>]:BB:V5G:UL:VIEW:CINDex \n
		Snippet: value: enums.CcIndex = driver.source.bb.v5G.uplink.view.get_cindex() \n
		No command help available \n
			:return: dl_tp_cell_idx: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:V5G:UL:VIEW:CINDex?')
		return Conversions.str_to_scalar_enum(response, enums.CcIndex)

	def set_cindex(self, dl_tp_cell_idx: enums.CcIndex) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:UL:VIEW:CINDex \n
		Snippet: driver.source.bb.v5G.uplink.view.set_cindex(dl_tp_cell_idx = enums.CcIndex.PC) \n
		No command help available \n
			:param dl_tp_cell_idx: No help available
		"""
		param = Conversions.enum_scalar_to_str(dl_tp_cell_idx, enums.CcIndex)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:UL:VIEW:CINDex {param}')

	def get_fsts(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:V5G:UL:VIEW:FSTS \n
		Snippet: value: float = driver.source.bb.v5G.uplink.view.get_fsts() \n
		No command help available \n
			:return: fsts: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:V5G:UL:VIEW:FSTS?')
		return Conversions.str_to_float(response)

	def set_fsts(self, fsts: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:UL:VIEW:FSTS \n
		Snippet: driver.source.bb.v5G.uplink.view.set_fsts(fsts = 1.0) \n
		No command help available \n
			:param fsts: No help available
		"""
		param = Conversions.decimal_value_to_str(fsts)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:UL:VIEW:FSTS {param}')

	def get_viss(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:V5G:UL:VIEW:VISS \n
		Snippet: value: float = driver.source.bb.v5G.uplink.view.get_viss() \n
		No command help available \n
			:return: viss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:V5G:UL:VIEW:VISS?')
		return Conversions.str_to_float(response)

	def set_viss(self, viss: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:UL:VIEW:VISS \n
		Snippet: driver.source.bb.v5G.uplink.view.set_viss(viss = 1.0) \n
		No command help available \n
			:param viss: No help available
		"""
		param = Conversions.decimal_value_to_str(viss)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:UL:VIEW:VISS {param}')
