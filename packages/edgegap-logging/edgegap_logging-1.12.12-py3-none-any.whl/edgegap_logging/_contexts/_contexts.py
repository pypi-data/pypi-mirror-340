from __future__ import annotations

from abc import ABC

from pydantic import BaseModel, ConfigDict


class Context(ABC):
    def get_context(self) -> dict:
        pass


class DictContext(dict, Context):
    def get_context(self) -> dict:
        return self


class TransactionContext(Context, BaseModel):
    model_config = ConfigDict(frozen=True)

    transaction_id: str

    def __init__(self, transaction_id: str):
        super(TransactionContext, self).__init__(transaction_id=transaction_id)

    def get_context(self):
        return {
            'transaction_id': self.transaction_id,
        }

    @staticmethod
    def contains_transaction_context(context: Context) -> bool:
        return 'transaction_id' in context.get_context()

    @staticmethod
    def try_parse_transaction_context(context: Context) -> TransactionContext | None:
        ctx = context.get_context()

        if 'transaction_id' not in ctx:
            return None

        return TransactionContext(transaction_id=ctx['transaction_id'])
