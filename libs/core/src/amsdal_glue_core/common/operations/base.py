from dataclasses import dataclass


@dataclass
class Operation:
    lock_id: str | None = None
    root_transaction_id: str | None = None
    transaction_id: str | None = None
