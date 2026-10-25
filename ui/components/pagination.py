"""
Pagination Controls Component for Large Datasets.
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability
"""

import math
import customtkinter as ctk
from typing import Callable, Optional


class PaginationControl(ctk.CTkFrame):
    """Reusable pagination toolbar with first, prev, next, last controls."""

    def __init__(
        self,
        master,
        total_items: int = 0,
        page_size: int = 10,
        on_page_changed: Optional[Callable[[int], None]] = None,
        **kwargs
    ):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.total_items = max(0, total_items)
        self.page_size = max(1, page_size)
        self.current_page = 1
        self.on_page_changed = on_page_changed

        self.btn_first = ctk.CTkButton(self, text="<<", width=36, height=28, command=self._go_first)
        self.btn_first.pack(side="left", padx=2)

        self.btn_prev = ctk.CTkButton(self, text="< Prev", width=60, height=28, command=self._go_prev)
        self.btn_prev.pack(side="left", padx=2)

        self.lbl_info = ctk.CTkLabel(self, text="Page 1 of 1 (0 items)", font=("Segoe UI", 10))
        self.lbl_info.pack(side="left", padx=10)

        self.btn_next = ctk.CTkButton(self, text="Next >", width=60, height=28, command=self._go_next)
        self.btn_next.pack(side="left", padx=2)

        self.btn_last = ctk.CTkButton(self, text=">>", width=36, height=28, command=self._go_last)
        self.btn_last.pack(side="left", padx=2)

        self._update_state()

    @property
    def total_pages(self) -> int:
        if self.total_items == 0:
            return 1
        return max(1, math.ceil(self.total_items / self.page_size))

    def update_counts(self, total_items: int, page_size: Optional[int] = None) -> None:
        """Updates total item count and adjusts current page if out of bounds."""
        self.total_items = max(0, total_items)
        if page_size:
            self.page_size = max(1, page_size)
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages
        if self.current_page < 1:
            self.current_page = 1
        self._update_state()

    def _update_state(self) -> None:
        """Updates label text and enables/disables navigation buttons."""
        tp = self.total_pages
        self.lbl_info.configure(text=f"Page {self.current_page} of {tp} ({self.total_items} records)")

        self.btn_first.configure(state="normal" if self.current_page > 1 else "disabled")
        self.btn_prev.configure(state="normal" if self.current_page > 1 else "disabled")
        self.btn_next.configure(state="normal" if self.current_page < tp else "disabled")
        self.btn_last.configure(state="normal" if self.current_page < tp else "disabled")

    def _trigger_change(self) -> None:
        self._update_state()
        if self.on_page_changed:
            self.on_page_changed(self.current_page)

    def _go_first(self) -> None:
        if self.current_page != 1:
            self.current_page = 1
            self._trigger_change()

    def _go_prev(self) -> None:
        if self.current_page > 1:
            self.current_page -= 1
            self._trigger_change()

    def _go_next(self) -> None:
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._trigger_change()

    def _go_last(self) -> None:
        if self.current_page != self.total_pages:
            self.current_page = self.total_pages
            self._trigger_change()
