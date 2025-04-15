from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MacCls:
	"""Mac commands group definition. 25 total commands, 5 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mac", core, parent)

	@property
	def address(self):
		"""address commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_address'):
			from .Address import AddressCls
			self._address = AddressCls(self._core, self._cmd_group)
		return self._address

	@property
	def fcontrol(self):
		"""fcontrol commands group. 0 Sub-classes, 13 commands."""
		if not hasattr(self, '_fcontrol'):
			from .Fcontrol import FcontrolCls
			self._fcontrol = FcontrolCls(self._core, self._cmd_group)
		return self._fcontrol

	@property
	def fcs(self):
		"""fcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fcs'):
			from .Fcs import FcsCls
			self._fcs = FcsCls(self._core, self._cmd_group)
		return self._fcs

	@property
	def qsControl(self):
		"""qsControl commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_qsControl'):
			from .QsControl import QsControlCls
			self._qsControl = QsControlCls(self._core, self._cmd_group)
		return self._qsControl

	@property
	def scontrol(self):
		"""scontrol commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_scontrol'):
			from .Scontrol import ScontrolCls
			self._scontrol = ScontrolCls(self._core, self._cmd_group)
		return self._scontrol

	def get_did(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:DID \n
		Snippet: value: str = driver.source.bb.wlad.pconfig.mac.get_did() \n
		Sets the value of the duration ID field. Depending on the frame type, the 2-byte field Duration/ID is used to transmit
		the association identity of the station transmitting the frame or it indicates the duration assigned to the frame type.
		Exactly 16 bit must be entered. \n
			:return: did: 16 bits
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:DID?')
		return trim_str_response(response)

	def set_did(self, did: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:DID \n
		Snippet: driver.source.bb.wlad.pconfig.mac.set_did(did = rawAbc) \n
		Sets the value of the duration ID field. Depending on the frame type, the 2-byte field Duration/ID is used to transmit
		the association identity of the station transmitting the frame or it indicates the duration assigned to the frame type.
		Exactly 16 bit must be entered. \n
			:param did: 16 bits
		"""
		param = Conversions.value_to_str(did)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:DID {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:STATe \n
		Snippet: value: bool = driver.source.bb.wlad.pconfig.mac.get_state() \n
		Activates/deactivates the generation of the MAC Header. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:STATe \n
		Snippet: driver.source.bb.wlad.pconfig.mac.set_state(state = False) \n
		Activates/deactivates the generation of the MAC Header. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:STATe {param}')

	def clone(self) -> 'MacCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MacCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
