import time
import traceback
import numpy as np

from taurus.external.qt import QtGui, Qt
from taurus.external.qt.Qt import (QDialog, QLabel, QLineEdit,
                                   QPushButton, QVBoxLayout,
                                   QHBoxLayout)

try:
    from pyhdbpp import get_default_reader

    archiving_reader = get_default_reader()
except Exception:
    archiving_reader = None

from .taurustrendset import TaurusTrendSet

DEFAULT_PLOT_DECIMATION = 1080
SECONDS_48_HOURS = 172800


class DecimationConfigDialog(QDialog):
    """
    Custom Input Dialog to retrieve decimation period desired from the user and
    apply the decimation using archiving.
    """
    def __init__(self, parent=None, message="", default_period=0):
        super().__init__(parent)
        self.setWindowTitle("Select Decimation Factor")

        # Create configurable options
        self.selectedOption = "Apply"

        # Create UI elements
        self.label = QLabel(message)
        self.lineEdit = QLineEdit(str(default_period))
        self.applyButton = QPushButton("Apply")
        self.cancelButton = QPushButton("Cancel")
        self.defaultButton = QPushButton("Restore default")

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.cancelButton)
        buttons_layout.addWidget(self.defaultButton)
        buttons_layout.addWidget(self.applyButton)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        # Connect signals to slots
        self.applyButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        self.defaultButton.clicked.connect(self.setDefaultDecimation)

    def setDefaultDecimation(self):
        self.selectedOption = "Default"
        self.accept()

    def getInputText(self):
        return self.lineEdit.text()


class ArchivingTool:
    def __init__(self, parent):
        self.parent = parent
        # set up archiving functionality
        self._archiving_enabled = False
        self._archiving_reader = None
        self._decimation_activated = True
        self._decimate_period = "Default"
        self._auto_reload_checkbox = None
        self._dismiss_archive_message = False
        if self._setArchivingReader():
            self._loadArchivingContextActions()

    def _loadArchivingContextActions(self):
        """Loads archiving options to context menu on the trend (right-click)
        and enables triggers regarding archiving.
        """
        menu = self.parent.plotItem.getViewBox().menu

        archiving_menu = QtGui.QMenu("Archiving", menu)
        menu.addMenu(archiving_menu)

        self._auto_reload_checkbox = QtGui.QAction(
            "Autoreload", archiving_menu
        )
        self._auto_reload_checkbox.setCheckable(True)
        self._auto_reload_checkbox.setChecked(False)
        self._auto_reload_checkbox.triggered.connect(
            self._onEnableDisableArchivingClicked
        )

        load_once_action = QtGui.QAction("Load Once (Ctrl+L)", archiving_menu)
        load_once_action.triggered.connect(self._loadArchivingDataOnce)

        load_once_shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+L"),
                                             self.parent)
        load_once_shortcut.activated.connect(self._loadArchivingDataOnce)

        decimate_and_redraw = QtGui.QAction("Decimate and Redraw (Ctrl+R)",
                                            archiving_menu)
        decimate_and_redraw.triggered.connect(self._decimate_and_redraw)

        configure_decimation = QtGui.QAction("Configure decimation",
                                             archiving_menu)
        configure_decimation.triggered.connect(self._configure_decimation)

        decimate_shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"),
                                            self.parent)
        decimate_shortcut.activated.connect(self._decimate_and_redraw)

        archiving_menu.addAction(self._auto_reload_checkbox)
        archiving_menu.addAction(load_once_action)
        archiving_menu.addAction(decimate_and_redraw)
        archiving_menu.addAction(configure_decimation)

    def _configure_decimation(self):
        msg_dec = ("Enter decimation period in seconds.\n"
                   "If you click 'Restore Default' it will use the "
                   "recommended value.\n")
        self._decimate_period = (self._askDecimationPeriod(msg_dec, 0))
        if self._decimate_period is None:
            self._decimate_period = True

        self._decimate_and_redraw()

    def _decimate_and_redraw(self):
        self.parent.clearTrends()
        self._decimation_activated = True
        self._loadArchivingData(loadOnce=True)

    def _loadArchivingDataOnce(self):
        self._loadArchivingData(loadOnce=True)

    def _onEnableDisableArchivingClicked(self):
        """Change the state of boolean archiving_enabled to the opposite
        of their actual value. If it's set to True a connection between
        sigRangeChanged and local function on_changed_trend is set,
        otherwise, the connection gets disconnected.
        """
        self._archiving_enabled = not self._archiving_enabled

        if self._archiving_enabled:
            self.parent.sigRangeChanged \
                .connect(lambda: self._loadArchivingData(loadOnce=False))
            self.parent.info("Archiving option set to enabled")
            self._loadArchivingData(loadOnce=False)  # Force first data query
        else:
            self.parent.sigRangeChanged.disconnect()
            self.parent.info("Archiving option set to disabled")

    def _setArchivingReader(self):
        """Try to set up a reader and return if it was possible or not
        (True/False). :return: True if reader is set or False if not
        """
        if archiving_reader:
            self._archiving_reader = archiving_reader
            self.parent.info("Archiving reader set")
            return True
        else:
            self.parent.info("Archiving reader not set")
            return False

    def _loadArchivingData(self, loadOnce=False):
        """When there is a change on the Range of view perform
        a query to get archiving data and append it to the left.
        """

        for taurus_trend_set in self.parent.plotItem.dataItems:
            if not isinstance(taurus_trend_set, TaurusTrendSet):
                continue
            try:
                range_left = self.parent.visibleRange().left()
                range_right = self.parent.visibleRange().right()
                if range_right > time.time():
                    range_right = time.time()

                plot_time_range = range_right - range_left

                if len(taurus_trend_set._xBuffer):
                    buffer_first = taurus_trend_set._xBuffer[0]
                    buffer_last = taurus_trend_set._xBuffer[-1]

                    if (range_right <= buffer_first
                       or buffer_last <= range_left):
                        query_start, query_end = range_left, range_right
                        query_window = plot_time_range

                    else:
                        if (buffer_first <= range_left
                           and range_right <= buffer_last):
                            # The plotting range is already within buffer!
                            query_start, query_end = range_left, range_right
                            query_window = plot_time_range

                        # DO NOT CHANGE THE ORDER OF THIS IFS, IT MATTERS
                        # WHEN MODIFYING CURRENT TIME WINDOW
                        elif range_left < buffer_first < range_right:
                            query_start, query_end = range_left, buffer_first
                            query_window = buffer_first - range_left

                        elif range_left < buffer_last < range_right:
                            query_start, query_end = buffer_last, range_right
                            query_window = query_end - query_start

                else:
                    query_start, query_end = range_left, range_right
                    buffer_first = buffer_last = time.time()
                    query_window = plot_time_range

                is_valid_query = query_window > (.15 * plot_time_range) > 1

                if is_valid_query and (buffer_first <= range_left
                   and range_right <= buffer_last):
                    buttonClicked = self._askForConfirmation(
                        "This query will rewrite existing plot buffers",
                        buttons=(QtGui.QMessageBox.Ok
                                 | QtGui.QMessageBox.Cancel))
                    if buttonClicked == QtGui.QMessageBox.Ok:
                        self.parent.clearTrends()
                    else:
                        is_valid_query = False

                if is_valid_query:

                    from_date = time.strftime('%Y-%m-%dT%H:%M:%S',
                                              time.localtime(query_start))
                    to_date = time.strftime('%Y-%m-%dT%H:%M:%S',
                                            time.localtime(query_end))

                    if self._checkForQuerySizeAndUserConfirmation(
                       query_start, query_end, taurus_trend_set.modelName):
                        try:
                            Qt.QApplication.instance().setOverrideCursor(
                                Qt.QCursor(Qt.Qt.CursorShape.BusyCursor)
                            )
                            if self._decimation_activated:
                                if self._decimate_period == "Default":
                                    decimate = True
                                else:
                                    decimate = (self._decimate_period
                                                if self._decimate_period > 0
                                                else False)
                            else:
                                decimate = False

                            values = self._archiving_reader \
                                .get_attribute_values(
                                    taurus_trend_set.modelName,
                                    from_date, to_date, decimate=decimate)

                            self.parent.info(
                                "loadArchivingData({}, {}, {}, {}): {} values"
                                .format(taurus_trend_set.modelName,
                                        from_date, to_date,
                                        decimate, len(values)))

                        except KeyError as ke:
                            values = None
                            self.parent.debug(
                                "Attribute '{}' has no archiving data".format(
                                    ke))
                        finally:
                            Qt.QApplication.instance().restoreOverrideCursor()

                        if values is not None and len(values):
                            if (len(values) + len(taurus_trend_set._xBuffer)) \
                                    < self.parent.buffer_tool.bufferSize():
                                self.parent.debug(
                                    "left-appending historical data from {} "
                                    "to {}".format(from_date, to_date))

                                ntrends = 1
                                if len(taurus_trend_set._yBuffer):
                                    ntrends = np.prod(taurus_trend_set._yBuffer
                                                      .contents().shape[1:])
                                else:
                                    try:
                                        for v in values:
                                            if v is not None:
                                                ntrends = np.size(v[1])
                                                break
                                    except Exception:
                                        pass

                                if ntrends <= 1:
                                    x = np.array([v[0] for v in values])
                                    y = np.array([v[1] for v in values])
                                    y.shape = (len(x), 1)
                                else:
                                    x, y = [], []
                                    for v in values:
                                        if (v[1] is not None
                                                and len(v[1]) == ntrends):
                                            x.append(v[0])
                                            y.append(v[1])

                                    x = np.array(x)
                                    y = np.array(y)
                                    y.shape = (len(x), ntrends)

                                try:
                                    if query_start >= buffer_last:
                                        taurus_trend_set._xBuffer.extend(x)
                                        taurus_trend_set._yBuffer.extend(y)
                                    else:
                                        taurus_trend_set._xBuffer.extendLeft(x)
                                        taurus_trend_set._yBuffer.extendLeft(y)

                                    taurus_trend_set._update()

                                except ValueError as e:
                                    import traceback
                                    traceback.print_exc()
                                    self.parent.error(
                                        "Error left-appending data "
                                        "to buffer.\n", e
                                    )
                            else:
                                msg = ("Buffer size is surpassing limit and "
                                       "data has been discarded.\n"
                                       "You can change the buffer size at "
                                       "your "
                                       "own responsibility and try again.")
                                if loadOnce:
                                    self._askForConfirmation(msg, buttons=QtGui
                                                             .QMessageBox.Ok)
                                else:
                                    msg += "\nAuto reload has been disabled"
                                    self._disableAutoReloadAndDiscardData(msg)
                                    return
                    else:
                        if not loadOnce:
                            msg = "Data from archiving has been discarded " \
                                  "and reload disabled"
                            self._disableAutoReloadAndDiscardData(msg)
                        break

            except Exception as e:
                import traceback
                traceback.print_exc()
                self.parent.warning(
                    "Error updating trend set of model {} "
                    "with error {}".format(taurus_trend_set.modelName, e)
                )

    def _disableAutoReloadAndDiscardData(self, message):
        self._askForConfirmation(message, buttons=QtGui.QMessageBox.Ok)
        self.info(message)
        self._auto_reload_checkbox.setChecked(False)
        self._onEnableDisableArchivingClicked()  # Force a trigger

    def _checkForQuerySizeAndUserConfirmation(self, from_date, to_date,
                                              model_name):

        hours = int((to_date - from_date) / 3600.)

        msg = "You are querying {} hours for {}".format(hours, model_name)

        min_dec = (to_date - from_date) / self.parent.buffer_tool.bufferSize()
        recommended = int((to_date - from_date) / DEFAULT_PLOT_DECIMATION) or 1
        if self._decimate_period == "Default":
            dec = recommended
        elif isinstance(self._decimate_period, (int, float)):
            msg += " (decimated every {} s)".format(self._decimate_period)
            dec = self._decimate_period
        else:
            dec = 10
        if dec < min_dec:
            dec = min_dec + 1

        if self._decimation_activated:
            if self._decimate_period is None:
                self._decimate_period = True
                return True

        if to_date - from_date > SECONDS_48_HOURS:
            if not self._dismiss_archive_message:
                msg += "This may take a while\n"
                msg += "\nContinue? (Yes to All disables this message)"
                buttonClicked = self._askForConfirmation(msg)
                self._dismiss_archive_message = \
                    buttonClicked == QtGui.QMessageBox.YesToAll
                return buttonClicked in [QtGui.QMessageBox.Ok,
                                         QtGui.QMessageBox.YesToAll]

        return True

    def _askDecimationPeriod(self, message, min_period):
        period = self._decimate_period

        ask_period = DecimationConfigDialog(message=message,
                                            default_period=period)
        if ask_period.exec_():
            _selectedOption = ask_period.selectedOption

            if (_selectedOption == "Default"
               or ask_period.getInputText() in ["Default", "True"]):
                self._decimation_activated = True
                return "Default"
            elif _selectedOption == "Apply":
                self._decimation_activated = True

            try:
                r = float(ask_period.getInputText())

                if r and r < min_period:
                    msg = (
                        "Buffer size may be surpassed, and then"
                        "data will be discarded.\n"
                        "If it occurs, you can change the buffer size "
                        "at your own responsibility and try again."
                    )
                    buttonclicked = \
                        self._askForConfirmation(
                            msg,
                            buttons=QtGui.QMessageBox.Ok | QtGui.
                            QMessageBox.Cancel
                        )
                    if buttonclicked == QtGui.QMessageBox.Cancel:
                        return None
                return r
            except ValueError:
                traceback.print_exc()
                self.parent.warning(
                    "Cannot cast from {} to float, applying "
                    "default".format(ask_period.getInputText())
                )
                return None
        else:
            return None

    def _askForConfirmation(self, message,
                            buttons=QtGui.QMessageBox.Ok | QtGui.QMessageBox
                            .YesToAll | QtGui.QMessageBox.Cancel):
        warn_user = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Warning!",
                                      message, buttons)
        return warn_user.exec_()

    def configure_decimation_options(self, activate_decimation=True,
                                     decimate_period=True):
        """
        Method used to activate or deactivate the decimation feature from code.

        Args:
            activate_decimation (bool): Activate or not the decimation
            decimate_period ("Default", True, int, float):
             True or "Default": Enables decimation to be determined by PyHDB++.
             int,float: Set in seconds the period of decimation.
        """

        self._decimation_activated = activate_decimation
        self._decimate_period = decimate_period
