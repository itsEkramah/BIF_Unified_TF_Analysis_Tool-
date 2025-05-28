import os
import qtawesome as qta

from PyQt5.QtCore import (
    Qt, QThread, pyqtSignal,
    QPropertyAnimation, QEasingCurve,
    QTimer
)
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QGridLayout, QGroupBox,
    QScrollArea, QSizePolicy, QPushButton, QGraphicsOpacityEffect
)

from modules.tf_parser import get_tf_results
from modules.tf_summary import get_tf_summary
from modules.network_builder import get_network_pixmap


# ---------------- AnimatedButton ----------------
class AnimatedButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._orig_geo = None
        self._hover_anim = QPropertyAnimation(self, b"geometry", self)
        self._hover_anim.setDuration(150)
        self._hover_anim.setEasingCurve(QEasingCurve.OutCubic)

    def enterEvent(self, ev):
        if self._orig_geo is None:
            self._orig_geo = self.geometry()
        bigger = self._orig_geo.adjusted(-2, -2, +2, +2)
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self.geometry())
        self._hover_anim.setEndValue(bigger)
        self._hover_anim.start()
        super().enterEvent(ev)

    def leaveEvent(self, ev):
        if self._orig_geo:
            self._hover_anim.stop()
            self._hover_anim.setStartValue(self.geometry())
            self._hover_anim.setEndValue(self._orig_geo)
            self._hover_anim.start()
        super().leaveEvent(ev)


# ---------------- fade-in helper ----------------
def fade_in(widget, duration=400, delay=0):
    """
    Fades a widget from 0→1 opacity over `duration` ms,
    optionally starting after `delay` ms,
    then removes the effect so scrolling doesn’t blank it out.
    """
    def _do_fade():
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)

        anim = QPropertyAnimation(effect, b"opacity", widget)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setDuration(duration)
        anim.setEasingCurve(QEasingCurve.Linear)

        # remove the effect when done
        anim.finished.connect(lambda: widget.setGraphicsEffect(None))

        anim.start()

    if delay > 0:
        QTimer.singleShot(delay, _do_fade)
    else:
        _do_fade()


# ---------------- Loading overlay ----------------
class LoadingOverlay(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("loadingOverlay")
        self.setGeometry(parent.rect())
        self.setStyleSheet("background: rgba(255,255,255,0.6);")
        self.movie = QMovie(":/resources/spinner.gif")
        lbl = QLabel(self)
        lbl.setMovie(self.movie)
        lbl.setAlignment(Qt.AlignCenter)
        self.movie.start()
        self.hide()


# ---------------- Background worker ----------------
class AnalysisWorker(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, tf):
        super().__init__()
        self.tf = tf

    def run(self):
        tf_name = self.tf.strip().upper()
        results = get_tf_results(tf_name)
        results["tf_name"] = tf_name
        results["summary"] = get_tf_summary(tf_name)
        self.finished.emit(results)


# ---------------- Main window ----------------
class TFAnalyzerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # load external QSS
        qss_path = os.path.join(os.path.dirname(__file__), "..", "styles", "light_style.qss")
        with open(qss_path) as f:
            self.setStyleSheet(f.read())

        self.setWindowTitle("Unified TF Analysis Tool")
        self.setGeometry(100, 100, 1200, 900)

        # Scrollable container
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)
        main_layout = QVBoxLayout(content)

        # Input bar
        input_layout = QHBoxLayout()
        self.tf_input = QLineEdit()
        self.tf_input.setPlaceholderText("Enter TF name (e.g., TP53)")
        analyze_btn = AnimatedButton(qta.icon("fa5s.search", color="white"), " Analyze")
        analyze_btn.clicked.connect(self.run_analysis)
        input_layout.addWidget(self.tf_input)
        input_layout.addWidget(analyze_btn)
        main_layout.addLayout(input_layout)

        # Grid for result “cards”
        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(16)
        main_layout.addLayout(grid)
        self.sections = {}

        def add_box(title, icon_name, row, col,
                    rowspan=1, colspan=1, height=150, img=False):
            # Create card container
            box = QGroupBox()
            box_layout = QVBoxLayout(box)

            # Header with icon + title
            header = QHBoxLayout()
            icon_lbl = QLabel()
            icon_pix = qta.icon(icon_name).pixmap(16, 16)
            icon_lbl.setPixmap(icon_pix)
            header.addWidget(icon_lbl)
            header.addSpacing(4)
            hdr_lbl = QLabel(f"<b>{title}</b>")
            header.addWidget(hdr_lbl)
            header.addStretch()
            box_layout.addLayout(header)

            # Content widget (table or image)
            if img:
                widget = QLabel("Loading image…", alignment=Qt.AlignCenter)
                widget.setScaledContents(True)
                widget.setMinimumHeight(height)
                widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            else:
                widget = QTextEdit("Loading…")
                widget.setReadOnly(True)
                widget.setMinimumHeight(height)
                widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            box_layout.addWidget(widget)
            grid.addWidget(box, row, col, rowspan, colspan)
            self.sections[title] = widget

        # Add all panels
        add_box("TRRUST Results",      "fa5s.database",      0, 0)
        add_box("CIS-BP Results",      "fa5s.dna",           0, 1)
        add_box("AnimalTFDB Results",  "fa5s.paw",           1, 0)
        add_box("PWM Motif Logo",      "fa5s.code",          1, 1, img=True)
        add_box("TF Summary",          "fa5s.book",          2, 0, 1, 2, height=120)
        add_box("TF Network Diagram",  "fa5s.network-wired", 3, 0, 1, 2, height=240, img=True)
        add_box("E-score Table",       "fa5s.chart-bar",     4, 0)
        add_box("Z-score Table",       "fa5s.chart-line",    4, 1)

        self.setCentralWidget(scroll)
        self.loading = LoadingOverlay(self.centralWidget())

    def run_analysis(self):
        tf = self.tf_input.text().strip()
        if not tf:
            return

        # reset “Loading…” placeholders
        for w in self.sections.values():
            if isinstance(w, QTextEdit):
                w.setText("Loading…")
            else:
                w.setText("Loading image…")

        self.loading.show()
        self.worker = AnalysisWorker(tf)
        self.worker.finished.connect(self.display_results)
        self.worker.start()

    def _fill_html(self, widget, df):
        if df is None or df.empty:
            widget.setHtml("<i>No data available.</i>")
            return

        html = "<table border='1' cellpadding='4'><tr>"
        html += "".join(f"<th>{col}</th>" for col in df.columns) + "</tr>"
        for _, row in df.iterrows():
            html += "<tr>" + "".join(f"<td>{val}</td>" for val in row.values) + "</tr>"
        html += "</table>"
        widget.setHtml(html)

    def display_results(self, r):
        self.loading.hide()

        # tables & summary
        self._fill_html(self.sections["TRRUST Results"],     r.get("trrust_df"))
        self._fill_html(self.sections["CIS-BP Results"],     r.get("cisbp_df"))
        self._fill_html(self.sections["AnimalTFDB Results"], r.get("animaltfdb_df"))
        self.sections["TF Summary"].setText(r.get("summary", "" ))
        self._fill_html(self.sections["E-score Table"],      r.get("escore_df"))
        self._fill_html(self.sections["Z-score Table"],      r.get("zscore_df"))

        # PWM
        pwm_lbl = self.sections["PWM Motif Logo"]
        pwm_path = "pwm_logo.png"
        if os.path.exists(pwm_path):
            pm = QPixmap(pwm_path)
            pwm_lbl.setPixmap(pm.scaled(
                pwm_lbl.width(), pwm_lbl.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        else:
            pwm_lbl.setText("[No PWM image]")

        # Network
        net_lbl = self.sections["TF Network Diagram"]
        px = get_network_pixmap(r.get("trrust_df"), r.get("tf_name"))
        net_lbl.setPixmap(px.scaled(
            net_lbl.width(), net_lbl.height(),
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))

        # staggered fade-ins
        for idx, w in enumerate(self.sections.values()):
            fade_in(w, duration=500, delay=idx * 80)
