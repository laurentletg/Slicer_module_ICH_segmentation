# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/laurentletourneau-guillon/Dropbox (Personal)/CHUM/RECHERCHE/2020ICHHEMATOMAS/2022 SLICER GUI/ICH_segmenter_predictions_2022_08/ICH_SEGMENTER_2022_08/Resources/UI/ICH_SEGMENTER_2022_08.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(553, 898)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.CollapsibleGroupBox = ctkCollapsibleGroupBox(Form)
        self.CollapsibleGroupBox.setObjectName("CollapsibleGroupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.CollapsibleGroupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.CollapsibleGroupBox)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.getDefaultDir = QtWidgets.QPushButton(self.CollapsibleGroupBox)
        self.getDefaultDir.setObjectName("getDefaultDir")
        self.verticalLayout.addWidget(self.getDefaultDir)
        self.BrowseFolders = QtWidgets.QPushButton(self.CollapsibleGroupBox)
        self.BrowseFolders.setObjectName("BrowseFolders")
        self.verticalLayout.addWidget(self.BrowseFolders)
        self.CurrentFolder = QtWidgets.QLabel(self.CollapsibleGroupBox)
        self.CurrentFolder.setObjectName("CurrentFolder")
        self.verticalLayout.addWidget(self.CurrentFolder)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.CollapsibleGroupBox)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.Annotator_name = QtWidgets.QLineEdit(self.CollapsibleGroupBox)
        self.Annotator_name.setObjectName("Annotator_name")
        self.verticalLayout_2.addWidget(self.Annotator_name)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.CollapsibleGroupBox)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.AnnotatorDegree = QtWidgets.QComboBox(self.CollapsibleGroupBox)
        self.AnnotatorDegree.setObjectName("AnnotatorDegree")
        self.AnnotatorDegree.addItem("")
        self.AnnotatorDegree.setItemText(0, "")
        self.AnnotatorDegree.addItem("")
        self.AnnotatorDegree.addItem("")
        self.AnnotatorDegree.addItem("")
        self.AnnotatorDegree.addItem("")
        self.AnnotatorDegree.addItem("")
        self.verticalLayout_3.addWidget(self.AnnotatorDegree)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.CollapsibleGroupBox)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.RevisionStep = QtWidgets.QComboBox(self.CollapsibleGroupBox)
        self.RevisionStep.setObjectName("RevisionStep")
        self.RevisionStep.addItem("")
        self.RevisionStep.setItemText(0, "")
        self.RevisionStep.addItem("")
        self.RevisionStep.addItem("")
        self.RevisionStep.addItem("")
        self.verticalLayout_4.addWidget(self.RevisionStep)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Previous = QtWidgets.QPushButton(self.CollapsibleGroupBox)
        self.Previous.setObjectName("Previous")
        self.horizontalLayout_2.addWidget(self.Previous)
        self.Next = QtWidgets.QPushButton(self.CollapsibleGroupBox)
        self.Next.setObjectName("Next")
        self.horizontalLayout_2.addWidget(self.Next)
        self.FileIndex = QtWidgets.QLabel(self.CollapsibleGroupBox)
        self.FileIndex.setText("")
        self.FileIndex.setObjectName("FileIndex")
        self.horizontalLayout_2.addWidget(self.FileIndex)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.CurrentPatient = QtWidgets.QLabel(self.CollapsibleGroupBox)
        self.CurrentPatient.setObjectName("CurrentPatient")
        self.verticalLayout.addWidget(self.CurrentPatient)
        self.CurrentSegmenationLabel = QtWidgets.QLabel(self.CollapsibleGroupBox)
        self.CurrentSegmenationLabel.setObjectName("CurrentSegmenationLabel")
        self.verticalLayout.addWidget(self.CurrentSegmenationLabel)
        self.BrowseFolders_2 = QtWidgets.QPushButton(self.CollapsibleGroupBox)
        self.BrowseFolders_2.setObjectName("BrowseFolders_2")
        self.verticalLayout.addWidget(self.BrowseFolders_2)
        self.gridLayout_4.addLayout(self.verticalLayout, 0, 0, 1, 2)
        self.SaveSegmentationButton = QtWidgets.QPushButton(self.CollapsibleGroupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.SaveSegmentationButton.setFont(font)
        self.SaveSegmentationButton.setObjectName("SaveSegmentationButton")
        self.gridLayout_4.addWidget(self.SaveSegmentationButton, 7, 1, 1, 1)
        self.pushButton_15 = QtWidgets.QPushButton(self.CollapsibleGroupBox)
        self.pushButton_15.setObjectName("pushButton_15")
        self.gridLayout_4.addWidget(self.pushButton_15, 5, 1, 1, 1)
        self.MRMLCollapsibleButton = qMRMLCollapsibleButton(self.CollapsibleGroupBox)
        self.MRMLCollapsibleButton.setObjectName("MRMLCollapsibleButton")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.MRMLCollapsibleButton)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.radioButton_5 = QtWidgets.QRadioButton(self.MRMLCollapsibleButton)
        self.radioButton_5.setObjectName("radioButton_5")
        self.gridLayout_2.addWidget(self.radioButton_5, 0, 1, 1, 1)
        self.radioButton_6 = QtWidgets.QRadioButton(self.MRMLCollapsibleButton)
        self.radioButton_6.setObjectName("radioButton_6")
        self.gridLayout_2.addWidget(self.radioButton_6, 0, 4, 1, 1)
        self.radioButton_3 = QtWidgets.QRadioButton(self.MRMLCollapsibleButton)
        self.radioButton_3.setObjectName("radioButton_3")
        self.gridLayout_2.addWidget(self.radioButton_3, 0, 2, 1, 1)
        self.radioButton_4 = QtWidgets.QRadioButton(self.MRMLCollapsibleButton)
        self.radioButton_4.setObjectName("radioButton_4")
        self.gridLayout_2.addWidget(self.radioButton_4, 0, 0, 1, 1)
        self.radioButton_2 = QtWidgets.QRadioButton(self.MRMLCollapsibleButton)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout_2.addWidget(self.radioButton_2, 0, 3, 1, 1)
        self.radioButton_Edema = QtWidgets.QRadioButton(self.MRMLCollapsibleButton)
        self.radioButton_Edema.setCheckable(True)
        self.radioButton_Edema.setChecked(False)
        self.radioButton_Edema.setAutoExclusive(False)
        self.radioButton_Edema.setObjectName("radioButton_Edema")
        self.gridLayout_2.addWidget(self.radioButton_Edema, 0, 5, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.MRMLCollapsibleButton, 10, 0, 1, 2)
        self.pushButton_14 = QtWidgets.QPushButton(self.CollapsibleGroupBox)
        self.pushButton_14.setObjectName("pushButton_14")
        self.gridLayout_4.addWidget(self.pushButton_14, 4, 1, 1, 1)
        self.NewICHSegm = QtWidgets.QPushButton(self.CollapsibleGroupBox)
        self.NewICHSegm.setObjectName("NewICHSegm")
        self.gridLayout_4.addWidget(self.NewICHSegm, 2, 1, 1, 1)
        self.LoadPrediction = QtWidgets.QPushButton(self.CollapsibleGroupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.LoadPrediction.setFont(font)
        self.LoadPrediction.setObjectName("LoadPrediction")
        self.gridLayout_4.addWidget(self.LoadPrediction, 1, 1, 1, 1)
        self.MRMLCollapsibleButton_2 = qMRMLCollapsibleButton(self.CollapsibleGroupBox)
        self.MRMLCollapsibleButton_2.setObjectName("MRMLCollapsibleButton_2")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.MRMLCollapsibleButton_2)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_Paint = QtWidgets.QPushButton(self.MRMLCollapsibleButton_2)
        self.pushButton_Paint.setCheckable(True)
        self.pushButton_Paint.setChecked(True)
        self.pushButton_Paint.setObjectName("pushButton_Paint")
        self.gridLayout.addWidget(self.pushButton_Paint, 1, 0, 1, 1)
        self.pushButton_Smooth = QtWidgets.QPushButton(self.MRMLCollapsibleButton_2)
        self.pushButton_Smooth.setObjectName("pushButton_Smooth")
        self.gridLayout.addWidget(self.pushButton_Smooth, 3, 2, 1, 1)
        self.pushButton_ToggleFill = QtWidgets.QPushButton(self.MRMLCollapsibleButton_2)
        self.pushButton_ToggleFill.setCheckable(True)
        self.pushButton_ToggleFill.setObjectName("pushButton_ToggleFill")
        self.gridLayout.addWidget(self.pushButton_ToggleFill, 2, 2, 1, 1)
        self.pushButton_Small_holes = QtWidgets.QPushButton(self.MRMLCollapsibleButton_2)
        self.pushButton_Small_holes.setObjectName("pushButton_Small_holes")
        self.gridLayout.addWidget(self.pushButton_Small_holes, 3, 1, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.MRMLCollapsibleButton_2)
        self.spinBox.setToolTip("")
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 2, 0, 1, 1)
        self.spinBox_2 = QtWidgets.QSpinBox(self.MRMLCollapsibleButton_2)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridLayout.addWidget(self.spinBox_2, 2, 1, 1, 1)
        self.pushButton_Erase = QtWidgets.QPushButton(self.MRMLCollapsibleButton_2)
        self.pushButton_Erase.setObjectName("pushButton_Erase")
        self.gridLayout.addWidget(self.pushButton_Erase, 1, 2, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.MRMLCollapsibleButton_2)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 1, 1, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.SegmentWindowPushButton = QtWidgets.QPushButton(self.MRMLCollapsibleButton_2)
        self.SegmentWindowPushButton.setCheckable(True)
        self.SegmentWindowPushButton.setObjectName("SegmentWindowPushButton")
        self.gridLayout_6.addWidget(self.SegmentWindowPushButton, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.MRMLCollapsibleButton_2, 11, 0, 1, 2)
        self.lcdNumber = QtWidgets.QLCDNumber(self.CollapsibleGroupBox)
        self.lcdNumber.setObjectName("lcdNumber")
        self.gridLayout_4.addWidget(self.lcdNumber, 8, 1, 1, 1)
        self.pushButton_13 = QtWidgets.QPushButton(self.CollapsibleGroupBox)
        self.pushButton_13.setObjectName("pushButton_13")
        self.gridLayout_4.addWidget(self.pushButton_13, 6, 1, 1, 1)
        self.pushButton_12 = QtWidgets.QPushButton(self.CollapsibleGroupBox)
        self.pushButton_12.setObjectName("pushButton_12")
        self.gridLayout_4.addWidget(self.pushButton_12, 3, 1, 1, 1)
        self.PauseTimerButton = QtWidgets.QPushButton(self.CollapsibleGroupBox)
        self.PauseTimerButton.setCheckable(True)
        self.PauseTimerButton.setObjectName("PauseTimerButton")
        self.gridLayout_4.addWidget(self.PauseTimerButton, 9, 1, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.CollapsibleGroupBox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 385, 339))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.SlicerDirectoryListView = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.SlicerDirectoryListView.setGeometry(QtCore.QRect(0, 0, 301, 201))
        self.SlicerDirectoryListView.setSelectionRectVisible(False)
        self.SlicerDirectoryListView.setObjectName("SlicerDirectoryListView")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_4.addWidget(self.scrollArea, 1, 0, 9, 1)
        self.gridLayout_3.addWidget(self.CollapsibleGroupBox, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.CollapsibleGroupBox.setTitle(_translate("Form", "Configuration"))
        self.label_3.setText(_translate("Form", "Set default directory"))
        self.getDefaultDir.setText(_translate("Form", "Get default directory"))
        self.BrowseFolders.setText(_translate("Form", "Browse volume folder"))
        self.CurrentFolder.setText(_translate("Form", "Current Folder:"))
        self.label_2.setText(_translate("Form", "Annotator\'s name"))
        self.label_4.setText(_translate("Form", "Degree"))
        self.AnnotatorDegree.setItemText(1, _translate("Form", "Medical Student"))
        self.AnnotatorDegree.setItemText(2, _translate("Form", "Resident"))
        self.AnnotatorDegree.setItemText(3, _translate("Form", "Radiologist"))
        self.AnnotatorDegree.setItemText(4, _translate("Form", "Supervisor"))
        self.AnnotatorDegree.setItemText(5, _translate("Form", "Research Team"))
        self.label_5.setText(_translate("Form", "Revision step"))
        self.RevisionStep.setItemText(1, _translate("Form", "0 - First"))
        self.RevisionStep.setItemText(2, _translate("Form", "1 - Revision"))
        self.RevisionStep.setItemText(3, _translate("Form", "2 - Final"))
        self.Previous.setText(_translate("Form", "<<  Previous"))
        self.Next.setText(_translate("Form", "Next  >>"))
        self.CurrentPatient.setText(_translate("Form", "Current Patient:"))
        self.CurrentSegmenationLabel.setText(_translate("Form", "Current Segmentation Label:"))
        self.BrowseFolders_2.setText(_translate("Form", "Browse prediction folder"))
        self.SaveSegmentationButton.setStatusTip(_translate("Form", "Saving segmentation"))
        self.SaveSegmentationButton.setText(_translate("Form", "Save segmentation"))
        self.SaveSegmentationButton.setShortcut(_translate("Form", "Ctrl+S"))
        self.pushButton_15.setText(_translate("Form", "New SDH segm"))
        self.MRMLCollapsibleButton.setText(_translate("Form", "Hemorrhage"))
        self.radioButton_5.setText(_translate("Form", "IVH"))
        self.radioButton_6.setText(_translate("Form", "EDH"))
        self.radioButton_3.setText(_translate("Form", "SAH"))
        self.radioButton_4.setText(_translate("Form", "ICH"))
        self.radioButton_2.setText(_translate("Form", "SDH"))
        self.radioButton_Edema.setText(_translate("Form", "Edema"))
        self.pushButton_14.setText(_translate("Form", "New SAH segm"))
        self.NewICHSegm.setText(_translate("Form", "New ICH segm"))
        self.LoadPrediction.setStatusTip(_translate("Form", "Timer started"))
        self.LoadPrediction.setText(_translate("Form", "Load prediction"))
        self.MRMLCollapsibleButton_2.setText(_translate("Form", "Tools"))
        self.pushButton_Paint.setText(_translate("Form", "Paint with mask"))
        self.pushButton_Smooth.setText(_translate("Form", "Smooth margins"))
        self.pushButton_ToggleFill.setText(_translate("Form", "Fill OFF"))
        self.pushButton_Small_holes.setText(_translate("Form", "Remove small holes"))
        self.pushButton_Erase.setText(_translate("Form", "Erase mode"))
        self.pushButton_4.setText(_translate("Form", "Paint without mask"))
        self.SegmentWindowPushButton.setText(_translate("Form", "Dock Segment Editor"))
        self.pushButton_13.setText(_translate("Form", "New EDH segm"))
        self.pushButton_12.setText(_translate("Form", "New IVH segm"))
        self.PauseTimerButton.setText(_translate("Form", "Pause"))

from ctkCollapsibleGroupBox import ctkCollapsibleGroupBox
from qMRMLCollapsibleButton import qMRMLCollapsibleButton
from qMRMLWidget import qMRMLWidget
