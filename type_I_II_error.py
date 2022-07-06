from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QMessageBox
from matplotlib.pyplot import draw
from scipy.stats import norm
import pyqtgraph as pg
import numpy as np
import sys



class mymainform(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(mymainform, self).__init__(*args, **kwargs)
        uic.loadUi("type_i_ii_error.ui", self)


        self.graph.setBackground("#2B3B84")
        self.show_type_i.stateChanged.connect(self._show_type_i)
        self.show_type_ii.stateChanged.connect(self._show_type_ii)
        self.show_power.stateChanged.connect(self._state_power)
        self.h0mu.returnPressed.connect(self.update_plot)
        self.hamu.returnPressed.connect(self.update_plot)
        self.type_i_error.returnPressed.connect(self.update_plot)
        self.exit.clicked.connect(self._leaving)
        


    def update_plot(self):
        # return to default setting--------------------------
        self.graph.clear()
        self.show_type_i.setChecked(False)
        self.show_type_ii.setChecked(False)
        self.show_power.setChecked(False)

        try:
            global h0mu, hamu    
            h0mu = float(self.h0mu.text())
            hamu = float(self.hamu.text())
            self.power_typeiierror_calculate()

            # basic plot setting-------------------------------
            penh0 = pg.mkPen(color = "#3DFCFF", width = 4.5)
            penha = pg.mkPen(color = "#FFC327", width = 4.5)
            lgpen = pg.mkPen(color = "white", width = 1)
            font = QtGui.QFont()
            font.setPixelSize(20)
            self.graph.getAxis("bottom").setStyle(tickFont = font)
            self.graph.getAxis("bottom").setTextPen("white")
            self.graph.getAxis("left").setStyle(tickFont = font)
            self.graph.getAxis("left").setTextPen("white")
            # -------------------------------------------------
            global x0, y0, xa, ya
            
            x0 = np.linspace(h0mu - 6.5, h0mu + 6.5, 1000)
            y0 = norm.pdf(x0, loc = h0mu, scale = 1)

            xa = np.linspace(hamu - 6.5, hamu + 6.5, 1000)
            ya = norm.pdf(xa, loc = hamu, scale = 1)

            self.graph.addLegend(pen = lgpen)
            self.graph.plot(x0, y0, pen = penh0,  name = "<p style = 'font-size: 14pt; color: #B5FFA3; font-weight: bold'>Null Hypothesis</p>")
            self.graph.plot(xa, ya, pen = penha, name = "<p style = 'font-size: 14pt; color: #B5FFA3; font-weight: bold'>True Parameter</p>")
        except ValueError:
            self.exception_dialog_value_error()
        
       


            
    def draw_type_i_error(self):
            # fill the area of type I error at the left tail-----------------------
            left_x_low = np.min(x0)
            left_x_high = norm.ppf(float(self.type_i_error.text()) / 2, loc = h0mu, scale = 1)
            x_left = np.linspace(left_x_low, left_x_high, 300)
            y_left = norm.pdf(x_left, loc = h0mu, scale = 1)
            left_curv = pg.PlotCurveItem(x = x_left, y = y_left)
            left_zero = pg.PlotCurveItem(x = x_left, y = np.zeros(len(x_left)))
            self.fill_1 = pg.FillBetweenItem(left_curv, left_zero, brush = "g")
            self.graph.addItem(self.fill_1)
            # ---------------------------------------------------------------------

            # fill the area of type I error at the right tail
            righ_x_low = norm.ppf(1 - (float(self.type_i_error.text()) / 2), loc = h0mu, scale = 1)
            right_x_high = np.max(x0)
            x_right = np.linspace(righ_x_low, right_x_high, 300)
            y_right = norm.pdf(x_right, loc = h0mu, scale = 1)
            right_curv = pg.PlotCurveItem(x = x_right, y = y_right)
            right_zero = pg.PlotCurveItem(x = x_right, y = np.zeros(len(x_right)))
            self.fill_2 = pg.FillBetweenItem(right_curv, right_zero, brush = "g")
            self.graph.addItem(self.fill_2)
            # ---------------------------------------------------------------------
            
# function for removing the type i error plot item---------------
    def remove_type_i_error(self):
        self.graph.removeItem(self.fill_1)
        self.graph.removeItem(self.fill_2)
# ---------------------------------------------------------------------


# function for determine the state of checkbox of type i error
    def _show_type_i(self, s):
        if s == 2:
            self.draw_type_i_error()
        else:
            self.remove_type_i_error()
# ---------------------------------------------------------------------

# funtion for drawing the type ii error--------------------
    def draw_type_ii_error(self, s):
        left = norm.ppf(float(self.type_i_error.text()) / 2, loc = h0mu, scale = 1)
        right = norm.ppf(1 - (float(self.type_i_error.text()) / 2), loc = h0mu, scale = 1)
        x = np.linspace(left, right, 300)
        y = norm.pdf(x, loc = hamu, scale = 1)
        curv1 = pg.PlotCurveItem(x = x, y = y)
        curv2 = pg.PlotCurveItem(x = x, y = np.zeros(len(x)))
        self.fill_typeiierror = pg.FillBetweenItem(curv1, curv2, brush = "#f25449")
        self.graph.addItem(self.fill_typeiierror)
# ----------------------------------------------------------


# function for removing the type ii error item
    def remove_type_ii_error(self):
        self.graph.removeItem(self.fill_typeiierror)
# ----------------------------------------------------------


# function for determine the state of checkbox of type ii error
    def _show_type_ii(self, s):
        if s == 2:
            self.draw_type_ii_error(s)
        else:
            self.remove_type_ii_error()
# ----------------------------------------------------------


# function for drawing the power-------------
    def draw_power(self): 
        # fill the power area for left tail
        left_x_low = np.min(xa)
        left_x_high = norm.ppf((float(self.type_i_error.text()) / 2), loc = h0mu, scale = 1) 
        x_left = np.linspace(left_x_low, left_x_high, 300)
        y_left = norm.pdf(x_left, loc = hamu, scale = 1)
        left_curv = pg.PlotCurveItem(x = x_left, y = y_left)
        left_zero = pg.PlotCurveItem(x = x_left, y = np.zeros(len(x_left)))
        self.fill_power_left = pg.FillBetweenItem(left_curv, left_zero, brush = "#FFFD1B")
        self.graph.addItem(self.fill_power_left)

        # fill the power area for right tail
        right_x_low = norm.ppf(1 - (float(self.type_i_error.text()) / 2), loc = h0mu, scale = 1)
        right_x_high = np.max(xa)
        x_right = np.linspace(right_x_low, right_x_high, 300)
        y_right = norm.pdf(x_right, loc = hamu, scale = 1)
        right_curv = pg.PlotCurveItem(x = x_right, y = y_right)
        right_zero = pg.PlotCurveItem(x = x_right, y = np.zeros(len(x_right)))
        self.fill_power_right = pg.FillBetweenItem(right_curv, right_zero, brush = "#FFFD1B")
        self.graph.addItem(self.fill_power_right)
# ----------------------------------------------------------

# calculate the value of power and type II error and then fill them into lineedit
    def power_typeiierror_calculate(self):
        x_left = norm.ppf((float(self.type_i_error.text()) / 2), loc = h0mu, scale = 1) 
        x_right = norm.ppf(1 - (float(self.type_i_error.text()) / 2), loc = h0mu, scale = 1) 
        type_ii_error = norm.cdf(x_right, loc = hamu, scale = 1) - norm.cdf(x_left, loc = hamu, scale = 1)
        power = 1 - type_ii_error
        self.type_ii_error.setText(str(round(type_ii_error, 3)))
        self.power.setText(str(round(power, 3)))
# ----------------------------------------------------------

# function for removing the power item--------------------
    def remove_power(self):
        self.graph.removeItem(self.fill_power_left)
        self.graph.removeItem(self.fill_power_right)
# ----------------------------------------------------------


# function for determine the state of checkbox of power----
    def _state_power(self, s):
        if s == 2:
            self.draw_power()
        else:
            self.remove_power()
# ----------------------------------------------------------


# create pop up window for leaving-------------------------
    def _leaving(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Alarm")
        dlg.setText("Are you sure you want to leave ?")
        dlg.setIcon(QMessageBox.Icon.Warning)
        dlg.setStyleSheet("background-color: white")
        dlg.addButton("Cancel", QtWidgets.QMessageBox.NoRole)
        dlg.addButton("Yes", QtWidgets.QMessageBox.NoRole)
        q = dlg.exec_()
        if q == 0:
            dlg.done(1)
        else:
            self.close()
# ----------------------------------------------------------
        
# create pop up window when the user does not enter the parameter 
# correctly
    def exception_dialog_value_error(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Alarm")
        dlg.setText("The parameter should be numerical")
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.setStyleSheet("background-color: white")
        dlg.addButton("OK", QtWidgets.QMessageBox.NoRole)
        q = dlg.exec_()
        if q == 0:
            dlg.done(1)
# ----------------------------------------------------------

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = mymainform()
    ui.show()
    sys.exit(app.exec())