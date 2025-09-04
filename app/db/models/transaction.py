# class for Transaction.

from __future__ import annotations

from decimal import Decimal
from datetime import datetime

from sqlalchemy import String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

class Transaction(Base):
    """ This is the model for Transactions.
    Money movements tied to a user and an optional category."""
    
    __tablename__ = "transactions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    merchant: Mapped[str] = mapped_column(String(200), default="", index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    posted_at: Mapped[datetime] = mapped_column(DateTime(timeone=True), index=True, nullable=False)
    note: Mapped[str] = mapped_column(String(500), default="", nullable=False)
    
    # relationships
    owner: Mapped["User"] = relationship(back_populates="transactions")
    category: Mapped["Category | None"] = relationship(back_populates="transactions")