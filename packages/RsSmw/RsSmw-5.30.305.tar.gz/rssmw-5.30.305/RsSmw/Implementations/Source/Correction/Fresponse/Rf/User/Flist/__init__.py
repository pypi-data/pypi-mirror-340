from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FlistCls:
	"""Flist commands group definition. 7 total commands, 3 Subgroups, 4 group commands
	Repeated Capability: Index, default value after init: Index.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("flist", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_index_get', 'repcap_index_set', repcap.Index.Nr1)

	def repcap_index_set(self, index: repcap.Index) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Index.Default.
		Default value after init: Index.Nr1"""
		self._cmd_group.set_repcap_enum_value(index)

	def repcap_index_get(self) -> repcap.Index:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def magnitude(self):
		"""magnitude commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_magnitude'):
			from .Magnitude import MagnitudeCls
			self._magnitude = MagnitudeCls(self._core, self._cmd_group)
		return self._magnitude

	@property
	def phase(self):
		"""phase commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_phase'):
			from .Phase import PhaseCls
			self._phase = PhaseCls(self._core, self._cmd_group)
		return self._phase

	@property
	def select(self):
		"""select commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_select'):
			from .Select import SelectCls
			self._select = SelectCls(self._core, self._cmd_group)
		return self._select

	def get_catalog(self) -> str:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:FLISt:CATalog \n
		Snippet: value: str = driver.source.correction.fresponse.rf.user.flist.get_catalog() \n
		Deletes all entries in the list. \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:USER:FLISt:CATalog?')
		return trim_str_response(response)

	def clear(self) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:FLISt:CLEar \n
		Snippet: driver.source.correction.fresponse.rf.user.flist.clear() \n
		Deletes all entries in the list. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:FLISt:CLEar')

	def clear_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:FLISt:CLEar \n
		Snippet: driver.source.correction.fresponse.rf.user.flist.clear_with_opc() \n
		Deletes all entries in the list. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:FLISt:CLEar', opc_timeout_ms)

	def get_size(self) -> int:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:FLISt:SIZE \n
		Snippet: value: int = driver.source.correction.fresponse.rf.user.flist.get_size() \n
		Deletes all entries in the list. \n
			:return: freq_resp_rf_fli_si: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:USER:FLISt:SIZE?')
		return Conversions.str_to_int(response)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:FLISt:[STATe] \n
		Snippet: value: bool = driver.source.correction.fresponse.rf.user.flist.get_state() \n
		Uses FR list files for user-defined corrections. Load the FR lists, enable them and apply the configuration with the
		corresponding FR list commands. \n
			:return: freq_corr_rf_fl_sta: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:USER:FLISt:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, freq_corr_rf_fl_sta: bool) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:FLISt:[STATe] \n
		Snippet: driver.source.correction.fresponse.rf.user.flist.set_state(freq_corr_rf_fl_sta = False) \n
		Uses FR list files for user-defined corrections. Load the FR lists, enable them and apply the configuration with the
		corresponding FR list commands. \n
			:param freq_corr_rf_fl_sta: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(freq_corr_rf_fl_sta)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:FLISt:STATe {param}')

	def clone(self) -> 'FlistCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FlistCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
