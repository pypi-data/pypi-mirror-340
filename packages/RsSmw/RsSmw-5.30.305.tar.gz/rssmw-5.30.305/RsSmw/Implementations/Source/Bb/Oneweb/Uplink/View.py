from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ViewCls:
	"""View commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("view", core, parent)

	# noinspection PyTypeChecker
	def get_cindex(self) -> enums.OneWebCcIndex:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:VIEW:CINDex \n
		Snippet: value: enums.OneWebCcIndex = driver.source.bb.oneweb.uplink.view.get_cindex() \n
		No command help available \n
			:return: dl_tp_cell_idx: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:UL:VIEW:CINDex?')
		return Conversions.str_to_scalar_enum(response, enums.OneWebCcIndex)

	def set_cindex(self, dl_tp_cell_idx: enums.OneWebCcIndex) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:VIEW:CINDex \n
		Snippet: driver.source.bb.oneweb.uplink.view.set_cindex(dl_tp_cell_idx = enums.OneWebCcIndex.PC) \n
		No command help available \n
			:param dl_tp_cell_idx: No help available
		"""
		param = Conversions.enum_scalar_to_str(dl_tp_cell_idx, enums.OneWebCcIndex)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:UL:VIEW:CINDex {param}')

	def get_fsts(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:VIEW:FSTS \n
		Snippet: value: int = driver.source.bb.oneweb.uplink.view.get_fsts() \n
		No command help available \n
			:return: fsts: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:UL:VIEW:FSTS?')
		return Conversions.str_to_int(response)

	def set_fsts(self, fsts: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:VIEW:FSTS \n
		Snippet: driver.source.bb.oneweb.uplink.view.set_fsts(fsts = 1) \n
		No command help available \n
			:param fsts: No help available
		"""
		param = Conversions.decimal_value_to_str(fsts)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:UL:VIEW:FSTS {param}')

	def get_viss(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:VIEW:VISS \n
		Snippet: value: int = driver.source.bb.oneweb.uplink.view.get_viss() \n
		No command help available \n
			:return: viss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:UL:VIEW:VISS?')
		return Conversions.str_to_int(response)

	def set_viss(self, viss: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:VIEW:VISS \n
		Snippet: driver.source.bb.oneweb.uplink.view.set_viss(viss = 1) \n
		No command help available \n
			:param viss: No help available
		"""
		param = Conversions.decimal_value_to_str(viss)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:UL:VIEW:VISS {param}')
