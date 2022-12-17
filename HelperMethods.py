
import typing as ty
import math

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QRadioButton,QMessageBox

class HelperMethods():
    @classmethod
    def ProducePushBut(cls,butText:str,connectFunc:ty.Callable[[],None],height=30,argsConnectFunc = [],self = None,styles="") -> QPushButton:
        if self !=None: but = QPushButton(butText,self)
        else: but = QPushButton(butText)
        but.setStyleSheet(styles)
        but.clicked.connect(lambda: connectFunc(but,*argsConnectFunc))
        but.setMinimumHeight(height)
        return but

    @classmethod
    def ProduceRadioButs(cls,rText,changeOnClick:ty.Union[ty.Callable[[],None],None] = None, args = []):
        checkbox = QRadioButton(rText)
        if changeOnClick != None:
            checkbox.toggled.connect(lambda:changeOnClick(*args))
        return checkbox

    @classmethod
    def ProduceMessageBox(cls,self,boxType:ty.Literal["about","question"],title:str,des:str,okButFunc:ty.Union[ty.Callable[[],None],None] = None,cancel:ty.Union[ty.Callable[[],None],None] = None,OkArgs:ty.List=[],cancelArgs:ty.List = [],sendMessageBox:bool = False) -> QMessageBox:
        if boxType == "about":
            if okButFunc != None:
                okButFunc(*OkArgs)
            QMessageBox.about(self,title,des)
        else:
            question = QMessageBox.question(self,title,des,QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel) 
            if question == QMessageBox.StandardButton.Ok:
                if sendMessageBox == False: okButFunc(*OkArgs)
                else: okButFunc(*OkArgs,question)
            else:
                if cancel != None: cancel(*cancelArgs)
                #QMessageBox.close(self)
    
    @classmethod
    def CalculateStandardDeviation(cls,arr:ty.List[int],population:bool = False) -> float:
        """
            s = sqrt(sum(a))
            a[i] = ((Loop of sample[i] - avg of sample))^2
        """

        avg = sum(arr)/len(arr)
        SqXElemMinusXAvg = []
        for i in arr:
            elem = (abs(i-avg))**2
            SqXElemMinusXAvg = [*SqXElemMinusXAvg,elem]
        

        sumOfNumerator = sum(SqXElemMinusXAvg)

        if population == False:
            N = len(arr) - 1
        else:
            N = len(arr)
        
        STD = math.sqrt((sumOfNumerator/N))
        return STD


