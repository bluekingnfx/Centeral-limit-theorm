from PyQt6.QtWidgets import QMainWindow,QApplication,QWidget,QVBoxLayout,QRadioButton,QHBoxLayout,QGroupBox,QFormLayout,QLabel,QLineEdit,QScrollArea
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon


from pathlib import Path as pa
import sys as sy
import typing as ty
import math
from random import randint
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,NavigationToolbar2QT as NavigationToolBar
from matplotlib.figure import Figure


from HelperMethods import HelperMethods as HM

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class CentralLimitTheorem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initWin()
    
    def initWin(self):
        self.selfAttachments()
        self.initMainWin()
        scrollWidget = QScrollArea(self)
        widget = QWidget()
        mainVLay = QVBoxLayout()
        scrollWidget.setWidgetResizable(True)
        self.SuppressSurface(mainVLay)
        widget.setLayout(mainVLay)
        scrollWidget.setWidget(widget)
        self.setCentralWidget(scrollWidget)
        self.show()

    def selfAttachments(self):
        
        self.rootFolder = str(pa(__file__).parent).replace("\\","/")

    def initMainWin(self):
        self.setWindowTitle("Central Limit theorem.")
        self.setMinimumSize(QSize(500,600))
        self.setWindowIcon(QIcon(self.rootFolder + "/data/icon.png"))

    
    def SuppressSurface(self,mainVLay:QVBoxLayout):
        widget = QWidget()
        VLy = QVBoxLayout()
        groupBox = QGroupBox("Repeated rolls for single sampling of a die.")
        hLayGroup = QHBoxLayout()
        RadioButs:ty.List[QRadioButton] = [ HM.ProduceRadioButs(str(i)) for i in [5,10,20,30,40,50]]
        for RadioBut in RadioButs:
            hLayGroup.addWidget(RadioBut)
        groupBox.setLayout(hLayGroup)
        formWidget = QWidget()
        formLayout = QFormLayout()
        label = QLabel("No: of samples")
        edit = QLineEdit()
        edit.setPlaceholderText("Enter a number, i.e) 100.")
        formLayout.addRow(label,edit)
        formWidget.setLayout(formLayout)
        VLy.addWidget(groupBox)
        VLy.addWidget(formWidget)
        invokeDialogueBut = HM.ProducePushBut("Process",self.InvokeDialogue,40,[RadioButs,edit,mainVLay],None,"font-size:16px")
        VLy.addWidget(invokeDialogueBut)
        widget.setLayout(VLy)
        mainVLay.addWidget(widget)


    def InvokeDialogue(self,but,RadioButs:ty.List[QRadioButton],edit:QLineEdit,mainVLay:QVBoxLayout):
        value = 0
        for i in RadioButs:
            if i.isChecked() == True:
                value = int(i.text())

        try:
            if value == 0: raise Exception("No Repeated rolls for single sampling is been selected.")
            turns = int(edit.text())
            if turns <= 0: 
                raise Exception("Turns is zero")
            text = f"You have selected {value} rolls per sample. Click OK to continue."
            HM.ProduceMessageBox(self,"question","Confirm?",text,self.Solution,None,[value,turns,mainVLay])
        except Exception as e:
            if str(e) == "No Repeated rolls for single sampling is been selected.":
                HM.ProduceMessageBox(self,"about","Error",str(e))
            else:
                HM.ProduceMessageBox(self,"about","Error",f"The sample count must be a number greater than 0. Given {edit.text()}. Please give a valid number.")
        

    def Solution(self,value:int,turns:int,mainVLay:QVBoxLayout):
        samplesAr = []
        for i in range(1,turns+1):
            sample = []
            for j in range(1,value+1):
                ranValue = randint(1,6)
                sample = [*sample,ranValue]
            samplesAr = [*samplesAr,(i,sample)]
        self.ProduceMap(samplesAr,value,turns,mainVLay)

    def ProduceMap(self,samplesAr:ty.List[ty.Tuple[int,ty.List[int]]],value:int,turns:int,mainVLay:QVBoxLayout):
        avgOfSamples = []
        for sample in samplesAr:
            AvgOfEachSample = sum(sample[1])/len(sample[1])
            avgOfSamples = [*avgOfSamples,(sample[0],AvgOfEachSample)]


        PopulationMeanOFDie = sum([1,2,3,4,5,6])/6
        STDofPopulation = HM.CalculateStandardDeviation([1,2,3,4,5,6],True)
        avgOfSamples = [i[1] for i in avgOfSamples]
        MeanOfAvgOfSamples = sum(avgOfSamples)/len(avgOfSamples)
        StdOfSamples = HM.CalculateStandardDeviation(avgOfSamples,False)
        sqOfTurns = math.sqrt(value)
        StDofMeanPopulationForNTurns = (STDofPopulation/sqOfTurns)

        widget = QWidget()
        widget.setMinimumHeight(400)
        VLay = QVBoxLayout()
        groupBox = QGroupBox("The Info about the graph")
        vLay = QVBoxLayout()
        label1 = QLabel(f"The Population mean of the dice {PopulationMeanOFDie}.")
        label1.setWordWrap(True)
        label2 = QLabel(f"The Standard deviation of a die {STDofPopulation}.")
        label3 = QLabel(f"Mean of sample average {MeanOfAvgOfSamples}")
        label4 = QLabel(f"Standard Deviation of average of Samples {StdOfSamples}")
        label5 = QLabel(f"Standard Deviation for Mean population of given {value} is {StDofMeanPopulationForNTurns}")

        label6 = QLabel(f"Theorem holds good, if Standard Deviation for Mean population of given {value} = Value1: {StDofMeanPopulationForNTurns} is approximately equals to Standard Deviation of average of Samples = Value2: {StdOfSamples}. Compare Value1, Value2")

        label2.setWordWrap(True)
        label3.setWordWrap(True)
        label4.setWordWrap(True)
        label5.setWordWrap(True)
        label6.setWordWrap(True)

        vLay.addWidget(label1)
        vLay.addWidget(label2)
        vLay.addWidget(label3)
        vLay.addWidget(label4)
        vLay.addWidget(label5)
        vLay.addWidget(label6)
        groupBox.setLayout(vLay)



        
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.hist(avgOfSamples)
        
        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolBar(sc, self)
        VLay.addWidget(toolbar)
        VLay.addWidget(sc)
        VLay.addWidget(groupBox)
        widget.setLayout(VLay)
        
        mainVLay.addWidget(widget)

        


if not QApplication.instance():
    app = QApplication(sy.argv)
else:
    app = QApplication.instance()

CentralLimitTheorem1 = CentralLimitTheorem()
sy.exit(app.exec())