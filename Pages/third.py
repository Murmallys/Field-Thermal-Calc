from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class ThirdPage(QWidget):
    """Третий этап — Результат.
    Содержит левую панель с вкладками, кнопку «Назад» на первой вкладке
    и кнопку «Отчёт» на последней вкладке (без функционала)."""

    # Сигнал для MainWindow: запрос перехода на предыдущий этап
    prev_stage_requested = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #F5F7FA;")
        self.setMinimumSize(1100, 644)

        # Шрифты
        self.font_side = QFont("Inter", 12, QFont.Weight.Normal)
        self.font_btn = QFont("Inter", 14, QFont.Weight.Medium)

        # Состояние
        self.current_side_tab = 0
        self.side_tabs = [
            "3-Вкладка 1", "3-Вкладка 2", "3-Вкладка 3",
            "3-Вкладка 4", "3-Вкладка 5"
        ]

        self._build_ui()

    # Сборка интерфейса
    def _build_ui(self):
        #Левая синяя панель
        self.side_panel = QFrame(self)
        self.side_panel.setStyleSheet(
            "background-color: #1B3A5C; border: none;"
        )
        self.side_panel.setGeometry(0, 0, 240, 644)

        #Заголовок
        side_title = QLabel("Заголовок 3", self.side_panel)
        side_title.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        side_title.setStyleSheet("color: #FFFFFF; border: none;")
        side_title.setGeometry(20, 20, 200, 30)

        #Пункты левой панели
        self.side_buttons = []
        y = 80
        for i, tab_name in enumerate(self.side_tabs):
            btn = QPushButton(f"•  {tab_name}", self.side_panel)
            btn.setFont(self.font_side)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(
                "background-color: transparent; color: #C8D6E5; "
                "border: none; text-align: left; padding-left: 20px;"
            )
            btn.setGeometry(0, y, 240, 44)
            btn.clicked.connect(lambda checked, idx=i: self._on_side_tab(idx))
            self.side_buttons.append(btn)
            y += 48

        self._highlight_side_tab(0)

        #Основная область контента
        self.content_area = QFrame(self)
        self.content_area.setStyleSheet(
            "background-color: #F5F7FA; border: none;"
        )
        self.content_area.setGeometry(240, 0, 860, 590)

        self.content_label = QLabel(
            "Страница: Вкладка 1", self.content_area
        )
        self.content_label.setFont(QFont("Inter", 20, QFont.Weight.Light))
        self.content_label.setStyleSheet(
            "color: #B0B8C4; border: none;"
        )
        self.content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_label.setGeometry(0, 200, 860, 60)

        #Нижняя панель с кнопками
        self.bottom_bar = QFrame(self)
        self.bottom_bar.setStyleSheet(
            "background-color: #F5F7FA; border: none;"
        )
        self.bottom_bar.setGeometry(240, 590, 860, 54)

        #Кнопка «Назад»
        self.btn_prev = QPushButton("← Назад", self.bottom_bar)
        self.btn_prev.setFont(self.font_btn)
        self.btn_prev.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_prev.setStyleSheet(
            "background-color: #1B3A5C; color: #FFFFFF; "
            "border-radius: 8px; border: none; padding: 8px 32px;"
        )
        self.btn_prev.setGeometry(10, 6, 140, 40)
        self.btn_prev.clicked.connect(self._on_prev)
        self.btn_prev.installEventFilter(self)

        # Кнопка «Отчёт»
        self.btn_report = QPushButton("Отчёт", self.bottom_bar)
        self.btn_report.setFont(self.font_btn)
        self.btn_report.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_report.setStyleSheet(
            "background-color: #1B3A5C; color: #FFFFFF; "
            "border-radius: 8px; border: none; padding: 8px 32px;"
        )
        self.btn_report.setGeometry(700, 6, 140, 40)
        # TODO: добавить функционал генерации отчёта
        self.btn_report.installEventFilter(self)

        # По умолчанию обе кнопки скрыты
        self.btn_prev.setVisible(False)
        self.btn_report.setVisible(False)

        # Показываем кнопку «Назад» на первой вкладке
        self._update_buttons_visibility(0)

    # Подсветка активной вкладки
    def _highlight_side_tab(self, index: int):
        for i, btn in enumerate(self.side_buttons):
            if i == index:
                btn.setStyleSheet(
                    "background-color: #2A5A8C; color: #FFFFFF; "
                    "border: none; text-align: left; padding-left: 20px;"
                )
            else:
                btn.setStyleSheet(
                    "background-color: transparent; color: #C8D6E5; "
                    "border: none; text-align: left; padding-left: 20px;"
                )

    # Обновление видимости кнопок
    def _update_buttons_visibility(self, index: int):
        """Показываем «Назад» на первой вкладке, «Отчёт» на последней."""
        if index == 0:
            #Первая вкладка — только «Назад»
            self.btn_prev.setVisible(True)
            self.btn_report.setVisible(False)
        elif index == len(self.side_tabs) - 1:
            #Последняя вкладка
            self.btn_prev.setVisible(False)
            self.btn_report.setVisible(True)
        else:
            #Промежуточные вкладки
            self.btn_prev.setVisible(False)
            self.btn_report.setVisible(False)

    #Обработчики
    def _on_side_tab(self, index: int):
        self.current_side_tab = index
        self._highlight_side_tab(index)
        self.content_label.setText(f"Страница: {self.side_tabs[index]}")
        self._update_buttons_visibility(index)

    def _on_prev(self):
        """Переход на предыдущий этап (этап 2)."""
        self.prev_stage_requested.emit(1)

    #Hover-эффект кнопок
    def eventFilter(self, obj, event):
        from PyQt6.QtCore import QEvent
        if obj in (self.btn_prev, self.btn_report):
            if event.type() == QEvent.Type.Enter:
                obj.setStyleSheet(
                    "background-color: #2A5A8C; color: #FFFFFF; "
                    "border-radius: 8px; border: none; padding: 8px 32px;"
                )
            elif event.type() == QEvent.Type.Leave:
                obj.setStyleSheet(
                    "background-color: #1B3A5C; color: #FFFFFF; "
                    "border-radius: 8px; border: none; padding: 8px 32px;"
                )
        return super().eventFilter(obj, event)

    #Сброс вкладки
    def reset_to_first_tab(self):
        """Сброс на первую вкладку."""
        self._on_side_tab(0)