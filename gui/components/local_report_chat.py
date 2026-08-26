"""Local, offline report assistant widget.

This component does not use OpenAI or any external API. It interprets common
Persian attendance questions and calculates answers directly from the current
report data provided by the page.
"""

import re
from collections import Counter, defaultdict
from datetime import datetime

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from theme.fonts import Fonts


class LocalReportAssistant:
    """Small rule-based natural-language analyzer for attendance reports."""

    STATUS_ALIASES = {
        "حاضر": {"حاضر", "حضور"},
        "غایب": {"غایب", "غیبت", "نبوده", "عدم حضور"},
        "تاخیر": {"تاخیر", "تأخیر", "دیر", "دیرکرد"},
    }

    def __init__(self, records, start_date=None, end_date=None):
        self.records = list(records or [])
        self.start_date = start_date
        self.end_date = end_date

    def set_context(self, records, start_date=None, end_date=None):
        """Replace the report context immediately when the page filter changes."""
        self.records = list(records or [])
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def _field(record, key, default=None):
        """Read a field from dict-like records and sqlite3.Row safely."""
        try:
            if hasattr(record, "keys") and key in record.keys():
                return record[key]
        except Exception:
            pass

        try:
            return record[key]
        except (KeyError, IndexError, TypeError):
            pass

        try:
            return getattr(record, key)
        except AttributeError:
            return default

    @classmethod
    def _name(cls, record):
        first_name = cls._field(record, "first_name", "") or ""
        last_name = cls._field(record, "last_name", "") or ""
        name = f"{first_name} {last_name}".strip()
        return name or "نامشخص"

    @classmethod
    def _status(cls, record):
        return str(cls._field(record, "status", "") or "").strip().lower()

    @staticmethod
    def _date_key(value):
        if not value:
            return None
        value = str(value).strip()
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                pass
        return None

    @staticmethod
    def _time_minutes(value):
        if not value:
            return None
        text = str(value).strip().replace("٫", ":")
        match = re.search(r"(\d{1,2})[:.](\d{1,2})", text)
        if not match:
            return None
        hours, minutes = int(match.group(1)), int(match.group(2))
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            return hours * 60 + minutes
        return None

    def _count_by_name(self, predicate=None):
        result = Counter()
        for record in self.records:
            if predicate is None or predicate(record):
                result[self._name(record)] += 1
        return result

    def _presence_counts(self):
        counts = defaultdict(lambda: Counter())
        for record in self.records:
            name = self._name(record)
            status = self._status(record)
            if "غیبت" in status or "غایب" in status:
                counts[name]["غیبت"] += 1
            elif "تاخیر" in status or "تأخیر" in status:
                counts[name]["تأخیر"] += 1
            elif "حاضر" in status or "حضور" in status:
                counts[name]["حضور"] += 1
            else:
                counts[name]["سایر"] += 1
        return counts

    def _scope_label(self):
        if self.start_date and self.end_date:
            return f"بازه انتخاب‌شده: {self.start_date} تا {self.end_date}"
        return "بازه انتخاب‌شده فعلی"

    def _scope_message(self, message):
        return f"{self._scope_label()}\n{message}"

    def detect_anomalies(self, limit=6):
        """Detect explainable attendance anomalies in the current filtered scope."""
        records = self.records
        if not records:
            return []

        findings = []
        seen = set()
        per_person = defaultdict(list)

        # Build per-person check-in history for personal baselines.
        for record in records:
            name = self._name(record)
            minutes = self._time_minutes(self._field(record, "check_in"))
            if minutes is not None:
                per_person[name].append(minutes)

        medians = {}
        for name, values in per_person.items():
            values = sorted(values)
            mid = len(values) // 2
            medians[name] = values[mid] if len(values) % 2 else (values[mid - 1] + values[mid]) / 2

        def add(level, name, date, reason):
            key = (level, name, str(date), reason)
            if key in seen:
                return
            seen.add(key)
            findings.append({"level": level, "name": name, "date": str(date or "نامشخص"), "reason": reason})

        # Structural/data-quality anomalies.
        duplicate_keys = Counter()
        for record in records:
            key = (self._name(record), str(self._field(record, "date", "")))
            duplicate_keys[key] += 1
        for (name, date), count in duplicate_keys.items():
            if count > 1:
                add("متوسط", name, date, f"برای یک روز {count} رکورد حضور ثبت شده است")

        for record in records:
            name = self._name(record)
            date = self._field(record, "date", "نامشخص")
            status = self._status(record)
            check_in = self._field(record, "check_in")
            check_out = self._field(record, "check_out")

            if status in ("حاضر", "حضور") and not check_in:
                add("متوسط", name, date, "وضعیت حضور ثبت شده ولی ساعت ورود خالی است")
            if status in ("حاضر", "حضور") and not check_out:
                add("متوسط", name, date, "ساعت خروج برای رکورد حاضر ثبت نشده است")

            minutes = self._time_minutes(check_in)
            baseline = medians.get(name)
            if minutes is not None and baseline is not None and minutes - baseline >= 60:
                delay = int(minutes - baseline)
                hours, mins = divmod(delay, 60)
                if hours and mins:
                    delay_text = f"{hours} ساعت و {mins} دقیقه"
                elif hours:
                    delay_text = f"{hours} ساعت"
                else:
                    delay_text = f"{mins} دقیقه"
                add("بالا", name, date, f"ورود حدود {delay_text} دیرتر از الگوی معمول این فرد بوده است")

        # High-frequency absence/delay patterns.
        counts = self._presence_counts()
        for name, values in counts.items():
            if values["غیبت"] >= 3:
                add("بالا", name, "بازه فعلی", f"{values['غیبت']} مورد غیبت در بازه ثبت شده است")
            if values["تأخیر"] >= 3:
                add("بالا", name, "بازه فعلی", f"{values['تأخیر']} مورد تأخیر در بازه ثبت شده است")

        priority = {"بالا": 0, "متوسط": 1, "پایین": 2}
        findings.sort(key=lambda x: (priority.get(x["level"], 9), x["name"], x["date"]))
        return findings[:limit]

    def answer(self, question):
        q = (question or "").strip()
        if not q:
            return "لطفاً سؤال خود را کامل بنویسید."

        records = self.records
        if not records:
            return self._scope_message("در حال حاضر رکوردی در بازه انتخاب‌شده برای تحلیل وجود ندارد.")

        q_lower = q.lower()
        counts = self._presence_counts()

        # Summary / management questions.
        if any(x in q_lower for x in ("خلاصه مدیریتی", "خلاصه", "جمع بندی", "جمع‌بندی")):
            total = len(records)
            absences = sum(v["غیبت"] for v in counts.values())
            delays = sum(v["تأخیر"] for v in counts.values())
            present = sum(v["حضور"] for v in counts.values())
            users = len(counts)
            return (
                f"خلاصه بازه انتخاب‌شده:\n"
                f"• تعداد کارکنان دارای رکورد: {users} نفر\n"
                f"• مجموع رکوردهای حضور: {present}\n"
                f"• مجموع غیبت‌ها: {absences}\n"
                f"• مجموع تأخیرها: {delays}\n"
                f"• مجموع رکوردهای بررسی‌شده: {total}"
            )

        # Explicit total record count.
        if any(x in q_lower for x in ("چند رکورد", "تعداد رکورد", "تعداد گزارش")):
            return f"در بازه انتخاب‌شده {len(records)} رکورد حضور و غیاب برای تحلیل وجود دارد."

        # Absence count / ranking.
        if any(x in q_lower for x in ("غیبت", "غایب")):
            absence = self._count_by_name(
                lambda r: "غیبت" in self._status(r) or "غایب" in self._status(r)
            )
            total = sum(absence.values())
            if "کدام" in q_lower or "بیشترین" in q_lower or "کارکنان" in q_lower or "نام" in q_lower:
                if not absence:
                    return "در بازه انتخاب‌شده هیچ رکورد غیبت ثبت نشده است."
                top = sorted(absence.items(), key=lambda x: (-x[1], x[0]))
                lines = [f"مجموع غیبت‌های ثبت‌شده: {total}"]
                for name, value in top[:10]:
                    lines.append(f"• {name}: {value} غیبت")
                return "\n".join(lines)
            return f"مجموع غیبت‌های ثبت‌شده در بازه انتخاب‌شده {total} مورد است."

        # Delay count / ranking.
        if any(x in q_lower for x in ("تأخیر", "تاخیر", "دیر")):
            delay = self._count_by_name(
                lambda r: "تأخیر" in self._status(r) or "تاخیر" in self._status(r)
            )
            total = sum(delay.values())
            if "کدام" in q_lower or "بیشترین" in q_lower or "کارکنان" in q_lower or "نام" in q_lower:
                if not delay:
                    return "در بازه انتخاب‌شده رکوردی با وضعیت تأخیر ثبت نشده است."
                top = sorted(delay.items(), key=lambda x: (-x[1], x[0]))
                lines = [f"مجموع تأخیرهای ثبت‌شده: {total}"]
                for name, value in top[:10]:
                    lines.append(f"• {name}: {value} تأخیر")
                return "\n".join(lines)
            return f"مجموع تأخیرهای ثبت‌شده در بازه انتخاب‌شده {total} مورد است."

        # Presence / attendance count.
        if any(x in q_lower for x in ("حضور", "حاضر")):
            present = self._count_by_name(
                lambda r: "حاضر" in self._status(r) or "حضور" in self._status(r)
            )
            total = sum(present.values())
            if "کدام" in q_lower or "کارکنان" in q_lower or "رتبه" in q_lower or "مقایسه" in q_lower:
                top = sorted(present.items(), key=lambda x: (-x[1], x[0]))
                if not top:
                    return "رکوردی با وضعیت حضور در بازه انتخاب‌شده پیدا نشد."
                return "تعداد رکوردهای حضور:\n" + "\n".join(
                    f"• {name}: {value}" for name, value in top[:10]
                )
            return f"مجموع رکوردهای حضور در بازه انتخاب‌شده {total} مورد است."

        # Per-employee overview.
        if any(x in q_lower for x in ("هر کارمند", "هر کارکن", "هر نفر", "مقایسه")):
            lines = []
            for name, values in sorted(counts.items()):
                lines.append(
                    f"• {name}: حضور {values['حضور']}، غیبت {values['غیبت']}، تأخیر {values['تأخیر']}"
                )
            return "\n".join(lines) if lines else "اطلاعات کافی برای مقایسه وجود ندارد."

        # Clean attendance / no issues.
        if any(x in q_lower for x in ("بدون غیبت", "بدون تأخیر", "بدون تاخیر", "منظم", "منظم‌ترین", "منظم ترین")):
            clean = []
            for name, values in counts.items():
                if values["غیبت"] == 0 and values["تأخیر"] == 0:
                    clean.append((name, values["حضور"]))
            clean.sort(key=lambda x: (-x[1], x[0]))
            if not clean:
                return "کارمندی که هم‌زمان رکورد غیبت و تأخیر نداشته باشد در بازه انتخاب‌شده پیدا نشد."
            return "کارکنان بدون غیبت و تأخیر:\n" + "\n".join(
                f"• {name}: {present} رکورد حضور" for name, present in clean[:15]
            )

        # Date concentration.
        if any(x in q_lower for x in ("روز", "تاریخ", "بازه")) and any(
            x in q_lower for x in ("بیشترین", "کمترین", "غیبت", "تأخیر", "تاخیر")
        ):
            target_delay = any(x in q_lower for x in ("تأخیر", "تاخیر"))
            by_date = Counter()
            for record in records:
                status = self._status(record)
                if target_delay:
                    if "تأخیر" in status or "تاخیر" in status:
                        by_date[str(self._field(record, "date", "نامشخص") or "نامشخص")] += 1
                else:
                    if "غیبت" in status or "غایب" in status:
                        by_date[str(self._field(record, "date", "نامشخص") or "نامشخص")] += 1
            if not by_date:
                return "برای شاخص درخواستی، داده کافی وجود ندارد."
            item = max(by_date.items(), key=lambda x: (x[1], x[0]))
            label = "تأخیر" if target_delay else "غیبت"
            return f"بیشترین {label} در تاریخ {item[0]} ثبت شده و تعداد آن {item[1]} مورد است."

        # Generic quality-check / anomaly wording.
        if any(x in q_lower for x in ("غیرعادی", "مشکوک", "نیاز به بررسی", "بررسی بیشتر")):
            flagged = []
            for name, values in counts.items():
                if values["غیبت"] >= 3 or values["تأخیر"] >= 3:
                    reasons = []
                    if values["غیبت"] >= 3:
                        reasons.append(f"{values['غیبت']} غیبت")
                    if values["تأخیر"] >= 3:
                        reasons.append(f"{values['تأخیر']} تأخیر")
                    flagged.append((name, " و ".join(reasons)))
            if not flagged:
                return "در بازه انتخاب‌شده مورد پرتکرار و مشخصی که نیازمند بررسی ویژه باشد پیدا نشد."
            return "موارد قابل بررسی:\n" + "\n".join(
                f"• {name}: {reason}" for name, reason in flagged[:10]
            )

        return (
            "سؤال شما را دریافت کردم، اما برای این پرسش پاسخ محلی آماده‌ای ندارم.\n"
            "لطفاً سؤال را درباره تعداد حضور، غیبت، تأخیر، مقایسه کارکنان، "
            "بیشترین/کمترین مقدار، یا خلاصه گزارش به‌صورت کامل بیان کنید."
        )


class AnomalyCenter(QFrame):
    """Compact offline anomaly center for the active report scope."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AnomalyCenter")
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet("""
            QFrame#AnomalyCenter {
                background: #FFFFFF;
                border: 1px solid #D9E3EE;
                border-radius: 12px;
            }
            QLabel#anomalyTitle, QLabel#anomalySummary, QLabel#anomalyItem {
                background: transparent;
                border: none;
            }
            QLabel#anomalyTitle { color: #0F172A; font-weight: 800; font-size: 13px; }
            QLabel#anomalySummary { color: #64748B; font-size: 11px; }
            QLabel#anomalyItem { color: #334155; font-size: 11px; padding: 2px 4px; }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 7, 10, 7)
        layout.setSpacing(3)

        header = QHBoxLayout()
        header.setSpacing(8)
        self.title = QLabel("مرکز هوشمند بررسی اتفاقات غیرعادی")
        self.title.setObjectName("anomalyTitle")
        self.summary = QLabel("در حال بررسی بازه فعلی...")
        self.summary.setObjectName("anomalySummary")
        header.addWidget(self.title)
        header.addStretch()
        header.addWidget(self.summary)
        layout.addLayout(header)

        self.items = [QLabel() for _ in range(3)]
        for item in self.items:
            item.setObjectName("anomalyItem")
            item.setWordWrap(False)
            item.setVisible(False)
            layout.addWidget(item)

    def update_context(self, records, start_date=None, end_date=None):
        assistant = LocalReportAssistant(records, start_date, end_date)
        findings = assistant.detect_anomalies(limit=3)
        scope = f"{start_date} تا {end_date}" if start_date and end_date else "بازه فعلی"
        if not findings:
            self.summary.setText(f"{scope} • مورد مهمی پیدا نشد")
        else:
            self.summary.setText(f"{scope} • {len(assistant.detect_anomalies(limit=100))} مورد قابل بررسی")

        for i, item in enumerate(self.items):
            if i < len(findings):
                f = findings[i]
                icon = "⚠" if f["level"] == "بالا" else "•"
                item.setText(f"{icon} {f['name']} — {f['reason']} ({f['date']})")
                item.setVisible(True)
            else:
                item.clear()
                item.setVisible(False)

class LocalReportChat(QFrame):
    """Compact RTL offline chat box for the current attendance report."""

    send_requested = Signal(str)

    QUESTIONS = [
        "لطفاً تعداد کارکنانی را که در بازه انتخاب‌شده غیبت داشته‌اند، اعلام کن.",
        "لطفاً نام کارکنانی را که بیشترین میزان تأخیر را در این گزارش داشته‌اند، مشخص کن.",
        "لطفاً وضعیت حضور و غیاب کارکنان را در بازه زمانی انتخاب‌شده خلاصه کن.",
        "لطفاً تعداد روزهای حضور، غیبت و تأخیر هر کارمند را بر اساس این گزارش مقایسه کن.",
        "لطفاً کارکنانی را که در بازه انتخاب‌شده بیشترین حضور منظم را داشته‌اند، معرفی کن.",
        "لطفاً کارکنانی را که بیشترین تعداد غیبت را داشته‌اند، از بیشترین به کمترین مرتب کن.",
        "لطفاً تعداد کل رکوردهای حضور و غیاب ثبت‌شده در بازه انتخاب‌شده را اعلام کن.",
        "لطفاً مجموع تأخیرهای ثبت‌شده در بازه انتخاب‌شده را محاسبه و اعلام کن.",
        "لطفاً مجموع غیبت‌های ثبت‌شده در بازه انتخاب‌شده را محاسبه و اعلام کن.",
        "لطفاً کارکنانی را که هیچ غیبت یا تأخیری نداشته‌اند، مشخص کن.",
        "لطفاً روزی را که بیشترین غیبت در آن ثبت شده است، مشخص کن.",
        "لطفاً روزی را که بیشترین تأخیر در آن ثبت شده است، مشخص کن.",
        "لطفاً کارکنان را بر اساس تعداد رکوردهای حضور از بیشترین به کمترین رتبه‌بندی کن.",
        "لطفاً کارکنان را بر اساس تعداد غیبت از بیشترین به کمترین رتبه‌بندی کن.",
        "لطفاً کارکنان را بر اساس تعداد تأخیر از بیشترین به کمترین رتبه‌بندی کن.",
        "لطفاً سه نکته مهم و قابل توجه درباره وضعیت حضور و غیاب این گزارش بیان کن.",
        "لطفاً مواردی را که به دلیل غیبت یا تأخیر زیاد نیاز به بررسی بیشتر دارند، مشخص کن.",
        "لطفاً این گزارش را برای ارائه به مدیر، کوتاه و روشن خلاصه کن.",
    ]

    def __init__(self, context_provider=None, parent=None):
        super().__init__(parent)
        self.context_provider = context_provider
        self._messages = []
        self._busy = False
        self._current_start_date = None
        self._current_end_date = None

        self.setObjectName("LocalReportChat")
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet(
            """
            QFrame#LocalReportChat {
                background: #FFFFFF;
                border: 1px solid #D9E3EE;
                border-radius: 12px;
            }
            QLabel#chatTitle, QLabel#chatHint {
                background: transparent;
                border: none;
            }
            QLabel#chatTitle { color: #0F172A; font-weight: 700; }
            QLabel#chatHint { color: #64748B; }
            QTextEdit#chatHistory, QTextEdit#chatInput {
                background: #F8FAFC;
                color: #1E293B;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 6px;
            }
            QTextEdit#chatHistory { font-size: 12px; }
            QTextEdit#chatInput { font-size: 12px; }
            QPushButton#chatSend {
                background: #5699D7;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 0 15px;
                min-height: 38px;
                font-weight: 700;
                font-size: 12px;
            }
            QPushButton#chatSend:disabled { background: #B7C7D8; }
            QComboBox#questionBox {
                background: #F8FAFC;
                color: #334155;
                border: 1px solid #E2E8F0;
                border-radius: 7px;
                padding: 2px 8px;
                font-size: 11px;
            }
            QComboBox#questionBox::drop-down { width: 24px; border: none; }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(5)

        header = QHBoxLayout()
        header.setSpacing(8)

        title = QLabel("دستیار تحلیل گزارش")
        title.setObjectName("chatTitle")
        title.setFont(Fonts.small())

        hint = QLabel("آفلاین")
        hint.setObjectName("chatHint")
        hint.setFont(Fonts.small())

        self.question_box = QComboBox()
        self.question_box.setObjectName("questionBox")
        self.question_box.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.question_box.addItem("سؤال‌های پیشنهادی")
        self.question_box.addItems(self.QUESTIONS)
        self.question_box.setCurrentIndex(0)
        self.question_box.setFixedHeight(32)
        self.question_box.currentIndexChanged.connect(self._select_suggested_question)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.question_box)
        header.addWidget(hint)
        layout.addLayout(header)

        self.history = QTextEdit()
        self.history.setObjectName("chatHistory")
        self.history.setReadOnly(True)
        self.history.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.history.setMinimumHeight(48)
        self.history.setMaximumHeight(70)
        layout.addWidget(self.history, 1)

        input_row = QHBoxLayout()
        input_row.setSpacing(8)

        self.input = QTextEdit()
        self.input.setObjectName("chatInput")
        self.input.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.input.setPlaceholderText("سؤال کامل خود را درباره گزارش وارد کنید...")
        self.input.setFixedHeight(40)
        self.input.setAcceptRichText(False)
        self.input.installEventFilter(self)

        self.send_button = QPushButton("ارسال")
        self.send_button.setObjectName("chatSend")
        self.send_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_button.clicked.connect(self._submit)

        input_row.addWidget(self.input, 1)
        input_row.addWidget(self.send_button)
        layout.addLayout(input_row)

        self._append_message("دستیار", "سلام! درباره بازه انتخاب‌شده سؤال خودت را کامل بنویس.")

    def update_context(self, records, start_date=None, end_date=None):
        """Refresh the chat context immediately after report filters change."""
        self._current_start_date = start_date
        self._current_end_date = end_date

    def _format_scope(self):
        start = self._current_start_date
        end = self._current_end_date
        if start is None or end is None:
            return "بازه انتخاب‌شده"
        return f"{start} تا {end}"

    def _select_suggested_question(self, index):
        if index <= 0:
            return
        self.input.setPlainText(self.question_box.itemText(index))
        self.input.setFocus()
        self.input.moveCursor(QTextCursor.MoveOperation.End)
        self.question_box.blockSignals(True)
        self.question_box.setCurrentIndex(0)
        self.question_box.blockSignals(False)

    def eventFilter(self, obj, event):
        if obj is self.input and event.type() == event.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                    return super().eventFilter(obj, event)
                self._submit()
                return True
        return super().eventFilter(obj, event)

    def _append_message(self, speaker, text):
        self._messages.append((speaker, text))
        cursor = self.history.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        if self.history.toPlainText():
            cursor.insertText("\n\n")
        cursor.insertText(f"{speaker}:\n{text}")
        self.history.setTextCursor(cursor)
        self.history.ensureCursorVisible()

    def _submit(self):
        if self._busy:
            return
        question = self.input.toPlainText().strip()
        if not question:
            return

        self._busy = True
        self.input.clear()
        self._append_message("شما", question)
        self._append_message("دستیار", "در حال بررسی گزارش...")
        self.send_button.setEnabled(False)
        self.input.setEnabled(False)

        records = []
        start_date = self._current_start_date
        end_date = self._current_end_date
        if callable(self.context_provider):
            try:
                value = self.context_provider()
                if isinstance(value, dict):
                    records = list(value.get("records") or [])
                    start_date = value.get("start_date", start_date)
                    end_date = value.get("end_date", end_date)
                elif isinstance(value, list):
                    records = value
            except Exception:
                records = []

        assistant = LocalReportAssistant(records, start_date, end_date)
        response = assistant.answer(question)
        self._remove_busy_line()
        self._append_message("دستیار", response)
        self.send_requested.emit(question)
        self._busy = False
        self.send_button.setEnabled(True)
        self.input.setEnabled(True)
        self.input.setFocus()

    def _remove_busy_line(self):
        text = self.history.toPlainText()
        marker = "\nدستیار:\nدر حال بررسی گزارش..."
        if text.endswith(marker):
            text = text[:-len(marker)]
        elif text.endswith("دستیار:\nدر حال بررسی گزارش..."):
            text = text[:-len("دستیار:\nدر حال بررسی گزارش...")]
        self.history.setPlainText(text)
        cursor = self.history.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.history.setTextCursor(cursor)

    def reset_analysis(self):
        """Reset the analysis session completely when leaving the report page."""
        self._messages = []
        self._busy = False
        self._current_start_date = None
        self._current_end_date = None

        self.history.clear()
        self.input.clear()
        self.question_box.blockSignals(True)
        self.question_box.setCurrentIndex(0)
        self.question_box.blockSignals(False)

        self.send_button.setEnabled(True)
        self.input.setEnabled(True)
        self._append_message(
            "دستیار",
            "سلام! درباره بازه انتخاب‌شده سؤال خودت را کامل بنویس."
        )

    def shutdown(self):
        self._busy = False
