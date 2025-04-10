"""
WiP.

Soon.
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import random
import logging.handlers

from typing import TYPE_CHECKING
from typing import Optional, NamedTuple, Literal, Iterable
from pathlib import Path
import logging
import math
import os
import textwrap
from functools import partial
import re
# * Third Party Imports --------------------------------------------------------------------------------->
from pyparsing.exceptions import ParseBaseException

# * Qt Imports --------------------------------------------------------------------------------------->
import PySide6
from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtGui import QFont, QColor, QPalette, QTextOption, QBrush, QMouseEvent, QTextCharFormat, QSyntaxHighlighter, QPainter
from PySide6.QtCore import Qt, Slot, Signal, QTimerEvent, QSize, QAbstractTableModel, QItemSelection
from PySide6.QtWidgets import (QLabel, QWidget, QFormLayout, QStyle, QScrollBar, QLineEdit, QScrollArea, QApplication, QTableView, QFrame, QVBoxLayout, QStyleOption, QStyleOptionViewItem, QComboBox, QSizePolicy, QGroupBox,
                               QTextEdit, QFormLayout, QStyledItemDelegate, QGridLayout, QRadioButton, QCheckBox, QHBoxLayout, QPushButton, QSpacerItem, QTableView,
                               QTableWidget, QTableWidgetItem, QAbstractItemView)

# * Gid Imports ----------------------------------------------------------------------------------------->
from gidapptools.gid_logger.logger import get_main_logger
from gidapptools.gid_logger.handler import GidStoringHandler
from gidapptools.general_helper.conversion import bytes2human
from gidapptools.general_helper.string_helper import StringCaseConverter, StringCase
from gidapptools.gid_parsing.py_log_parsing import GeneralGrammar

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name

from pygments.style import Style as PygmentsStyle
from pygments.lexer import Lexer as PygmentsLexer
from pygments.formatter import Formatter as PygmentsFormatter
from pygments import token as pygments_token
import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


if TYPE_CHECKING:
    from gidapptools.gid_logger.records import LOG_RECORD_TYPES
# endregion [Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion [Logging]

# region [Constants]


THIS_FILE_DIR = Path(__file__).parent.absolute()


# endregion [Constants]


class AppLogHighlighter(QSyntaxHighlighter):
    grammar = GeneralGrammar()
    level_regex = re.compile(r"(?P<level>(DEBUG)|(INFO)|(WARN(ING)?)|(CRITICAL)|(ERROR))")
    line_number_regex = re.compile(r"\| *(?P<line_number>\d+) *\|")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.formats: dict[str, QTextCharFormat] = {}
        self.setup_formats()

    def setup_formats(self):
        self.base_format = QTextCharFormat()

        date_format = QTextCharFormat()
        date_format.setForeground(QColor(0, 0, 0, 255))
        date_format.setTextOutline(QColor(255, 255, 255, 50))
        date_format.setFontWeight(1000)
        self.formats["time_stamp"] = date_format

        line_number_format = QTextCharFormat()
        line_number_format.setForeground(QColor(0, 0, 0, 255))
        line_number_format.setTextOutline(QColor(255, 255, 255, 50))
        line_number_format.setFontWeight(1000)
        self.formats["line_number"] = line_number_format

        level_format = QTextCharFormat()
        level_format.setFontWeight(1000)
        level_format.setFontUnderline(True)
        self.formats["level"] = level_format

        debug_format = QTextCharFormat()
        debug_format.setBackground(QColor(144, 238, 144, 75))
        self.formats["debug"] = debug_format

        info_format = QTextCharFormat()
        info_format.setBackground(QColor(173, 216, 230, 75))
        self.formats["info"] = info_format

        critical_format = QTextCharFormat()
        critical_format.setBackground(QColor(255, 165, 0, 75))
        self.formats["critical"] = critical_format

        error_format = QTextCharFormat()
        error_format.setBackground(QColor(220, 20, 60, 100))
        self.formats["error"] = error_format

        message_format = QTextCharFormat()
        message_format.setFontWeight(1000)
        self.formats["message"] = message_format

        thread_format = QTextCharFormat()
        self.formats["thread"] = thread_format

        module_format = QTextCharFormat()
        self.formats["module"] = module_format

        function_format = QTextCharFormat()
        self.formats["function"] = function_format

    def highlightBlock(self, text: str) -> None:

        # try:
        #     tokens = self.grammar(text)
        #     background_fmt = self.formats[tokens["level"].log_level.casefold()]
        #     self.setFormat(0, len(text), background_fmt)
        #     for name, token in tokens.items():
        #         fmt = self.formats.get(name, self.base_format)
        #         fmt.setBackground(background_fmt.background())
        #         self.setFormat(token.start, token.span, fmt)

        # except ParseBaseException as e:
        # print(f"{e=} | {e.args=}", flush=True)
        if match := self.line_number_regex.search(text):
            self.setFormat(match.start("line_number"), match.end("line_number") - match.start("line_number"), self.formats["line_number"])

        if match := self.level_regex.search(text):
            self.setFormat(0, len(text), self.formats.get(match.group("level").casefold(), self.base_format))

    # def highlightBlock(self, text: str) -> None:
    #     try:
    #         backgrounds = {"debug": QColor(0, 200, 0, 50),
    #                        "info": QColor(0, 0, 255, 50),
    #                        "critical": QColor(255, 200, 0, 50),
    #                        "error": QColor(255, 0, 0, 100)}
    #         if not text.strip():
    #             return
    #         parts = text.split("|")

    #         level_part = parts[2]

    #         start = text.find(level_part)
    #         background = backgrounds.get(level_part.strip().casefold(), QColor(0, 0, 0, 0))
    #         format_item = QTextCharFormat()
    #         format_item.setBackground(background)
    #         self.setFormat(0, text.find("||-->"), format_item)

    #         date_part = parts[0].strip()
    #         start = text.find(date_part)
    #         fmt = self.formats["date"]
    #         fmt.setBackground(background)
    #         self.setFormat(start, len(date_part), fmt)

    #         line_number_part = parts[1].strip()
    #         start = text.find(line_number_part)
    #         fmt = self.formats["line_number"]
    #         fmt.setBackground(background)
    #         self.setFormat(start, len(line_number_part), fmt)

    #         message_start = text.find("||--> ") + 6
    #         self.setFormat(message_start, len(text) - message_start, self.formats["message"])
    #     except IndexError:
    #         pass


class MetaBox(QGroupBox):

    def __init__(self, log_file: Path, parent=None):
        super().__init__(parent=parent)
        self.log_file = log_file
        self.setLayout(QFormLayout())

        self.setTitle("Meta Data")
        self.widgets = {}

        self.setup()

    def _gather_meta_data(self) -> dict[str, str]:
        data = {}
        data["Name"] = self.log_file.name
        data["Path"] = self.log_file.as_posix()
        data["Size"] = bytes2human(self.log_file.stat().st_size)
        data["Lines"] = len(self.log_file.read_text(encoding='utf-8', errors='ignore').splitlines())

        return data

    def setup(self):
        for k, v in self._gather_meta_data().items():
            value_widget = QLabel()
            value_widget.setText(str(v))
            self.layout.addRow(k, value_widget)
            self.widgets[k] = value_widget

    @property
    def layout(self) -> QFormLayout:
        return super().layout()

    def update_size(self):
        size_widget = self.widgets["Size"]
        size_widget.setText(bytes2human(self.log_file.stat().st_size))
        size_widget.repaint()

        line_amount_widget = self.widgets["Lines"]
        line_amount_widget.setText(str(len(self.log_file.read_text(encoding='utf-8', errors='ignore').splitlines())))
        line_amount_widget.repaint()


class FileAppLogViewer(QWidget):

    def __init__(self, log_file: Path, parent=None) -> None:
        super().__init__(parent=parent)
        self.log_file = Path(log_file).resolve()
        self.file_size = None
        self.timer_id = None

    def setup(self) -> "FileAppLogViewer":
        self.setLayout(QGridLayout())
        self.setWindowTitle("Application Log")

        self.setup_widgets()
        self.set_content()
        # self.file_watcher = QFileSystemWatcher(self)
        # self.file_watcher.addPath(str(self.log_file))
        # self.file_watcher.fileChanged.connect(self.set_content)
        # self.file_watcher.fileChanged.connect(self.set_content)
        self.timer_id = self.startTimer(500, Qt.CoarseTimer)
        return self

    def setup_widgets(self):
        self.meta_box = MetaBox(self.log_file)
        self.layout.addWidget(self.meta_box)

        self.text_widget = QTextEdit(self)
        self.text_widget.setReadOnly(True)
        self.text_widget.setLineWrapMode(QTextEdit.NoWrap)
        font: QFont = self.text_widget.font()
        font.setStyleHint(QFont.Monospace)
        font.setFamily("Consolas")
        self.text_widget.setFont(font)

        self.layout.addWidget(self.text_widget)
        self.highlighter = AppLogHighlighter()
        self.highlighter.setDocument(self.text_widget.document())

    def set_content(self):
        self.file_size = self.log_file.stat().st_size
        content = self.log_file.read_text(encoding='utf-8', errors='ignore')
        self.text_widget.setPlainText(content)
        self.resize_to_content()
        self.text_widget.verticalScrollBar().setValue(self.text_widget.verticalScrollBar().maximum())
        self.text_widget.update()
        self.text_widget.repaint()

    def resize_to_content(self):
        height = self.size().height()
        width = min(2000, self.text_widget.document().size().toSize().width())
        self.resize(width, height)

    def check_file(self):
        if self.log_file.stat().st_size != self.file_size:
            self.set_content()
            self.meta_box.update_size()

    def timerEvent(self, event: PySide6.QtCore.QTimerEvent) -> None:
        self.check_file()
        return super().timerEvent(event)

    @property
    def layout(self) -> QGridLayout:
        return super().layout()

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        if self.timer_id is not None:
            self.killTimer(self.timer_id)
        event.accept()


class LogLevelSelector(QGroupBox):
    level_selection_changed = Signal(tuple)

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self._level_widgets: dict[str, QCheckBox] = {}

    @property
    def layout(self) -> QVBoxLayout:
        return super().layout()

    @property
    def all_levels_checked(self) -> bool:
        return all(_level_widget.isChecked() for _level_widget in self._level_widgets.values())

    def get_activated_level_names(self) -> tuple[Literal["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"]]:
        return tuple(name for name, checkbox in self._level_widgets.items() if checkbox.isChecked())

    def _setup_level_widgets(self):
        for level_name in ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"):
            _level_check_box = QCheckBox(level_name, self)
            _level_check_box.checkStateChanged.connect(partial(self.on_level_checkStateChanged, level_name=level_name))
            self._level_widgets[level_name] = _level_check_box
            self.layout.addWidget(_level_check_box)

    def on_level_checkStateChanged(self, state: Qt.CheckState, level_name: str):
        self.level_selection_changed.emit(self.get_activated_level_names())

    def set_all_checked_states(self, checked: bool):
        for _level_check_box in self._level_widgets.values():
            _level_check_box.setChecked(checked)

    def invert_all_checked_states(self):
        for _level_check_box in self._level_widgets.values():
            _level_check_box.setChecked(not _level_check_box.isChecked())

    def setup(self) -> Self:
        self.setTitle("Log Levels")
        self._setup_level_widgets()
        self.set_all_checked_states(True)

        return self

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.RightButton and any(_level_widget.geometry().contains(event.position().toPoint()) for _level_widget in self._level_widgets.values()):

            if self.all_levels_checked is True:
                self.set_all_checked_states(False)
            else:
                self.set_all_checked_states(True)
            event.accept()

        super().mousePressEvent(event)


class StoredAppLogViewer(QWidget):
    closed_signal = Signal()

    def __init__(self,
                 logger: logging.Logger,
                 parent: Optional[PySide6.QtWidgets.QWidget] = None,
                 storage_handler: GidStoringHandler = None) -> None:
        super().__init__(parent)
        self.logger = logger
        if storage_handler is None:
            self.storage_handler: GidStoringHandler = self._try_find_storage_handler()
        else:
            self.storage_handler: GidStoringHandler = storage_handler
        self.last_len = 0
        self.last_active_level_names: frozenset[Literal["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"]] = frozenset(["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"])
        self.timer_id = None

    def _try_find_storage_handler(self) -> logging.Handler:
        logger = self.logger

        while len(logger.handlers) <= 0:
            logger = logging.getLogger(logger.name.rsplit(".", 1)[0])

        all_handlers = list(logger.handlers)

        for _handler in tuple(all_handlers):
            if isinstance(_handler, logging.handlers.QueueHandler):
                for qued_listener in _handler.listener:
                    for qued_handler in qued_listener.handlers:
                        all_handlers.append(qued_handler)

        for handler in tuple(all_handlers):
            if isinstance(handler, GidStoringHandler):
                return handler

        raise ValueError("no storing handler found.")

    def setup(self, initial_level: Literal["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"] | None = None) -> Self:
        self.setLayout(QGridLayout())
        self.setWindowTitle("Application Log")

        self.setup_widgets()
        self.gather_content()
        if self.timer_id is None:
            self.timer_id = self.startTimer(int(5 * 1000), Qt.CoarseTimer)

        return self

    def setup_widgets(self):
        self.text_widget = QTextEdit(self)
        self.text_widget.setReadOnly(True)
        self.text_widget.setLineWrapMode(QTextEdit.NoWrap)
        font: QFont = self.text_widget.font()
        font.setStyleHint(QFont.Monospace)
        font.setFamily("Consolas")
        font.setPointSizeF(font.pointSizeF() * 1.25)
        self.text_widget.setFont(font)
        self.highlighter = AppLogHighlighter()
        self.highlighter.setDocument(self.text_widget.document())
        self.layout.addWidget(self.text_widget)

        self.clear_button = QPushButton("Clear")
        self.clear_button.pressed.connect(self.on_clear_pressed)
        self.layout.addWidget(self.clear_button)

    @ Slot()
    def on_level_selection_changed(self, level_text: str):
        ...

    @ Slot()
    def on_clear_pressed(self, checked: bool = False):
        self.storage_handler.clear()
        self.gather_content()

    @ property
    def layout(self) -> QGridLayout:
        return super().layout()

    def gather_content(self):
        if len(self.storage_handler) != self.last_len:
            all_messages = []
            for message_tuple in self.storage_handler.get_stored_messages().values():
                for raw_message in message_tuple:
                    all_messages.append(raw_message)
            all_messages = sorted(all_messages, key=lambda x: (x.created, x.msecs))
            text = ""
            for msg in all_messages:
                text += self.storage_handler.format(msg) + '\n'
            h_scroll_value = self.text_widget.horizontalScrollBar().value()
            self.text_widget.setPlainText(text)
            self.text_widget.verticalScrollBar().setValue(self.text_widget.verticalScrollBar().maximum())
            self.text_widget.horizontalScrollBar().setValue(h_scroll_value)

            self.last_len = len(self.storage_handler)

    def timerEvent(self, event: PySide6.QtCore.QTimerEvent) -> None:
        self.gather_content()
        return super().timerEvent(event)

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        if self.timer_id is not None:
            self.killTimer(self.timer_id)

        self.closed_signal.emit()
        event.accept()


class HighlightDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.doc = QtGui.QTextDocument(self.parent())
        self._highlight_data: list[tuple[QtCore.QRegularExpression, QtGui.QTextCharFormat]] = []

    def paint(self, painter, option, index):
        painter.save()
        options = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        self.doc.setDefaultFont(options.font)
        self.doc.setPlainText(options.text)

        palette: QPalette = options.palette

        bkgrnd_color = index.data(Qt.ItemDataRole.BackgroundRole)
        if bkgrnd_color:

            palette.setColor(QPalette.ColorRole.Base, bkgrnd_color.color())

        foreground_color = index.data(Qt.ItemDataRole.ForegroundRole)
        if foreground_color:
            palette.setColor(QPalette.ColorRole.Text, foreground_color.color())

        self.apply_highlight()
        options.text = ""
        style = QtWidgets.QApplication.style() if options.widget is None else options.widget.style()
        style.drawControl(QtWidgets.QStyle.CE_ItemViewItem, options, painter)

        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()
        if option.state & QtWidgets.QStyle.State_Selected:
            ctx.palette.setColor(QtGui.QPalette.Text, option.palette.color(
                QtGui.QPalette.Active, QtGui.QPalette.HighlightedText))
        else:
            ctx.palette.setColor(QtGui.QPalette.Text, option.palette.color(
                QtGui.QPalette.Active, QtGui.QPalette.Text))

        textRect = style.subElementRect(
            QtWidgets.QStyle.SE_ItemViewItemText, options)

        if index.column() != 0:
            textRect.adjust(5, 0, 0, 0)

        the_constant = 4
        margin = (option.rect.height() - options.fontMetrics.height()) // 2
        margin = margin - the_constant
        textRect.setTop(textRect.top() + margin)

        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        self.doc.documentLayout().draw(painter, ctx)

        painter.restore()

    def apply_highlight(self):
        for regex, fmt in self._highlight_data:
            cursor = QtGui.QTextCursor(self.doc)
            cursor.beginEditBlock()
            highlightCursor = QtGui.QTextCursor(self.doc)
            while not highlightCursor.isNull() and not highlightCursor.atEnd():
                highlightCursor = self.doc.find(regex, highlightCursor)
                if not highlightCursor.isNull():
                    highlightCursor.mergeCharFormat(fmt)
            cursor.endEditBlock()

    def add_format_item(self, regex: QtCore.QRegularExpression, fmt: QtGui.QTextFormat) -> None:
        self._highlight_data.append((regex, fmt))

    def copy(self, parent=None) -> "HighlightDelegate":
        new_highlight_delegate = self.__class__(parent)

        new_highlight_delegate._highlight_data = list(self._highlight_data)

        return new_highlight_delegate


class ColumnDataItem:

    __slots__ = ("_attr_name",
                 "_display_name",
                 "_alignment",
                 "_delegate",
                 "_set_to_hidden")

    def __init__(self,
                 attr_name: str,
                 display_name: str | None = None,
                 alignment: Qt.AlignmentFlag = None,
                 delegate: QStyledItemDelegate | None = None,
                 hidden: bool = False) -> None:
        self._attr_name = attr_name
        self._display_name = display_name if display_name is not None else self._get_auto_display_name()
        self._alignment = alignment
        self._delegate = delegate
        self._set_to_hidden = hidden

    @property
    def set_to_hidden(self) -> bool:
        return self._set_to_hidden

    @ property
    def attr_name(self) -> str:
        return self._attr_name

    @ property
    def display_name(self) -> str:
        return self._display_name

    @ property
    def alignment(self) -> Qt.AlignmentFlag | None:
        return self._alignment

    @ property
    def delegate(self) -> QStyledItemDelegate | None:
        return self._delegate

    def _get_auto_display_name(self) -> str:
        return StringCaseConverter.convert_to(self.attr_name, StringCase.TITLE)


def get_date_style_delegate(parent=None):
    highlight_delegate = HighlightDelegate(parent)

    date_regex = QtCore.QRegularExpression(r"\d+\-\d+\-\d+")

    date_fmt = QtGui.QTextCharFormat()

    date_fmt.setForeground(QApplication.palette().dark())
    date_fmt.setFontWeight(500)

    highlight_delegate.add_format_item(date_regex, date_fmt)

    time_regex = QtCore.QRegularExpression(r"\d+\:\d+\:\d+\.\d*")

    time_fmt = QtGui.QTextCharFormat()
    QApplication.style
    time_fmt.setForeground(QApplication.palette().placeholderText())

    time_fmt.setFontUnderline(True)

    highlight_delegate.add_format_item(time_regex, time_fmt)

    return highlight_delegate


# _DATE_STYLE_DELEGATE = get_date_style_delegate()


def get_message_style_delegate(parent=None):
    highlight_delegate = HighlightDelegate(parent)

    string_regex = QtCore.QRegularExpression(r"(?P<quotes>\'|\").*?(?P=quotes)")

    string_fmt = QtGui.QTextCharFormat()

    string_fmt.setForeground(QApplication.palette().link())

    string_fmt.setFontItalic(True)

    highlight_delegate.add_format_item(string_regex, string_fmt)

    return highlight_delegate


def _get_style_foreground_color(style: PygmentsStyle) -> str:

    foreground_color = None

    for possible_attr_name in ("foreground", "FOREGROUND"):
        foreground_color = getattr(style, possible_attr_name, None)
        if foreground_color is not None:
            break

    if foreground_color is None:
        foreground_color = style.style_for_token(pygments_token.Token)["color"]

    if foreground_color is None:
        foreground_color = "#ffffff"

    foreground_color = "#" + foreground_color.strip().removeprefix("#")
    return foreground_color


class MessageTableWidgetItem(QTableWidgetItem):

    def __init__(self,
                 msg_item: "LOG_RECORD_TYPES",
                 pygments_style: PygmentsStyle,
                 pygments_lexer: PygmentsLexer,
                 pygments_formatter: PygmentsFormatter,
                 **pygment_formatter_kwargs) -> None:
        super().__init__()
        self.msg_item = msg_item
        self.msg_text = self.msg_item.message + (f"\n{self.msg_item.exc_text}" if self.msg_item.exc_text else "")
        self.pygments_style = pygments_style
        self.pygments_lexer = pygments_lexer
        self.pygments_formatter = pygments_formatter
        self.pygment_formatter_kwargs = dict(pygment_formatter_kwargs)

        self._tooltip_html_text: str | None = None

        self.setText(self.msg_text.split("\n", 1)[0].strip())

    def _create_tooltip_html_text(self) -> str:
        tool_tip_raw_text = self.msg_text.strip()

        tooltip_html_text = highlight(tool_tip_raw_text, self.pygments_lexer, self.pygments_formatter)

        tooltip_html_text = tooltip_html_text.replace("</span><br></pre>", "</span></pre>")

        return tooltip_html_text

    def toolTip(self) -> str:
        if self._tooltip_html_text is None:
            self._tooltip_html_text = self._create_tooltip_html_text()

        return self._tooltip_html_text

    def data(self, role: int) -> PythonLexer:

        if role == Qt.ItemDataRole.ToolTipRole:
            return self.toolTip()

        return super().data(role)


class LogMessageDetailWidget(QScrollArea):

    def __init__(self,

                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.inner_widget: QWidget | None = None
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.clear()
        self.pygment_style = get_style_by_name("github-dark")
        self.pygment_lexer = PythonLexer()
        self.pygment_formatter_kwargs = {"noclasses": True,
                                         "style": self.pygment_style,
                                         "lineseparator": "<br>",
                                         "prestyles": 'font-family: FiraCode Nerd Font Mono, monospace; font-weight: bold'}
        self.pygment_formatter = HtmlFormatter(**self.pygment_formatter_kwargs)

        self.setStyleSheet("QTextEdit#ExceptionTextField {background-color:" + self.pygment_style.background_color + "; color: " + _get_style_foreground_color(self.pygment_style) + ";}")

    def show_log_message(self,
                         log_message: Optional["LOG_RECORD_TYPES"] = None) -> None:
        if log_message is None:
            self.clear()
            return

        self._remove_previous_widget()

        self.inner_widget = QWidget()
        self.inner_widget.setObjectName("LogInnerWidget")
        self.inner_widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        _layout = QFormLayout()
        if log_message is None:
            self.setLayout(_layout)
            return

        _layout.addRow("CLASSNAME: ", QLabel(log_message.__class__.__name__))
        for attr_name in [_attr_name for _attr_name in dir(log_message) if not (_attr_name.startswith("__") and _attr_name.endswith("__"))]:
            _value = getattr(log_message, attr_name, None)

            if callable(_value):
                continue

            if attr_name.casefold() == "message":
                if log_message.levelno == logging.ERROR:

                    _value_widget = QTextEdit()
                    _value_widget.setObjectName("ExceptionTextField")
                    _value_widget.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

                    _value_widget.setWordWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
                    _value_widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
                    _value_widget.setAcceptRichText(True)

                    _html_text = highlight(str(_value), self.pygment_lexer, self.pygment_formatter)

                    _html_text = _html_text.replace("</span><br></pre>", "</span></pre>")
                    _value_widget.setHtml(_html_text)
                    # _value_widget.setText(str(_value))

                else:
                    _value_widget = QTextEdit(str(_value))
                    _value_widget.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

                    _value_widget.setWordWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
                    _value_widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

            else:
                _value_widget = QLineEdit(str(_value))

            _value_widget.setReadOnly(True)
            _font = _value_widget.font()
            _font.setStyleHint(QFont.StyleHint.Monospace)
            _font.setFamily("Consolas")
            _value_widget.setFont(_font)

            # _value_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
            _layout.addRow(StringCaseConverter.convert_to(attr_name, StringCase.TITLE) + ": ", _value_widget)

        _layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        _layout.setSizeConstraint(QFormLayout.SizeConstraint.SetNoConstraint)
        self.inner_widget.setLayout(_layout)

        self.setWidget(self.inner_widget)
        self.setHidden(False)
        self.resize(self.size().width(), self.sizeHint().height())

    def _remove_previous_widget(self) -> None:
        if self.inner_widget is None:
            return

        self.takeWidget()
        self.inner_widget.deleteLater()
        self.inner_widget = None

    def clear(self) -> None:
        self._remove_previous_widget()

        self.setHidden(True)
        self.resize(self.size().width(), 0)


class LogMessagesTableWidget(QTableWidget):

    def mousePressEvent(self, event: QMouseEvent):

        _index = self.indexAt(event.position().toPoint())

        if _index.isValid() is False:
            self.selectionModel().clearSelection()

        super().mousePressEvent(event)


class StoredAppLogTableViewer(StoredAppLogViewer):

    def __init__(self,
                 logger: logging.Logger,
                 parent=None,
                 storage_handler: GidStoringHandler = None) -> None:
        super().__init__(parent=parent, logger=logger, storage_handler=storage_handler)
        self.setLayout(QVBoxLayout())

        self._inner_layout = QGridLayout()
        self.layout.addLayout(self._inner_layout, 1)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)

        self.error_background_color = QColor(Qt.GlobalColor.red)
        self.error_background_color.setAlpha(50)

        self.critical_background_color = QColor.fromRgb(255, 165, 0)
        self.critical_background_color.setAlpha(50)

        self.warning_background_color = QColor(Qt.GlobalColor.yellow)
        self.warning_background_color.setAlpha(50)

        self.debug_background_color = QColor(Qt.GlobalColor.gray)
        self.debug_background_color.setAlpha(50)

        self.debug_foreground_color = QColor(Qt.GlobalColor.darkGray)

        self.pygment_style = get_style_by_name("github-dark")
        self.pygment_lexer = PythonLexer()
        self.pygment_formatter_kwargs = {"noclasses": True,
                                         "style": self.pygment_style,
                                         "lineseparator": "<br>",
                                         "prestyles": 'font-family: FiraCode Nerd Font Mono, monospace; font-weight: bold'}
        self.pygment_formatter = HtmlFormatter(**self.pygment_formatter_kwargs)

        self.setStyleSheet("QToolTip {background-color:" + self.pygment_style.background_color + "; color: " + _get_style_foreground_color(self.pygment_style) + ";}")

        self._loaded_messages: list["LOG_RECORD_TYPES"] = []

    @ property
    def layout(self) -> QVBoxLayout:
        _layout = super().layout
        if callable(_layout):
            _layout = _layout()
        return _layout

    @ property
    def inner_layout(self) -> QGridLayout:
        return self._inner_layout

    def _get_color_map(self):
        return {"background": {"error": ...,
                               "critical": ...,
                               "warning": ...,
                               "info": ...,
                               "debug": ...},
                "foregorund": {"error": ...}}

    def _setup_level_select_widget(self) -> LogLevelSelector:
        level_select_widget = LogLevelSelector(self).setup()

        level_select_widget.level_selection_changed.connect(self.on_level_selection_changed)
        return level_select_widget

    def setup_widgets(self):
        self.level_select_widget = self._setup_level_select_widget()
        self.inner_layout.addWidget(self.level_select_widget, 0, 0, 2, 1)
        self.table_widget = LogMessagesTableWidget(self)
        self.table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.column_data = (ColumnDataItem(attr_name="asctime"),
                            ColumnDataItem(attr_name="levelname", display_name="Level Name", alignment=Qt.AlignmentFlag.AlignCenter),
                            ColumnDataItem(attr_name="name", alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, hidden=True),
                            ColumnDataItem(attr_name="pathname", alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, hidden=True),
                            ColumnDataItem(attr_name="lineno", display_name="Line Number", alignment=Qt.AlignmentFlag.AlignCenter, hidden=True),
                            ColumnDataItem(attr_name="funcName", alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter),
                            ColumnDataItem(attr_name="threadName", alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, hidden=True),
                            ColumnDataItem(attr_name="thread", alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, hidden=True),
                            ColumnDataItem(attr_name="process", alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, hidden=True),
                            ColumnDataItem(attr_name="stack_info", alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, hidden=True),
                            ColumnDataItem(attr_name="exc_info", alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, hidden=True),
                            ColumnDataItem(attr_name="args", alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, hidden=True),
                            ColumnDataItem(attr_name="message", alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter))

        # self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.setHorizontalScrollMode(self.table_widget.ScrollMode.ScrollPerItem)
        self.table_widget.setVerticalScrollMode(self.table_widget.ScrollMode.ScrollPerItem)

        self.table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_widget.setAutoScroll(False)
        self.table_widget.setColumnCount(len(self.column_data))
        self.table_widget.setHorizontalHeaderLabels([item.display_name for item in self.column_data])
        self.table_widget.horizontalHeader().setMinimumSectionSize(100)
        self.table_widget.verticalHeader().setMinimumSectionSize(25)
        # self.table_widget.horizontalHeader().setSectionResizeMode(len(self.column_data) - 1, self.table_widget.horizontalHeader().ResizeMode.Stretch)
        self.table_widget.setWordWrap(False)
        self.table_widget.setTextElideMode(Qt.TextElideMode.ElideNone)
        for column, column_data in enumerate(self.column_data):
            if column_data.delegate is not None:
                column_data.delegate.setParent(self.table_widget)
                self.table_widget.setItemDelegateForColumn(column, column_data.delegate)
            if column_data.set_to_hidden is True:
                self.table_widget.horizontalHeader().setSectionHidden(column, True)

        font: QFont = self.table_widget.font()
        font.setStyleHint(QFont.Monospace)
        font.setFamily("Consolas")
        font.setPointSizeF(font.pointSizeF() * 1.25)
        self.table_widget.setFont(font)

        self.inner_layout.addWidget(self.table_widget, 0, 1, 4, 9)

        self.clear_button = QPushButton("Clear Current Logs")
        self.clear_button.pressed.connect(self.on_clear_pressed)
        self.inner_layout.addWidget(self.clear_button, 3, 0, 1, 1)
        self.inner_layout.setColumnStretch(0, 0)
        self.inner_layout.setColumnStretch(1, 10)

        self.detail_widget = LogMessageDetailWidget()

        self.layout.addWidget(self.detail_widget, 1)

    def setup(self, initial_level: Literal["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"] | None = None) -> Self:
        # self.setLayout(QGridLayout())
        self.setWindowTitle("Application Log")

        self.setup_widgets()

        _active_level_names = ["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"]

        if initial_level is not None and initial_level in _active_level_names:
            _active_level_names = _active_level_names[_active_level_names.index(initial_level):]

            for _lvl_name, _checkbox in self.level_select_widget._level_widgets.items():
                if _lvl_name not in _active_level_names:
                    _checkbox.setChecked(False)

                else:
                    _checkbox.setChecked(True)

        self.gather_content(_active_level_names)

        self.timer_id = self.startTimer(int(0.25 * 1000), Qt.CoarseTimer)

        return self

    @ Slot()
    def on_clear_pressed(self, checked: bool = False):
        current_selected_level_names = self.level_select_widget.get_activated_level_names()
        for _level_name in current_selected_level_names:
            self.storage_handler.clear(_level_name.casefold())
        self.gather_content()
        try:
            self.detail_widget.show_log_message()
        except Exception as e:
            self.logger.error(e, exc_info=True)

    @ Slot()
    def on_level_selection_changed(self, active_level_names: Iterable[Literal["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"]]):
        self.gather_content(active_level_names)

    def gather_content(self, active_level_names: Iterable[Literal["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"]] | None = None):
        active_level_names = frozenset(active_level_names if active_level_names is not None else self.last_active_level_names)
        self._loaded_messages = [r for r in self.storage_handler.get_all_messages(True) if r.levelname.upper() in active_level_names]

        if self.last_active_level_names == active_level_names and len(self._loaded_messages) == self.table_widget.rowCount():
            return

        self.table_widget.clearContents()

        h_scroll_value = self.table_widget.horizontalScrollBar().value()

        self.table_widget.setRowCount(len(self._loaded_messages))

        common_path_prefix = os.path.commonprefix([Path(m.pathname).resolve().as_posix() for m in self._loaded_messages]).removesuffix("/")
        if "/" in common_path_prefix:
            common_path_prefix = "/".join(common_path_prefix.split("/")[:-1])
        for row, msg in enumerate(self._loaded_messages):

            for column, column_data in enumerate(self.column_data):
                if column_data.attr_name == "asctime":
                    item = QTableWidgetItem(self.storage_handler.formatter.formatTime(msg))

                elif column_data.attr_name == "message":
                    item = MessageTableWidgetItem(msg_item=msg, pygments_style=self.pygment_style, pygments_lexer=self.pygment_lexer, pygments_formatter=self.pygment_formatter, **self.pygment_formatter_kwargs)

                elif column_data.attr_name == "pathname":
                    resolved_pathname = Path(msg.pathname).resolve().as_posix()
                    if resolved_pathname.startswith(common_path_prefix):
                        resolved_pathname = resolved_pathname.replace(common_path_prefix, "...", 1)

                    item = QTableWidgetItem(resolved_pathname)

                else:
                    value = getattr(msg, column_data.attr_name)

                    text = "" if value is None else str(value)

                    item = QTableWidgetItem(text)

                if column_data.alignment is not None:
                    item.setTextAlignment(column_data.alignment)

                _pathname = Path(msg.pathname).resolve()

                if column_data.attr_name != "message":
                    item.setToolTip(f"{_pathname.as_posix()!s}")

                match msg.levelname.casefold():
                    case "error":

                        item.setBackground(self.error_background_color)

                    case "critical":

                        item.setBackground(self.critical_background_color)

                    case "warning" | "warn":

                        item.setBackground(self.warning_background_color)

                    case "debug":

                        item.setBackground(self.debug_background_color)

                        item.setForeground(self.debug_foreground_color)

                    case "info":
                        pass

                self.table_widget.setItem(row, column, item)
            if msg.exc_text:
                self.table_widget.resizeRowToContents(row)
        self.table_widget.setHorizontalScrollMode(self.table_widget.ScrollMode.ScrollPerPixel)
        self.table_widget.setVerticalScrollMode(self.table_widget.ScrollMode.ScrollPerPixel)
        self.table_widget.verticalScrollBar().setValue(self.table_widget.verticalScrollBar().maximum())
        self.table_widget.horizontalScrollBar().setValue(h_scroll_value)

        # self.table_widget.verticalScrollBar().setRange(0, len(self._loaded_messages) * 5)
        self.table_widget.verticalScrollBar().setSingleStep(2)
        self.table_widget.verticalScrollBar().setPageStep(len(self._loaded_messages))

        # self.table_widget.verticalScrollBar().setPageStep(len(self._loaded_messages) * 5)

        # self.table_widget.horizontalScrollBar().setRange(0, len(self.column_data) * 2)
        self.table_widget.horizontalScrollBar().setSingleStep(2)
        self.table_widget.horizontalScrollBar().setPageStep(len(self.column_data))

        # self.table_widget.horizontalScrollBar().setPageStep(len(self.column_data) * 2)

        self.last_len = self.table_widget.rowCount()
        self.last_active_level_names = frozenset(active_level_names)

        if self.table_widget.rowCount() > 0:

            self.table_widget.resizeColumnsToContents()
            self.table_widget.resizeRowsToContents()

        self.table_widget.resizeColumnsToContents()

        # self.table_widget.clicked.connect(self.on_item_activated)
        self.table_widget.selectionModel().selectionChanged.connect(self._clear_detail_if_not_item)

    @Slot()
    def _clear_detail_if_not_item(self, new_selection: QItemSelection, old_selection: QItemSelection):
        _indexes = [i for i in new_selection.indexes() if i is not None]

        if len(_indexes) <= 0:
            self.detail_widget.clear()

        else:
            self.on_item_activated(self.table_widget.itemFromIndex(_indexes[-1]))

    @Slot()
    def on_item_activated(self, item: Optional[QTableWidgetItem] = None, old_item: Optional[QTableWidgetItem] = None) -> None:
        if item is None:
            self.detail_widget.clear()

        else:
            try:

                self.detail_widget.show_log_message(self._loaded_messages[item.row()])
            except Exception as e:
                self.logger.error(e, exc_info=True)
        self.update()

    def timerEvent(self, event: QTimerEvent) -> None:
        event.accept()
        self.gather_content(active_level_names=self.level_select_widget.get_activated_level_names())


class LogMessageModel(QAbstractTableModel):

    def __init__(self,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)


# region [Main_Exec]
if __name__ == '__main__':
    pass

# endregion [Main_Exec]
