"""
The base class for all transaction types. Represents fields common to all transaction
types.

See https://xrpl.org/transaction-types.html.
See https://xrpl.org/transaction-common-fields.html.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from xrpl.models.base_model import REQUIRED, BaseModel


class TransactionType(str, Enum):
    """Enum containing the different Transaction types."""

    ACCOUNT_DELETE = "AccountDelete"
    ACCOUNT_SET = "AccountSet"
    CHECK_CANCEL = "CheckCancel"
    CHECK_CASH = "CheckCash"
    CHECK_CREATE = "CheckCreate"
    DEPOSIT_PREAUTH = "DepositPreauth"
    ESCROW_CANCEL = "EscrowCancel"
    ESCROW_CREATE = "EscrowCreate"
    ESCROW_FINISH = "EscrowFinish"
    OFFER_CANCEL = "OfferCancel"
    OFFER_CREATE = "OfferCreate"
    PAYMENT = "Payment"
    PAYMENT_CHANNEL_CLAIM = "PaymentChannelClaim"
    PAYMENT_CHANNEL_CREATE = "PaymentChannelCreate"
    PAYMENT_CHANNEL_FUND = "PaymentChannelFund"
    SET_REGULAR_KEY = "SetRegularKey"
    SIGNER_LIST_SET = "SignerListSet"
    TRUST_SET = "TrustSet"


@dataclass(frozen=True)
class Memo(BaseModel):
    """
    The Memos field includes arbitrary messaging data with
    the transaction. It is presented as an array of objects.
    Each object has only one field, Memo, which in turn contains
    another object with one or more of the following fields.
    """

    memo_data: Optional[str] = None
    memo_format: Optional[str] = None
    memo_type: Optional[str] = None

    def _get_errors(self: Memo) -> Dict[str, str]:
        errors = super()._get_errors()
        present_memo_fields = [
            field
            for field in [
                self.memo_data,
                self.memo_format,
                self.memo_type,
            ]
            if field is not None
        ]
        if len(present_memo_fields) < 1:
            errors["Memo"] = "Memo must contain at least one field"
        return errors


@dataclass(frozen=True)
class Signer(BaseModel):
    """
    The Signers field contains a multi-signature, which has
    signatures from up to 8 key pairs, that together should
    authorize the transaction. The Signers list is an array
    of objects, each with one field, Signer. The Signer field
    has the following nested fields.
    """

    account: str = REQUIRED
    txn_signature: str = REQUIRED
    signing_pub_key: str = REQUIRED


@dataclass(frozen=True)
class Transaction(BaseModel):
    """
    The base class for all transaction types. Represents fields common to all
    transaction types.

    See https://xrpl.org/transaction-types.html.
    See https://xrpl.org/transaction-common-fields.html.
    """

    account: str = REQUIRED
    transaction_type: TransactionType = REQUIRED
    fee: Optional[str] = None  # auto-fillable
    sequence: Optional[int] = None  # auto-fillable
    account_txn_id: Optional[str] = None
    flags: int = 0
    last_ledger_sequence: Optional[int] = None
    memos: Optional[List[Memo]] = None
    signers: Optional[List[Signer]] = None
    source_tag: Optional[int] = None
    signing_pub_key: Optional[str] = None
    txn_signature: Optional[str] = None

    def to_dict(self: Transaction) -> Dict[str, Any]:
        """
        Returns the dictionary representation of a Transaction.

        Returns:
            The dictionary representation of a Transaction.
        """
        return {**super().to_dict(), "transaction_type": self.transaction_type.value}

    def has_flag(self: Transaction, flag: int) -> bool:
        """
        Returns whether the transaction has the given flag value set.

        Args:
            flag: The given flag value for which the function will determine whether it
                is set.

        Returns:
            Whether the transaction has the given flag value set.
        """
        return self.flags & flag != 0
