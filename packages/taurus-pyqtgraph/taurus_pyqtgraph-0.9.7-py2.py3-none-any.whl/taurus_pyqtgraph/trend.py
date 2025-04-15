#!/usr/bin/env python

#############################################################################
##
# This file is part of Taurus
##
# http://taurus-scada.org
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Taurus is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Taurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################
from __future__ import absolute_import

__all__ = ["TaurusTrend"]

import copy
import traceback

from pyqtgraph import PlotWidget
from taurus.core.util.containers import LoopList
from taurus.core.util.log import Logger
from taurus.external.qt import QtGui, PYSIDE2, QtWidgets
from taurus.external.qt.QtCore import QTimer
from taurus.qt.qtcore.configuration import BaseConfigurableClass

from taurus_pyqtgraph.statisticstool import StatisticsTool
from .archivingtool import ArchivingTool
from .autopantool import XAutoPanTool
from .buffersizetool import BufferSizeTool
from .curveproperties import CURVE_COLORS, RangeOptions, set_range_on_trend
from .curvespropertiestool import CurvesPropertiesTool
from .datainspectortool import DataInspectorTool
from .dateaxisitem import DateAxisItem
from .forcedreadtool import ForcedReadTool
from .legendtool import PlotLegendTool
from .taurusmodelchoosertool import TaurusXYModelChooserTool
from .taurustrendset import TaurusTrendSet
from .y2axis import Y2ViewBox
from .titlepatterneditor import TitlePatternEditor, EVALUATION_KEYS

# try:
#     from pyhdbpp import get_default_reader
#
#     archiving_reader = get_default_reader()
# except Exception:
#     archiving_reader = None

# SECONDS_48_HOURS = 172800
# DEFAULT_PLOT_DECIMATION = 1080


class TaurusTrend(PlotWidget, BaseConfigurableClass):
    """
    TaurusTrend is a general widget for plotting the evolution of a value
    over time. It is an extended taurus-aware version of
    :class:`pyqtgraph.PlotWidget`.

    Apart from all the features already available in a regular PlotWidget,
    TaurusTrend incorporates the following tools/features:

        - Secondary Y axis (right axis)
        - Time X axis
        - A plot configuration dialog, and save/restore configuration
          facilities
        - A menu option for adding/removing taurus  models
        - A menu option for showing/hiding the legend
        - Automatic color change of curves for newly added models

    """

    def __init__(self, parent=None, **kwargs):

        buffer_size = kwargs.pop("buffer_size", 65536)

        if PYSIDE2:
            # Workaround for https://bugreports.qt.io/browse/PYSIDE-1564
            BaseConfigurableClass.__init__(self)
            PlotWidget.__init__(self, parent=parent, **kwargs)
        else:
            super(TaurusTrend, self).__init__(parent=parent, **kwargs)

        # Compose with a Logger
        self._logger = Logger(name=self.__class__.__name__)
        self.debug = self._logger.debug
        self.info = self._logger.info
        self.warning = self._logger.warning
        self.error = self._logger.error

        # set up cyclic color generator
        self._curveColors = LoopList(CURVE_COLORS)
        self._curveColors.setCurrentIndex(-1)

        self.titlePatternEditor = TitlePatternEditor()

        plot_item = self.getPlotItem()
        menu = plot_item.getViewBox().menu

        # add trends clear action
        clearTrendsAction = QtGui.QAction("Clear trends", menu)
        clearTrendsAction.triggered.connect(self.clearTrends)
        menu.addAction(clearTrendsAction)

        # add save & retrieve configuration actions
        saveConfigAction = QtGui.QAction("Save configuration", menu)
        saveConfigAction.triggered.connect(self._onSaveConfigAction)
        menu.addAction(saveConfigAction)

        loadConfigAction = QtGui.QAction("Retrieve saved configuration", menu)
        loadConfigAction.triggered.connect(self._onLoadConfigAction)
        menu.addAction(loadConfigAction)

        # add change curve labels
        changeCurvesTitlesAction = QtGui.QAction("Change Curves Titles "
                                                 "(All curves)...", menu)
        changeCurvesTitlesAction.triggered.connect(
            self._onChangeCurvesTitlesAction)
        menu.addAction(changeCurvesTitlesAction)

        # # set up archiving functionality
        # self._archiving_enabled = False
        # self._archiving_reader = None
        # self._ask_for_decimation = True
        # self._decimation_activated = True
        # self._decimate_period = True
        # self._auto_reload_checkbox = None
        # self._dismiss_archive_message = False
        # if self._setArchivingReader():
        #     self._loadArchivingContextActions()

        # Add archiving tool to trend
        self._archiving_tool = ArchivingTool(self)

        self.registerConfigProperty(self._getState, self.restoreState, "state")
        self.registerConfigProperty(self._getDynamicRange,
                                    self.restoreDynamicRange, "dynamicRange")
        # self.registerConfigProperty(
        #     lambda: self.getAxisLogMode("left"),
        #     lambda enabled: self.setAxisLogMode("y", isEnabled=enabled),
        #     "leftAxisLogMode")

        # self.registerConfigProperty(
        #     lambda: self.getAxisLogMode("bottom"),
        #     lambda enabled: self.setAxisLogMode("x", isEnabled=enabled),
        #     "bottomAxisLogMode")

        # add legend tool
        legend_tool = PlotLegendTool(self)
        legend_tool.attachToPlotItem(plot_item)

        # add model chooser
        self._model_chooser_tool = TaurusXYModelChooserTool(
            self, itemClass=TaurusTrendSet, showX=False
        )
        self._model_chooser_tool.attachToPlotItem(
            self.getPlotItem(), self, self._curveColors
        )

        # add statistics tool
        self._statistics_tool = StatisticsTool(self, itemClass=TaurusTrendSet)
        self._statistics_tool.attachToPlotItem(self.getPlotItem(), self)

        # add Y2 axis
        self._y2 = Y2ViewBox()
        self._y2.attachToPlotItem(self.getPlotItem())

        # Add time X axis
        axis = DateAxisItem(orientation="bottom")
        axis.attachToPlotItem(plot_item)

        # add plot configuration dialog
        self._cprop_tool = CurvesPropertiesTool(self)
        self._cprop_tool.attachToPlotItem(plot_item, y2=self._y2)

        # add data inspector widget
        inspector_tool = DataInspectorTool(self)
        inspector_tool.attachToPlotItem(self.getPlotItem())

        # add force read tool
        self._fr_tool = ForcedReadTool(self)
        self._fr_tool.attachToPlotItem(self.getPlotItem())

        # add buffer size tool
        self.buffer_tool = BufferSizeTool(self, buffer_size=buffer_size)
        self.buffer_tool.attachToPlotItem(self.getPlotItem())

        # Add the auto-pan ("oscilloscope mode") tool
        self._autopan = XAutoPanTool()
        self._autopan.attachToPlotItem(self.getPlotItem())

        # add Set View Range actions
        x_axis_menu = self.plotItem.x_axis_menu

        label = QtGui.QLabel("Set View Range: ")
        label.setObjectName("range_label")
        self.combo_box = QtGui.QComboBox(self)
        self.combo_box.setObjectName("range_combo_box")
        self.combo_box.setEditable(True)
        for option in RangeOptions:
            self.combo_box.addItem(str(option))

        x_axis_menu.addWidget(label, 8, 0, 1, 2)
        x_axis_menu.addWidget(self.combo_box, 8, 2, 1, 2)

        self.combo_box.activated.connect(self._on_range_idx_changed)

        # Register config properties
        self.registerConfigDelegate(self._model_chooser_tool, "XYmodelchooser")
        # self.registerConfigDelegate(self._y2, "Y2Axis")
        self.registerConfigDelegate(self._cprop_tool, "CurvePropertiesTool")
        self.registerConfigDelegate(legend_tool, "legend")
        self.registerConfigDelegate(self._fr_tool, "forceread")
        self.registerConfigDelegate(self.buffer_tool, "buffer")
        self.registerConfigDelegate(inspector_tool, "inspector")

    def __getitem__(self, idx):
        """
        Provides a list-like interface: items can be accessed using slice
        notation
        """
        return self._getCurves()[idx]

    def __len__(self):
        return len(self._getCurves())

    def __bool__(self):
        return True

    def _on_range_idx_changed(self):
        time_range = self.combo_box.currentText()
        plot_item = self.getPlotItem()
        set_range_on_trend(time_range, plotItem=plot_item)
        plot_item.getViewBox().menu.close()

    def _getCurves(self):
        """returns a flat list with all items from all trend sets"""
        ret = []
        for ts in self.getTrendSets():
            ret += ts[:]
        return ret

    def getTrendSets(self):
        """Returns all the trend sets attached to this plot item"""
        return [
            e
            for e in self.getPlotItem().listDataItems()
            if isinstance(e, TaurusTrendSet)
        ]

    def clearTrends(self):
        """Clear the buffers of all the trend sets in the plot"""
        for ts in self.getTrendSets():
            ts.clearBuffer()

    def setModel(self, names):
        """Set a list of models"""
        # support passing a string  in names instead of a sequence
        if isinstance(names, str):
            names = [names]
        self._model_chooser_tool.updateModels(names or [])

    def addModels(self, names):
        """Reimplemented to delegate to the  model chooser"""
        # support passing a string in names
        if isinstance(names, str):
            names = [names]
        self._model_chooser_tool.addModels(names)

    def _getState(self):
        """Same as PlotWidget.saveState but removing viewRange conf to force
        a refresh with targetRange when loading
        """
        state = copy.deepcopy(self.saveState())
        # remove viewRange conf
        del state["view"]["viewRange"]
        if self.combo_box.currentText().strip() != "":
            # If a dynamicRange exists the targetRange has to be removed
            del state["view"]["targetRange"]
        return state

    def setXAxisMode(self, x_axis_mode):
        """Required generic TaurusTrend API """
        if x_axis_mode != "t":
            raise NotImplementedError(  # TODO
                'X mode "{}" not yet supported'.format(x_axis_mode)
            )

    def getAxisLogMode(self, axis):
        if axis in ["left", "y"]:
            axis = "left"
        elif axis in ["bottom", "x"]:
            axis = "bottom"

        return self.plotItem.getAxis(axis).logMode

    def setAxisLogMode(self, axis, isEnabled=False):
        """
        Method to change log mode of a desired axis.
        Possible options:
            setAxisLogMode("left", True)
            setAxisLogMode("bottom", True)
            setAxisLogMode("y", True) # The same as left
            setAxisLogMode("x", True) # The same as bottom
        """

        if axis in ["left", "y"]:
            axisObject = self.plotItem.getAxis("bottom")
            try:
                axisObject.setLogMode(y=isEnabled)
            except Exception:
                self.warning("Could not restore log mode for axis {} with "
                             "type  {}.".format(axis, str(type(axisObject))))
                self.warning("Exception: {}".format(traceback.format_exc()))
            axis = "left"
        elif axis in ["bottom", "x"]:
            axisObject = self.plotItem.getAxis("bottom")
            try:
                axisObject.setLogMode(x=isEnabled)
            except Exception:
                self.warning("Could not restore log mode for axis {} with "
                             "type  {}.".format(axis, str(type(axisObject))))
                self.warning("Exception: {}".format(traceback.format_exc()))

            axis = "bottom"
        else:
            axis = False

        if axis:
            menu = self.plotItem.getViewBox().menu

            if hasattr(menu, "axes"):
                x_menu, y_menu = menu.axes
                actions = []
                if axis == "left":
                    actions = y_menu.actions()
                elif axis == "bottom":
                    actions = x_menu.actions()

                for action in actions:
                    if action.text() == "Log scale":
                        action.setChecked(isEnabled)
            else:
                submenus = menu.findChildren(QtWidgets.QMenu)
                menu_title = "Y axis" if axis == "left" else "X axis"
                for submenu in submenus:
                    if submenu.title() == menu_title:
                        for action in submenu.actions():
                            if action.text() == "Log scale":
                                action.setChecked(isEnabled)

    def setForcedReadingPeriod(self, period):
        """Required generic TaurusTrend API """
        self._fr_tool.setPeriod(period)

    def setMaxDataBufferSize(self, buffer_size):
        """Required generic TaurusTrend API """
        self.buffer_tool.setBufferSize(buffer_size)

    def _onSaveConfigAction(self):
        """wrapper to avoid issues with overloaded signals"""
        return self.saveConfigFile()

    def _onLoadConfigAction(self):
        """wrapper to avoid issues with overloaded signals"""
        return self.loadConfigFile()

    def _onChangeCurvesTitlesAction(self):
        """Show pop up to change title on curves"""
        label_config = self.titlePatternEditor.showDialog()

        if label_config:
            for item in self.getTrendSets():
                result = label_config
                for key, resolver in EVALUATION_KEYS.items():
                    if key in self.titlePatternEditor.legend_pattern:
                        try:
                            result = result.replace(key,
                                                    resolver(item.modelObj))
                        except AttributeError:
                            self._logger.warning(traceback.format_exc())
                            result = result.replace(key, "NoDef")

                if len(item) == 1:
                    item[0].setData(name=result)
                    self.plotItem.legend.getLabel(item[0]).setText(result)

                if len(item) > 1:
                    for i in range(len(item)):
                        result_array = "{}[{}]".format(result, i)
                        item[i].setData(name=result_array)
                        (self.plotItem.legend.getLabel(item[i])
                         .setText(result_array))

    def _getDynamicRange(self):
        # get the actual range
        return self.combo_box.currentText()

    def restoreDynamicRange(self, dynamicRange):
        # restore dynamic_range if exists
        # It has to be done after the view is rendered,
        # if not, the restore does not work properly

        def delayed_function():
            if dynamicRange.strip() != "":
                self.combo_box.setCurrentText(dynamicRange)
                set_range_on_trend(dynamicRange, self.getPlotItem())
                self.setAutoVisible(y=True)

        QTimer.singleShot(3000, delayed_function)


def trend_main(
    models=(), config_file=None, demo=False, window_name="TaurusTrend (pg)"
):
    """Launch a TaurusTrend"""
    import sys
    from taurus.qt.qtgui.application import TaurusApplication

    app = TaurusApplication(cmd_line_parser=None, app_name="taurustrend(pg)")

    w = TaurusTrend()

    w.setWindowTitle(window_name)

    if demo:
        models = list(models)
        models.extend(["eval:rand()", "eval:1+rand(2)"])

    if config_file is not None:
        w.loadConfigFile(config_file)

    if models:
        w.setModel(models)

    w.show()
    ret = app.exec_()

    sys.exit(ret)


if __name__ == "__main__":
    trend_main(models=("eval:rand()", "sys/tg_test/1/ampli"),)
