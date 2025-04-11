# nsd_utils/fsm/extended_wizard.py

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import __version__ as AIOGRAM_VERSION
if AIOGRAM_VERSION != "3.19":
    raise RuntimeError("Requires aiogram==3.19")

class ExtendedWizardSceneBase(StatesGroup):
    async def on_start(self, event, state):
        pass
    async def on_finish(self, event, state):
        pass
    async def on_cancel(self, event, state):
        pass
    async def on_step(self, event, state):
        pass
    async def validate_current_step(self, event, state):
        return True

async def wizard_start(wizard_cls, event, state: FSMContext):
    steps = []
    for k in wizard_cls.__dict__:
        if isinstance(getattr(wizard_cls, k), State):
            steps.append(k)
    if steps:
        st = getattr(wizard_cls, steps[0])
        await state.set_state(st)
        obj = wizard_cls()
        await obj.on_start(event, state)
        await obj.on_step(event, state)

async def wizard_next(wizard_cls, event, state: FSMContext):
    obj = wizard_cls()
    cur = await state.get_state()
    names = []
    for k in wizard_cls.__dict__:
        if isinstance(getattr(wizard_cls, k), State):
            names.append(k)
    order = [getattr(wizard_cls, x) for x in names]
    idx = None
    for i, s in enumerate(order):
        if s.state == cur:
            idx = i
            break
    if idx is not None:
        valid = await obj.validate_current_step(event, state)
        if not valid:
            await obj.on_step(event, state)
            return
        if idx+1 >= len(order):
            await obj.on_finish(event, state)
            await state.clear()
        else:
            nxt = order[idx+1]
            await state.set_state(nxt)
            await obj.on_step(event, state)

async def wizard_cancel(wizard_cls, event, state: FSMContext):
    obj = wizard_cls()
    await obj.on_cancel(event, state)
    await state.clear()
