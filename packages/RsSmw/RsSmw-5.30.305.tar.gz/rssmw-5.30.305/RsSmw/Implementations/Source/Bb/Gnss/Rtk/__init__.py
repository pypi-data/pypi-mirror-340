from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RtkCls:
	"""Rtk commands group definition. 30 total commands, 2 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rtk", core, parent)

	@property
	def base(self):
		"""base commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_base'):
			from .Base import BaseCls
			self._base = BaseCls(self._core, self._cmd_group)
		return self._base

	@property
	def bstation(self):
		"""bstation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bstation'):
			from .Bstation import BstationCls
			self._bstation = BstationCls(self._core, self._cmd_group)
		return self._bstation

	def get_password(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:PASSword \n
		Snippet: value: str = driver.source.bb.gnss.rtk.get_password() \n
		Queries the password, that belongs to the RTCM user name. \n
			:return: password: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:RTK:PASSword?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_port(self) -> enums.RtkPort:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:PORT \n
		Snippet: value: enums.RtkPort = driver.source.bb.gnss.rtk.get_port() \n
		Sets the port number of the LAN connection. \n
			:return: port_number: 2101| 4022| 50000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:RTK:PORT?')
		return Conversions.str_to_scalar_enum(response, enums.RtkPort)

	def set_port(self, port_number: enums.RtkPort) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:PORT \n
		Snippet: driver.source.bb.gnss.rtk.set_port(port_number = enums.RtkPort._2101) \n
		Sets the port number of the LAN connection. \n
			:param port_number: 2101| 4022| 50000
		"""
		param = Conversions.enum_scalar_to_str(port_number, enums.RtkPort)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RTK:PORT {param}')

	# noinspection PyTypeChecker
	def get_protocol(self) -> enums.RtkProtocol:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:PROTocol \n
		Snippet: value: enums.RtkProtocol = driver.source.bb.gnss.rtk.get_protocol() \n
		Queries the protocol for transmitting RTK data. \n
			:return: protocol: RTCM NTRIP/RTCM 3.3 protocol
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:RTK:PROTocol?')
		return Conversions.str_to_scalar_enum(response, enums.RtkProtocol)

	def set_protocol(self, protocol: enums.RtkProtocol) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:PROTocol \n
		Snippet: driver.source.bb.gnss.rtk.set_protocol(protocol = enums.RtkProtocol.RTCM) \n
		Queries the protocol for transmitting RTK data. \n
			:param protocol: RTCM NTRIP/RTCM 3.3 protocol
		"""
		param = Conversions.enum_scalar_to_str(protocol, enums.RtkProtocol)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RTK:PROTocol {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:STATe \n
		Snippet: value: bool = driver.source.bb.gnss.rtk.get_state() \n
		Activates real-time kinematics simulation. \n
			:return: rtk_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:RTK:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, rtk_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:STATe \n
		Snippet: driver.source.bb.gnss.rtk.set_state(rtk_state = False) \n
		Activates real-time kinematics simulation. \n
			:param rtk_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(rtk_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RTK:STATe {param}')

	def get_user(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:USER \n
		Snippet: value: str = driver.source.bb.gnss.rtk.get_user() \n
		Queries the user ID, that is the RTCM user name. \n
			:return: user_id: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:RTK:USER?')
		return trim_str_response(response)

	def clone(self) -> 'RtkCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RtkCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
