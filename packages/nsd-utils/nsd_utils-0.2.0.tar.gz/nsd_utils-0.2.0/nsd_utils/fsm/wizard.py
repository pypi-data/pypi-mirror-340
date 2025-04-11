# fsm/wizard.py

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from typing import Any

class WizardSceneBase(StatesGroup):
    """
    Базовый класс для многошаговых сценариев.
    Пример использования:
      class DepositWizard(WizardSceneBase):
          step_currency = State()
          step_amount = State()
          step_confirm = State()
    """

    async def on_enter_step(self, step: State, event: Message | CallbackQuery, data: dict) -> Any:
        """
        Можете переопределять в потомках.
        """
        pass

    async def on_exit_step(self, step: State, event: Message | CallbackQuery, data: dict) -> Any:
        """
        Вызывается при уходе со шага.
        """
        pass

    # Можно расширять как угодно:
    # методы, которые вызываются при on_transition, on_finish и т.п.
