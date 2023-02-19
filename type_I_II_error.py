from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QDoubleValidator
from matplotlib.pyplot import draw
from scipy.stats import norm
import pyqtgraph as pg
import numpy as np
import sys



class mymainform(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(mymainform, self).__init__(*args, **kwargs)
        uic.loadUi("type_i_ii_error.ui", self)

        self.h0mu.setText("0")
        self.hamu.setText("0.5")
        self.type_i_error.setText("0.05")

        
        self.update_plot()

        self.graph.setBackground("#2B3B84")
        self.graph.setEnabled(False)
        self.h0mu.setValidator(QDoubleValidator())
        self.hamu.setValidator(QDoubleValidator())
        self.type_i_error.setValidator(QDoubleValidator())

        self.show_type_i.stateChanged.connect(self._show_type_i)
        self.show_type_ii.stateChanged.connect(self._show_type_ii)
        self.show_power.stateChanged.connect(self._show_power)
        self.h0mu.returnPressed.connect(self.update_plot)
        self.hamu.returnPressed.connect(self.update_plot)
        self.type_i_error.returnPressed.connect(self.update_plot)

    

    def update_plot(self):
        # return to default setting--------------------------
        self.graph.clear()
        
        self.show_type_i.setChecked(True)
        self.show_type_ii.setChecked(True)

        self.h0mu_val = float(self.h0mu.text())
        self.hamu_val = float(self.hamu.text())
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
        
        x0 = np.linspace(self.h0mu_val - 6.5, self.h0mu_val + 6.5, 1000)
        y0 = norm.pdf(x0, loc = self.h0mu_val, scale = 1)

        xa = np.linspace(self.hamu_val - 6.5, self.hamu_val + 6.5, 1000)
        ya = norm.pdf(xa, loc = self.hamu_val, scale = 1)

        self.graph.addLegend(pen = lgpen)
        self.graph.plot(x0, y0, pen = penh0,  name = "<p style = 'font-size: 14pt; color: #B5FFA3; font-weight: bold'>Null Hypothesis</p>")
        self.graph.plot(xa, ya, pen = penha, name = "<p style = 'font-size: 14pt; color: #B5FFA3; font-weight: bold'>True Parameter</p>")

        self._show_type_i(2)
        self._show_type_ii(2)
        self._add_text()


    def _add_text(self):
        self.explain_text = "The graph illustrates the process of a two-tailed test of testing value of μ. \n\n"
        self.explain_text += f"The null hypothesis (H0) is μ = {self.h0mu_val} and the alternative hypothesis (Ha) is μ ≠ {self.h0mu_val} \n\n"
        self.explain_text += f"Now suppose we randomly sample from the population of a normal distribution with μ = {self.hamu_val} and σ = 1 \n\n"
        self.explain_text += f"When we set the significance level to {self.type_i_error.text()}, "
        self.explain_text += f"the value of type II error will be {self.type_ii_error_val} "
        self.explain_text += f"The power of the test is {self.power_val}  \n\n"
        self.explain_text += f"That is, when drawing multiple samples from the population of μ = {self.hamu_val} and σ = 1, we would have probability of {self.type_ii_error.text()} to falsely fail to reject the null hypothesis when the value of μ is {self.hamu_val} rather than {self.h0mu_val} \n\n"
        self.explain_text += f"In addition, we would have probability of {self.power_val} to correctly reject the null hypothesis."
        self.explain_text_edit.setText(self.explain_text)



    def draw_type_i_error(self):
            # fill the area of type I error at the left tail-----------------------
            left_x_low = np.min(x0)
            left_x_high = norm.ppf(float(self.type_i_error.text()) / 2, loc = self.h0mu_val, scale = 1)
            x_left = np.linspace(left_x_low, left_x_high, 300)
            y_left = norm.pdf(x_left, loc = self.h0mu_val, scale = 1)
            left_curv = pg.PlotCurveItem(x = x_left, y = y_left)
            left_zero = pg.PlotCurveItem(x = x_left, y = np.zeros(len(x_left)))
            self.fill_1 = pg.FillBetweenItem(left_curv, left_zero, brush = "g")
            self.graph.addItem(self.fill_1)
            # ---------------------------------------------------------------------

            # fill the area of type I error at the right tail
            righ_x_low = norm.ppf(1 - (float(self.type_i_error.text()) / 2), loc = self.h0mu_val, scale = 1)
            right_x_high = np.max(x0)
            x_right = np.linspace(righ_x_low, right_x_high, 300)
            y_right = norm.pdf(x_right, loc = self.h0mu_val, scale = 1)
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
        left = norm.ppf(float(self.type_i_error.text()) / 2, loc = self.h0mu_val, scale = 1)
        right = norm.ppf(1 - (float(self.type_i_error.text()) / 2), loc = self.h0mu_val, scale = 1)
        x = np.linspace(left, right, 300)
        y = norm.pdf(x, loc = self.hamu_val, scale = 1)
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
        left_x_high = norm.ppf((float(self.type_i_error.text()) / 2), loc = self.h0mu_val, scale = 1) 
        x_left = np.linspace(left_x_low, left_x_high, 300)
        y_left = norm.pdf(x_left, loc = self.hamu_val, scale = 1)
        left_curv = pg.PlotCurveItem(x = x_left, y = y_left)
        left_zero = pg.PlotCurveItem(x = x_left, y = np.zeros(len(x_left)))
        self.fill_power_left = pg.FillBetweenItem(left_curv, left_zero, brush = "#FFFD1B")
        self.graph.addItem(self.fill_power_left)

        # fill the power area for right tail
        right_x_low = norm.ppf(1 - (float(self.type_i_error.text()) / 2), loc = self.h0mu_val, scale = 1)
        right_x_high = np.max(xa)
        x_right = np.linspace(right_x_low, right_x_high, 300)
        y_right = norm.pdf(x_right, loc = self.hamu_val, scale = 1)
        right_curv = pg.PlotCurveItem(x = x_right, y = y_right)
        right_zero = pg.PlotCurveItem(x = x_right, y = np.zeros(len(x_right)))
        self.fill_power_right = pg.FillBetweenItem(right_curv, right_zero, brush = "#FFFD1B")
        self.graph.addItem(self.fill_power_right)
# ----------------------------------------------------------

# calculate the value of power and type II error and then fill them into lineedit
    def power_typeiierror_calculate(self):
        x_left = norm.ppf((float(self.type_i_error.text()) / 2), loc = self.h0mu_val, scale = 1) 
        x_right = norm.ppf(1 - (float(self.type_i_error.text()) / 2), loc = self.h0mu_val, scale = 1) 
        self.type_ii_error_val = round(norm.cdf(x_right, loc = self.hamu_val, scale = 1) - norm.cdf(x_left, loc = self.hamu_val, scale = 1), 3)
        self.power_val = round(1 - self.type_ii_error_val, 3)
        self.type_ii_error.setText(str(self.type_ii_error_val))
        self.power.setText(str(self.power_val))
# ----------------------------------------------------------

# function for removing the power item--------------------
    def remove_power(self):
        self.graph.removeItem(self.fill_power_left)
        self.graph.removeItem(self.fill_power_right)
# ----------------------------------------------------------


# function for determine the state of checkbox of power----
    def _show_power(self, s):
        if s == 2:
            self.draw_power()
        else:
            self.remove_power()
# ----------------------------------------------------------



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = mymainform()
    ui.show()
    sys.exit(app.exec())