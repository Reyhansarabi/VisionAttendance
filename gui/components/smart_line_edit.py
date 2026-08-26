import re

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit


# =========================================================
# Character Detection
# =========================================================

_RTL_RE = re.compile(
    r"[\u0590-\u08FF\uFB1D-\uFDFD\uFE70-\uFEFC]"
)

_LTR_RE = re.compile(
    r"[A-Za-z]"
)

_DIGIT_RE = re.compile(
    r"[0-9\u06F0-\u06F9]"
)


# =========================================================
# Detect Text Direction
# =========================================================

def _strong_direction(text):
    """
    تشخیص جهت متن بر اساس اولین کاراکتر معنادار.

    فارسی / عربی  -> rtl
    انگلیسی       -> ltr
    عدد            -> ltr
    """

    for character in text or "":

        # فارسی / عربی
        if _RTL_RE.match(character):
            return "rtl"

        # انگلیسی
        if _LTR_RE.match(character):
            return "ltr"

        # اعداد انگلیسی / فارسی
        if _DIGIT_RE.match(character):
            return "ltr"

    return None


# =========================================================
# Text Direction Alignment
# =========================================================

def text_direction_alignment(
    text,
    empty_alignment=None
):
    """
    استاندارد ترازبندی متن داخل فیلد:

    فارسی / عربی -> راست
    انگلیسی      -> چپ
    عدد           -> چپ
    خالی          -> empty_alignment
    """

    direction = _strong_direction(
        text
    )

    # =====================================================
    # Persian / Arabic
    # =====================================================

    if direction == "rtl":

        return (
            Qt.AlignmentFlag.AlignRight
            |
            Qt.AlignmentFlag.AlignVCenter
        )

    # =====================================================
    # English / Numbers
    # =====================================================

    if direction == "ltr":

        return (
            Qt.AlignmentFlag.AlignLeft
            |
            Qt.AlignmentFlag.AlignVCenter
        )

    # =====================================================
    # Empty
    # =====================================================

    if empty_alignment is None:

        empty_alignment = (
            Qt.AlignmentFlag.AlignRight
        )

    return (
        empty_alignment
        |
        Qt.AlignmentFlag.AlignVCenter
    )


# =========================================================
# Smart Line Edit
# =========================================================

class SmartLineEdit(QLineEdit):

    """
    فیلد متنی هوشمند.

    قوانین:

        فارسی:
            راست‌چین

        انگلیسی:
            چپ‌چین

        عدد:
            چپ‌چین

        خالی:
            بر اساس Placeholder
    """

    def __init__(
        self,
        parent=None,
        empty_alignment=None
    ):

        super().__init__(
            parent
        )

        # =================================================
        # Default Empty Alignment
        # =================================================

        self._empty_alignment = (
            empty_alignment
            if empty_alignment is not None
            else Qt.AlignmentFlag.AlignRight
        )

        # =================================================
        # Store Stylesheet
        # =================================================

        self._base_stylesheet = ""

        # =================================================
        # IMPORTANT
        # =================================================
        # به layoutDirection دست نمی‌زنیم.
        #
        # فقط Alignment متن را کنترل می‌کنیم.
        #
        # این باعث می‌شود RTL بودن کل صفحه یا والد،
        # ساختار فیلد را به‌هم نزند.
        # =================================================

        # =================================================
        # Text Changed
        # =================================================

        self.textChanged.connect(
            self._update_direction
        )

        # =================================================
        # Initial Alignment
        # =================================================

        self._update_direction(
            self.text()
        )

    # =====================================================
    # Placeholder
    # =====================================================

    def setPlaceholderText(
        self,
        text
    ):

        super().setPlaceholderText(
            text
        )

        # اگر فیلد خالی است،
        # Alignment را براساس Placeholder تنظیم کن.
        if not self.text():

            self._update_direction(
                ""
            )

    # =====================================================
    # Empty Alignment
    # =====================================================

    def set_empty_alignment(
        self,
        alignment
    ):

        self._empty_alignment = (
            alignment
        )

        self._update_direction(
            self.text()
        )

    # =====================================================
    # Placeholder Alignment
    # =====================================================

    def _placeholder_alignment(self):

        direction = _strong_direction(
            self.placeholderText()
        )

        # -------------------------------------------------
        # Placeholder فارسی
        # -------------------------------------------------

        if direction == "rtl":

            return (
                Qt.AlignmentFlag.AlignRight
            )

        # -------------------------------------------------
        # Placeholder انگلیسی / عدد
        # -------------------------------------------------

        if direction == "ltr":

            return (
                Qt.AlignmentFlag.AlignLeft
            )

        # -------------------------------------------------
        # Placeholder نامشخص
        # -------------------------------------------------

        return self._empty_alignment

    # =====================================================
    # Stylesheet
    # =====================================================

    def setStyleSheet(
        self,
        style_sheet
    ):

        self._base_stylesheet = (
            style_sheet or ""
        )

        super().setStyleSheet(
            self._base_stylesheet
        )

        # بعد از اعمال stylesheet،
        # Alignment را دوباره اعمال می‌کنیم.
        self._apply_alignment(
            self.text()
        )

    # =====================================================
    # Apply Alignment
    # =====================================================

    def _apply_alignment(
        self,
        text
    ):

        # =================================================
        # Text Exists
        # =================================================

        if text:

            alignment = (
                text_direction_alignment(
                    text,
                    self._empty_alignment
                )
            )

            self.setAlignment(
                alignment
            )

            return

        # =================================================
        # Empty Field
        # =================================================

        self.setAlignment(
            self._placeholder_alignment()
            |
            Qt.AlignmentFlag.AlignVCenter
        )

    # =====================================================
    # Text Changed
    # =====================================================

    def _update_direction(
        self,
        text
    ):

        self._apply_alignment(
            text
        )