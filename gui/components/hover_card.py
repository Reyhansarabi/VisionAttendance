from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect
)

from PySide6.QtCore import (
    QPropertyAnimation,
    QEasingCurve,
    QPoint
)

from PySide6.QtGui import QColor



class HoverCard(QFrame):

    def __init__(self, parent=None):

        super().__init__(parent)


        self.default_pos = None


        self.shadow = QGraphicsDropShadowEffect()

        self.shadow.setBlurRadius(
            18
        )

        self.shadow.setOffset(
            0,
            5
        )

        self.shadow.setColor(
            QColor(
                40,
                90,
                160,
                30
            )
        )


        self.setGraphicsEffect(
            self.shadow
        )


        self.animation = QPropertyAnimation(
            self,
            b"pos"
        )


        self.animation.setDuration(
            180
        )


        self.animation.setEasingCurve(
            QEasingCurve.OutCubic
        )



    def enterEvent(self, event):

        if self.default_pos is None:
            self.default_pos = self.pos()


        self.shadow.setBlurRadius(
            32
        )

        self.shadow.setOffset(
            0,
            10
        )

        self.shadow.setColor(
            QColor(
                30,
                100,
                220,
                60
            )
        )


        self.animation.stop()


        self.animation.setStartValue(
            self.pos()
        )


        self.animation.setEndValue(
            self.default_pos + QPoint(0, -3)
        )


        self.animation.start()


        super().enterEvent(event)



    def leaveEvent(self, event):


        self.shadow.setBlurRadius(
            18
        )

        self.shadow.setOffset(
            0,
            5
        )


        self.shadow.setColor(
            QColor(
                40,
                90,
                160,
                30
            )
        )


        self.animation.stop()


        self.animation.setStartValue(
            self.pos()
        )


        self.animation.setEndValue(
            self.default_pos
        )


        self.animation.start()


        super().leaveEvent(event)