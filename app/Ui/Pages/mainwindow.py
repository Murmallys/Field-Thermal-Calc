from PyQt6.QtWidgets import (
    QMainWindow, QStackedWidget, QFrame, QPushButton, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from app.Ui.Pages.first import FirstPage
from app.Ui.Pages.second import SecondPage
from app.Ui.Pages.third import ThirdPage


class MainWindow(QMainWindow):
    """Главное окно приложения. Содержит верхнюю панель этапов
    и QStackedWidget для переключения между страницами."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("База знаний")
        self.setFixedSize(1100, 700)
        self.setStyleSheet("background-color: #F5F7FA;")

        # Шрифты
        self.font_tab = QFont("Inter", 12, QFont.Weight.Normal)
        self.font_tab_active = QFont("Inter", 12, QFont.Weight.Bold)

        # Текущий этап (0, 1, 2)
        self.current_stage = 0

        self._build_top_bar()
        self._build_stack()

    #  Верхняя панель этапов
    def _build_top_bar(self):
        self.top_bar = QFrame(self)
        self.top_bar.setStyleSheet(
            "background-color: #E8ECF1; border: none;"
        )
        self.top_bar.setGeometry(0, 0, 1100, 56)

        self.stage_buttons = []
        stage_names = ["Создание проекта", "Расчёт и подбор", "Результат"]
        x_start = 20
        for i, name in enumerate(stage_names):
            btn = QPushButton(name, self.top_bar)
            btn.setFont(self.font_tab if i != 0 else self.font_tab_active)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            
            if i == 0:
                btn.setStyleSheet(
                    "background-color: #FFFFFF; border-radius: 8px; "
                    "border: none; padding: 10px 24px; color: #1A1A1A;"
                )
            else:
                btn.setStyleSheet(
                    "background-color: transparent; border-radius: 8px; "
                    "border: none; padding: 10px 24px; color: #6B7B8D;"
                )
            
            btn.setGeometry(x_start, 8, 220, 40)
            btn.clicked.connect(lambda checked, idx=i: self._on_stage_clicked(idx))
            btn.installEventFilter(self)
            
            self.stage_buttons.append(btn)
            x_start += 240

    #  Стек страниц
    def _build_stack(self):
        self.stack = QStackedWidget(self)
        self.stack.setGeometry(0, 56, 1100, 644)

        # Этап 1
        self.first_page = FirstPage()
        self.first_page.next_stage_requested.connect(self._go_to_stage)
        self.stack.addWidget(self.first_page)

        # Этап 2
        self.second_page = SecondPage()
        self.second_page.next_stage_requested.connect(self._go_to_stage)
        self.second_page.prev_stage_requested.connect(self._go_to_stage)
        self.stack.addWidget(self.second_page)

        # Этап 3
        self.third_page = ThirdPage()
        self.third_page.prev_stage_requested.connect(self._go_to_stage)
        self.stack.addWidget(self.third_page)

        self.stack.setCurrentIndex(0)

    #  Обработчик клика по этапу
    def _on_stage_clicked(self, stage_index: int):
        """Переход на выбранный этап при клике."""
        self._go_to_stage(stage_index)

    #  Переключение этапа
    def _go_to_stage(self, stage_index: int):
        """Переход на указанный этап (0, 1, 2)."""
        if stage_index < 0 or stage_index > 2:
            return

        self.current_stage = stage_index
        self.stack.setCurrentIndex(stage_index)
        self._highlight_stage(stage_index)

    #  Подсветка активного этапа
    def _highlight_stage(self, index: int):
        for i, btn in enumerate(self.stage_buttons):
            if i == index:
                btn.setFont(self.font_tab_active)
                btn.setStyleSheet(
                    "background-color: #FFFFFF; border-radius: 8px; "
                    "border: none; padding: 10px 24px; color: #1A1A1A;"
                )
            else:
                btn.setFont(self.font_tab)
                btn.setStyleSheet(
                    "background-color: transparent; border-radius: 8px; "
                    "border: none; padding: 10px 24px; color: #6B7B8D;"
                )

    #  Hover-эффект для кнопок этапов
    def eventFilter(self, obj, event):
        from PyQt6.QtCore import QEvent
        if obj in self.stage_buttons:
            index = self.stage_buttons.index(obj)
            is_active = (index == self.current_stage)
            
            if event.type() == QEvent.Type.Enter:
                if not is_active:
                    obj.setStyleSheet(
                        "background-color: #F0F0F0; border-radius: 8px; "
                        "border: none; padding: 10px 24px; color: #1A1A1A;"
                    )
            elif event.type() == QEvent.Type.Leave:
                if not is_active:
                    obj.setStyleSheet(
                        "background-color: transparent; border-radius: 8px; "
                        "border: none; padding: 10px 24px; color: #6B7B8D;"
                    )
        return super().eventFilter(obj, event)

    def _go_to_stage(self, stage_index: int):
        """Переход на указанный этап (0, 1, 2)."""
        if stage_index < 0 or stage_index > 2:
            return

        #Сброс вкладки
        if stage_index == 0:
            self.first_page.reset_to_first_tab()
        elif stage_index == 1:
            self.second_page.reset_to_first_tab()
        elif stage_index == 2:
            self.third_page.reset_to_first_tab()

        self.current_stage = stage_index
        self.stack.setCurrentIndex(stage_index)
        self._highlight_stage(stage_index)