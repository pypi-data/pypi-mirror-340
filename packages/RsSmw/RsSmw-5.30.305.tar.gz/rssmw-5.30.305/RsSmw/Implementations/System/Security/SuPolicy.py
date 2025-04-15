from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SuPolicyCls:
	"""SuPolicy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("suPolicy", core, parent)

	def set(self, sec_pass_word: str, update_policy: enums.UpdPolicyMode) -> None:
		"""SCPI: SYSTem:SECurity:SUPolicy \n
		Snippet: driver.system.security.suPolicy.set(sec_pass_word = 'abc', update_policy = enums.UpdPolicyMode.CONFirm) \n
		No command help available \n
			:param sec_pass_word: No help available
			:param update_policy: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sec_pass_word', sec_pass_word, DataType.String), ArgSingle('update_policy', update_policy, DataType.Enum, enums.UpdPolicyMode))
		self._core.io.write(f'SYSTem:SECurity:SUPolicy {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self) -> enums.UpdPolicyMode:
		"""SCPI: SYSTem:SECurity:SUPolicy \n
		Snippet: value: enums.UpdPolicyMode = driver.system.security.suPolicy.get() \n
		No command help available \n
			:return: update_policy: No help available"""
		response = self._core.io.query_str(f'SYSTem:SECurity:SUPolicy?')
		return Conversions.str_to_scalar_enum(response, enums.UpdPolicyMode)
