from genericpath import exists
import os
from ssl import _create_unverified_context
import unittest
import logging
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
from slicer.util import getNode
from glob import glob
import re
import time
import pandas as pd
from datetime import datetime



VOLUME_FILE_TYPE = '*.nrrd' 
SEGM_FILE_TYPE = '*.seg.nrrd'

#
# ICH_SEGMENTER_2022_08
#

class ICH_SEGMENTER_2022_08(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "ICH_SEGMENTER_2022_08"  # TODO: make this more human readable by adding spaces
    self.parent.categories = ["Examples"]  # TODO: set categories (folders where the module shows up in the module selector)
    self.parent.dependencies = []  # TODO: add here list of module names that this module requires
    self.parent.contributors = ["John Doe (AnyWare Corp.)"]  # TODO: replace with "Firstname Lastname (Organization)"
    # TODO: update with short description of the module and a link to online module documentation
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#ICH_SEGMENTER_2022_08">module documentation</a>.
"""
    # TODO: replace with organization, grant and thanks
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
"""

    # Additional initialization step after application startup is complete
    # slicer.app.connect("startupCompleted()", registerSampleData)


#
# Register sample data sets in Sample Data module
#

# def registerSampleData():
  # """
  # Add data sets to Sample Data module.
  # """
  # # It is always recommended to provide sample data for users to make it easy to try the module,
  # # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

  # import SampleData
  # iconsPath = os.path.join(os.path.dirname(__file__), 'Resources/Icons')

  # # To ensure that the source code repository remains small (can be downloaded and installed quickly)
  # # it is recommended to store data sets that are larger than a few MB in a Github release.

  # # ICH_SEGMENTER_2022_081
  # SampleData.SampleDataLogic.registerCustomSampleDataSource(
  #   # Category and sample name displayed in Sample Data module
  #   category='ICH_SEGMENTER_2022_08',
  #   sampleName='ICH_SEGMENTER_2022_081',
  #   # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
  #   # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
  #   thumbnailFileName=os.path.join(iconsPath, 'ICH_SEGMENTER_2022_081.png'),
  #   # Download URL and target file name
  #   uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
  #   fileNames='ICH_SEGMENTER_2022_081.nrrd',
  #   # Checksum to ensure file integrity. Can be computed by this command:
  #   #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
  #   checksums = 'SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95',
  #   # This node name will be used when the data set is loaded
  #   nodeNames='ICH_SEGMENTER_2022_081'
  # )

  # # ICH_SEGMENTER_2022_082
  # SampleData.SampleDataLogic.registerCustomSampleDataSource(
  #   # Category and sample name displayed in Sample Data module
  #   category='ICH_SEGMENTER_2022_08',
  #   sampleName='ICH_SEGMENTER_2022_082',
  #   thumbnailFileName=os.path.join(iconsPath, 'ICH_SEGMENTER_2022_082.png'),
  #   # Download URL and target file name
  #   uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
  #   fileNames='ICH_SEGMENTER_2022_082.nrrd',
  #   checksums = 'SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97',
  #   # This node name will be used when the data set is loaded
  #   nodeNames='ICH_SEGMENTER_2022_082'
  # )


#
# ICH_SEGMENTER_2022_08Widget
#

class ICH_SEGMENTER_2022_08Widget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent=None):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.__init__(self, parent)
    VTKObservationMixin.__init__(self)  # needed for parameter node observation
    self.logic = None
    self._parameterNode = None
    self._updatingGUIFromParameterNode = False
    self.ICH_segm_name = None
    
    # LLG CODE BELOW
    self.ICH_segm_name = None
    self.predictions_names= None
    self.DefaultDir = None

    # ----- ANW Addition  ----- : Initialize called var to False so the timer only stops once
    self.called = False
    self.called_onLoadPrediction = False
    # self.editor = None


  def setup(self):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.setup(self)

    # Load widget from .ui file (created by Qt Designer).
    # Additional widgets can be instantiated manually and added to self.layout.
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/ICH_SEGMENTER_2022_08.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
    # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
    # "setMRMLScene(vtkMRMLScene*)" slot.
    uiWidget.setMRMLScene(slicer.mrmlScene)

    # Create logic class. Logic implements all computations that should be possible to run
    # in batch mode, without a graphical user interface.
    self.logic = ICH_SEGMENTER_2022_08Logic()


    # Buttons
    ### LLG CONNECTIONS
    self.ui.getDefaultDir.connect('clicked(bool)', self.getDefaultDir)
    self.ui.BrowseFolders.connect('clicked(bool)', self.onBrowseFoldersButton)
    self.ui.NewICHSegm.connect('clicked(bool)', self.onNewICHSegm)
    self.ui.SaveSegmentationButton.connect('clicked(bool)', self.onSaveSegmentationButton)
    self.ui.BrowseFolders_2.connect('clicked(bool)', self.onBrowseFolders_2Button)
    self.ui.LoadPrediction.connect('clicked(bool)', self.onLoadPredictionButton)
    self.ui.Previous.connect('clicked(bool)', self.onPreviousButton)
    self.ui.Next.connect('clicked(bool)', self.onNextButton)
    self.ui.pushButton_1.connect('clicked(bool)', self.onPushButton_1)
    self.ui.pushButton_2.connect('clicked(bool)', self.onPushButton_2)
    self.ui.pushButton_3.connect('clicked(bool)', self.onPushButton_3)  
    self.ui.pushButton_4.connect('clicked(bool)', self.onPushButton_4)  
    self.ui.pushButton_5.connect('clicked(bool)', self.onPushButton_5)  
    self.ui.pushButton_6.connect('clicked(bool)', self.onPushButton_6)  
    self.ui.pushButton_7.connect('clicked(bool)', self.onPushButton_7)  
    self.ui.pushButton_8.connect('clicked(bool)', self.onPushButton_8)  
    self.ui.pushButton_9.connect('clicked(bool)', self.onPushButton_9)  
    self.ui.pushButton_10.connect('clicked(bool)', self.onPushButton_10)  
    self.ui.pushButton_11.connect('clicked(bool)', self.onPushButton_11)

    ### ANW CONNECTIONS
    self.ui.PauseTimerButton.connect('clicked(bool)', self.togglePauseTimerButton)
    self.ui.pushButton_ToggleFill.connect('clicked(bool)', self.toggleFillButton)
    self.ui.pushButton_ToggleFill.setStyleSheet("background-color : indianred")
    self.ui.SegmentWindowPushButton.connect('clicked(bool)', self.onSegmendEditorPushButton)
    self.ui.SegmentWindowPushButton.setStyleSheet("background-color : lightgray")
    self.ui.radioButton_Edema.connect('clicked(bool)', self.onCheckEdema)

    # import qSlicerSegmentationsModuleWidgetsPythonQt
    # self.editor = qSlicerSegmentationsModuleWidgetsPythonQt.qMRMLSegmentEditorWidget()
    # self.editor.setMaximumNumberOfUndoStates(10)
    # self.editor.setMRMLScene(slicer.mrmlScene)


  def getDefaultDir(self):
      self.DefaultDir = qt.QFileDialog.getExistingDirectory(None,"Open default directory", self.DefaultDir, qt.QFileDialog.ShowDirsOnly)
      print(f'This is the Default Directory : {self.DefaultDir}')

  def onBrowseFoldersButton(self):
      print('Clicked Browse Button')
      print(f'Current path {self.DefaultDir}')
      # LLG get dialog window to ask for directory
      self.CurrentFolder= qt.QFileDialog.getExistingDirectory(None,"Open a folder", self.DefaultDir, qt.QFileDialog.ShowDirsOnly)
      print('Current Folder')
      print(self.CurrentFolder)
      self.updateCurrentFolder()
      # LLG GET A LIST OF cases WITHIN CURRENT FOLDERS (SUBDIRECTORIES). List comp to get only the case
      print(f'FDASFASDFSAFSAFASFAS{self.CurrentFolder}{os.sep}{VOLUME_FILE_TYPE}')
      self.CasesPaths = sorted(glob(f'{self.CurrentFolder}{os.sep}{VOLUME_FILE_TYPE}'))
      print('Case paths::::')
      print(self.CasesPaths)
      self.Cases = sorted([re.findall(r'Volume_(ID_[a-zA-Z\d]+)',os.path.split(i)[-1])[0] for i in self.CasesPaths])
      print('Case numbers::::')
      print(self.Cases)
      # Populate the SlicerDirectoryListView
      self.ui.SlicerDirectoryListView.addItems(self.Cases)
      self.ui.SlicerDirectoryListView.clicked.connect(self.getCurrentTableItem)
      # # SET CURRENT INDEX AT 0 ===THIS IS THE CENTRAL THING THAT HELPS FOR CASE NAVIGATION
      self.currentCase_index = 0
      self.updateCaseAll()
      self.loadPatient()

  
  def updateCaseAll(self):
      # All below is depend on self.currentCase_index updates, 
      self.currentCase = self.Cases[self.currentCase_index]
      self.currentCasePath = self.CasesPaths[self.currentCase_index]
      self.updateCaseIndex(self.currentCase_index)
      self.updateCurrentPatient()
      # self.ui.SlicerDirectoryListView.setCurrentRow(self.currentCase)

      
  def getCurrentTableItem(self):
      # When an item in SlicerDirectroyListView is selected the case number is printed
      print(self.ui.SlicerDirectoryListView.currentItem().text())
      # Below gives the row number == index to be used to select elements in the list
      print(self.ui.SlicerDirectoryListView.currentRow)
      #below we update the case index and we need to pass one parameter to the methods since it takes 2 (1 in addition to self)
      self.updateCaseIndex(self.ui.SlicerDirectoryListView.currentRow)
      # Update the case index
      self.currentCase_index = self.ui.SlicerDirectoryListView.currentRow
      # Same code in onBrowseFoldersButton, need to update self.currentCase
      # note that updateCaseAll() not implemented here 
      self.currentCase = self.Cases[self.currentCase_index]
      self.currentCasePath = self.CasesPaths[self.currentCase_index]
      self.updateCurrentPatient()
      self.loadPatient()

      # self.updateCurrentFolder()
      # self.loadPatient()

  def updateCaseIndex(self,index):
      # ----- ANW Modification ----- : Numerator on UI should start at 1 instead of 0 for coherence
      self.ui.FileIndex.setText('{} / {}'.format(index+1,len(self.Cases)))

  def updateCurrentFolder(self):
      # self.ui.CurrecntFolder.setText(os.path.join(self.CurrentFolder,self.currentCase))
      self.ui.CurrentFolder.setText('Current folder : \n{}'.format(self.CurrentFolder))
      
  def updateCurrentPatient(self):
      self.ui.CurrentPatient.setText(f'Current case : {self.currentCase}')  
  
  def updateCurrentSegmenationLabel(self):
      self.ui.CurrentSegmenationLabel.setText('Current segment : {}'.format(self.ICH_segm_name))
      
  def loadPatient(self):
      slicer.mrmlScene.Clear()
      slicer.util.loadVolume(self.currentCasePath)
      self.VolumeNode = slicer.util.getNodesByClass('vtkMRMLScalarVolumeNode')[0]
      self.updateCaseAll()
      self.ICH_segm_name = None
      self.ui.CurrentSegmenationLabel.setText('New patient loaded - No segmentation created!')
      # Adjust windowing (no need to use self. since this is used locally)
      Vol_displayNode = self.VolumeNode.GetDisplayNode()
      Vol_displayNode.AutoWindowLevelOff()
      Vol_displayNode.SetWindow(85)
      Vol_displayNode.SetLevel(45)
            
  def onPreviousButton(self):
      #Code below avoid getting in negative values. 
      self.currentCase_index = max(0,self.currentCase_index-1)
      # self.updateCaseAll()
      self.updateCaseAll()
      self.loadPatient()
  

  def onNextButton(self):
      print('Clicked Next Button',self.DefaultDir)
      self.currentCase_index = min(len(self.Cases)+1,self.currentCase_index+1)
      print(self.currentCase_index)
      # self.updateCaseAll()
      self.updateCaseAll()
      # self.currentCase = os.path.join(self.CurrentFolder,self.Cases[self.currentCase_index])
      self.loadPatient()

  # ----- ANW Modification ----- : This code is exactly the same as 2 blocks prior, I commented it
  # def loadPatient(self):
  #     slicer.mrmlScene.Clear()
  #     slicer.util.loadVolume(self.currentCasePath)
  #     self.VolumeNode = slicer.util.getNodesByClass('vtkMRMLScalarVolumeNode')[0]
  #     self.updateCaseAll()
  #     self.ICH_segm_name = None
  #     self.ui.CurrentSegmenationLabel.setText('New patient loaded - No segmentation created!')
  #     # Adjust windowing (no need to use self. since this is used locally)
  #     Vol_displayNode = self.VolumeNode.GetDisplayNode()
  #     Vol_displayNode.AutoWindowLevelOff()
  #     Vol_displayNode.SetWindow(85)
  #     Vol_displayNode.SetLevel(45)


  def onNewICHSegm(self):
      # slicer.util.selectModule("SegmentEditor")
      self.ICH_segm_name = "{}_ICH".format(self.currentCase)
      print(f'Segmentation name:: {self.ICH_segm_name}')
      self.segmentEditorWidget = slicer.modules.segmenteditor.widgetRepresentation().self().editor
      self.segmentEditorNode = self.segmentEditorWidget.mrmlSegmentEditorNode()
      self.segmentationNode=slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
      self.segmentEditorWidget.setSegmentationNode(self.segmentationNode)
      self.segmentEditorWidget.setMasterVolumeNode(self.VolumeNode)
      # set refenrence geometry to Volume node
      self.segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(self.VolumeNode)
      #below with add a 'segment' in the segmentatation node which is called 'self.ICH_segm_name
      self.addedSegmentID = self.segmentationNode.GetSegmentation().AddEmptySegment(self.ICH_segm_name)
      #Select Segment (else you need to click on it yourself)
      shn = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)
      items = vtk.vtkIdList()
      sc = shn.GetSceneItemID()
      shn.GetItemChildren(sc, items, True)
      self.ICH_segment_name = shn.GetItemName(items.GetId(2))
      self.segmentEditorNode.SetSelectedSegmentID(self.ICH_segment_name)
      self.updateCurrentSegmenationLabel()
      # Toggle paint brush right away. 
      self.onPushButton_1()
      self.startTimer()

      # ----- ANW Addition ----- : Reset called to False when new segmentation is created to restart the timer
      self.called = False

  def onNewICHSegm(self):
      # slicer.util.selectModule("SegmentEditor")
      self.ICH_segm_name = "{}_ICH".format(self.currentCase)
      print(f'Segmentation name:: {self.ICH_segm_name}')
      self.segmentEditorWidget = slicer.modules.segmenteditor.widgetRepresentation().self().editor
      self.segmentEditorNode = self.segmentEditorWidget.mrmlSegmentEditorNode()
      self.segmentationNode=slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
      self.segmentEditorWidget.setSegmentationNode(self.segmentationNode)
      self.segmentEditorWidget.setMasterVolumeNode(self.VolumeNode)
      # set refenrence geometry to Volume node
      self.segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(self.VolumeNode)
      #below with add a 'segment' in the segmentatation node which is called 'self.ICH_segm_name
      self.addedSegmentID = self.segmentationNode.GetSegmentation().AddEmptySegment(self.ICH_segm_name)
      #Select Segment (else you need to click on it yourself)
      shn = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)
      items = vtk.vtkIdList()
      sc = shn.GetSceneItemID()
      shn.GetItemChildren(sc, items, True)
      self.ICH_segment_name = shn.GetItemName(items.GetId(2))
      self.segmentEditorNode.SetSelectedSegmentID(self.ICH_segment_name)
      self.updateCurrentSegmenationLabel()
      # Toggle paint brush right away.
      self.onPushButton_1()
      self.startTimer()

      # ----- ANW Addition ----- : Reset called to False when new segmentation is created to restart the timer
      self.called = False
  
  # def startTimer(self):
  #     print('ICH segment name::: {}'.format(self.ICH_segment_name))
  #     self.start_time = datetime.now()
  #     print("STARTING TIMER !!!!")
  #
  #     # ----- ANW Addition ----- : Code to keep track of time passed with lcdNumber on UI
  #     # Create a timer
  #     self.timer = qt.QTimer()
  #     self.timer.timeout.connect(self.updatelcdNumber)
  #
  #     # Start the timer and update every second
  #     self.timer.start(1000)
  #
  #     # Call the updatelcdNumber function
  #     self.updatelcdNumber()



  def startTimer(self):
      print('ICH segment name::: {}'.format(self.ICH_segment_name))
      self.counter = 0

      self.flag = True
      print("STARTING TIMER !!!!")

      # ----- ANW Addition ----- : Code to keep track of time passed with lcdNumber on UI
      # Create a timer
      self.timer = qt.QTimer()
      self.timer.timeout.connect(self.updatelcdNumber)

      # Start the timer and update every second
      self.timer.start(100)

      # Call the updatelcdNumber function
      self.updatelcdNumber()

  def updatelcdNumber(self):
      # Get the time
      if self.flag:
          self.counter += 1

      self.ui.lcdNumber.display(self.counter/10)

  # def stopTimer(self):
  #     # If already called once (i.e when user pressed save segm button but forgot to annotator name), simply return the time
  #     if self.called:
  #         return self.total_time
  #     else:
  #         try:
  #             print('STOPPING TIMER!')
  #             self.total_time = round((time.perf_counter() - self.start_time), 2)
  #             self.timer.stop()
  #             print(f"Total segmentation time: {self.total_time} seconds")
  #             self.called = True
  #             return self.total_time
  #         except AttributeError as e:
  #             print(f'!!! YOU DID NOT START THE COUNTER !!! :: {e}')
  #             return None

  def stopTimer(self):
      # If already called once (i.e when user pressed save segm button but forgot to annotator name), simply return the time
      if self.called:
          return self.total_time
      else:
          try:
              print('STOPPING TIMER!')
              self.total_time = self.counter/10
              self.timer.stop()
              print(f"Total segmentation time: {self.total_time} seconds")
              self.flag = False
              self.called = True
              return self.total_time
          except AttributeError as e:
              print(f'!!! YOU DID NOT START THE COUNTER !!! :: {e}')
              return None

  # def togglePauseTimerButton(self):
  #     # if button is checked
  #     if self.ui.PauseTimerButton.isChecked():
  #         # setting background color to light-blue
  #         self.ui.PauseTimerButton.setStyleSheet("background-color : lightblue")
  #         self.ui.PauseTimerButton.setText('Restart')
  #         self.intermediate_time = round((time.perf_counter() - self.start_time), 2)
  #         self.timer.stop()
  #
  #     # if it is unchecked
  #     else:
  #         # set background color back to light-grey
  #         self.ui.PauseTimerButton.setStyleSheet("background-color : lightgrey")
  #         self.ui.PauseTimerButton.setText('Pause')
  #         self.timer.start(1000)


  def togglePauseTimerButton(self):
      # if button is checked - Time paused
      if self.ui.PauseTimerButton.isChecked():
          # setting background color to light-blue
          self.ui.PauseTimerButton.setStyleSheet("background-color : lightblue")
          self.ui.PauseTimerButton.setText('Restart')
          self.timer.stop()
          self.flag = False

      # if it is unchecked
      else:
          # set background color back to light-grey
          self.ui.PauseTimerButton.setStyleSheet("background-color : lightgrey")
          self.ui.PauseTimerButton.setText('Pause')
          self.timer.start(100)
          self.flag = True



  def createFolders(self):
      self.revision_step = self.ui.RevisionStep.currentText
      if len(self.revision_step) != 0:
          self.output_dir_labels= os.path.join(self.CurrentFolder, f'Labels_{self.revision_step[0]}') # only get the number
          os.makedirs(self.output_dir_labels, exist_ok=True)
          # add a subfolder with nifti segmentations
          self.output_dir_labels_nii = os.path.join(self.CurrentFolder, f'Labels_nii_{self.revision_step[0]}')
          os.makedirs(self.output_dir_labels_nii, exist_ok=True)
          # Create separate folder
          self.output_dir_time= os.path.join(self.CurrentFolder, f'Time_{self.revision_step[0]}')
          os.makedirs(self.output_dir_time, exist_ok=True)
      else:
          print('Please select revision step !!!')
          msgboxtime = qt.QMessageBox()
          msgboxtime.setText("Segmentation not saved : revision step is not defined!  \n Please save again with revision step!")
          msgboxtime.exec()


  def onCheckEdema(self):

      if self.ui.radioButton_Edema.isChecked(): # Uncheck autoExclusive in UI or else it will stay checked forever
          self.edema = self.ui.radioButton_Edema.text
      else:
          self.edema = None

      return self.edema


  # ----- Modification -----
  def onSaveSegmentationButton(self):
      # Note that perf_counter should only be used for interval counting, returns float of time in SECONDS
      #By default creates a new folder in the volume directory 
      # FUTURE IMPROVEMENT: add the name of the segmenter and level in the name

      # Stop the timer when the button is pressed
      self.time = self.stopTimer()


      # Create folders if not exist
      self.createFolders()

      #    print(self.AnnotatorDegree.currentText)
      self.annotator_name = self.ui.Annotator_name.text
      self.annotator_degree = self.ui.AnnotatorDegree.currentText

      self.edema = self.onCheckEdema()


      # Save if annotator_name is not empty and timer started:
      if self.annotator_name and self.time is not None:
          print('Saving time')
          # Save time to csv
          self.df = pd.DataFrame(
              {'Case number': [self.currentCase], 'Annotator Name': [self.annotator_name], 'Annotator degree': [self.annotator_degree],
               'Time': [str(self.time)], 'Revision step': [self.revision_step[0]]})

          self.outputTimeFile = os.path.join(self.output_dir_time,
                                             '{}_Case_{}_time_{}.csv'.format(self.annotator_name, self.currentCase, self.revision_step[0]))
          if not os.path.isfile(self.outputTimeFile):
              self.df.to_csv(self.outputTimeFile)
          else:
              print('This time file already exists')
              msg1 = qt.QMessageBox()
              msg1.setWindowTitle('Save As')
              msg1.setText(
                  f'The file {self.annotator_name}_Case_{self.currentCase}_time_{self.revision_step[0]}.csv already exists \n Do you want to replace the existing file?')
              msg1.setIcon(qt.QMessageBox.Warning)
              msg1.setStandardButtons(qt.QMessageBox.Ok | qt.QMessageBox.Cancel)
              msg1.buttonClicked.connect(self.msg1_clicked)
              msg1.exec()

          # Save .nrrd file
          if self.edema is None:
              self.outputSegmFile = os.path.join(self.output_dir_labels,
                                                 "{}_{}_{}.seg.nrrd".format(self.ICH_segm_name, self.annotator_name, self.revision_step[0]))
          else:
              self.outputSegmFile = os.path.join(self.output_dir_labels,
                                                 "{}_{}_{}_{}.seg.nrrd".format(self.ICH_segm_name, self.annotator_name, self.edema,
                                                                            self.revision_step[0]))
          if not os.path.isfile(self.outputSegmFile):
              slicer.util.saveNode(self.segmentationNode, self.outputSegmFile)
          else:
              print('This .nrrd file already exists')
              msg2 = qt.QMessageBox()
              msg2.setWindowTitle('Save As')
              msg2.setText(
                  f'The file {self.ICH_segm_name}_{self.annotator_name}_{self.revision_step[0]}.seg.nrrd already exists \n Do you want to replace the existing file?')
              msg2.setIcon(qt.QMessageBox.Warning)
              msg2.setStandardButtons(qt.QMessageBox.Ok | qt.QMessageBox.Cancel)
              msg2.buttonClicked.connect(self.msg2_clicked)
              msg2.exec()

          # Save alternative nitfi
          # Export segmentation to a labelmap volume
          # Note to save to nifti you need to convert to labelmapVolumeNode
          self.labelmapVolumeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLabelMapVolumeNode')
          slicer.modules.segmentations.logic().ExportVisibleSegmentsToLabelmapNode(self.segmentationNode,
                                                                                   self.labelmapVolumeNode,
                                                                                   self.VolumeNode)
          if self.edema is None:
              self.outputSegmFileNifti = os.path.join(self.output_dir_labels_nii,
                                                  "{}_{}_{}.nii.gz".format(self.ICH_segm_name, self.annotator_name, self.revision_step[0]))
          else:
              self.outputSegmFileNifti = os.path.join(self.output_dir_labels_nii,
                                                      "{}_{}_{}_{}.nii.gz".format(self.ICH_segm_name, self.annotator_name, self.edema,
                                                                               self.revision_step[0]))
          if not os.path.isfile(self.outputSegmFileNifti):
              slicer.util.saveNode(self.labelmapVolumeNode, self.outputSegmFileNifti)
          else:
              print('This .nii.gz file already exists')
              msg3 = qt.QMessageBox()
              msg3.setWindowTitle('Save As')
              msg3.setText(
                  f'The file {self.ICH_segm_name}_{self.annotator_name}_{self.revision_step[0]}.nii.gz already exists \n Do you want to replace the existing file?')
              msg3.setIcon(qt.QMessageBox.Warning)
              msg3.setStandardButtons(qt.QMessageBox.Ok | qt.QMessageBox.Cancel)
              msg3.buttonClicked.connect(self.msg3_clicked)
              msg3.exec()

          # Saving messages
          print((f'Saving case : {self.VolumeNode.GetName()}'))
          self.ui.CurrentSegmenationLabel.setText(f'Case {self.VolumeNode.GetName()} saved !')

      # If annotator_name empty or timer not started.
      else:
          if not self.annotator_name:
              print('Empty annotator name !!!')
              msgboxtime = qt.QMessageBox()
              msgboxtime.setText("Segmentation not saved : no annotator name !  \n Please save again with your name!")
              msgboxtime.exec()
          elif self.time is None:
              print('You did not start the timer !!!')
              msgboxtime = qt.QMessageBox()
              msgboxtime.setText(
                  "You did not start a timed segmentation. \n Please press the 'New ICH segm' button to start a timed segmentation")
              msgboxtime.exec()


      try:
        self.SlicerVolumeName = re.findall('Volume_(ID_[a-zA-Z\d]+)', self.VolumeNode.GetName())[0]
        print(f'Volume Node accoding to slicer :: {self.SlicerVolumeName}')
        print('Volume Name according to GUI: {}'.format(self.currentCase))
        assert self.currentCase == self.SlicerVolumeName
        print('Matched Volume number (sanity check)!')
      except AssertionError as e:
        print('Mismatch in case error :: {}'.format(str(e)))



  # ----- ANW Addition ----- : Actions for pop-up message box buttons
  def msg1_clicked(self, msg1_button):
      if msg1_button.text == 'OK':
          self.df.to_csv(self.outputTimeFile)
      else:
          return

  def msg2_clicked(self, msg2_button):
      if msg2_button.text == 'OK':
          slicer.util.saveNode(self.segmentationNode, self.outputSegmFile)
      else:
          return

  def msg3_clicked(self, msg3_button):
      if msg3_button.text == 'OK':
          slicer.util.saveNode(self.labelmapVolumeNode, self.outputSegmFileNifti)
      else:
          return
      
  def onBrowseFolders_2Button(self):
      self.predictionFolder= qt.QFileDialog.getExistingDirectory(None,"Open a folder", self.DefaultDir, qt.QFileDialog.ShowDirsOnly)

      self.predictions_paths = sorted(glob(os.path.join(self.predictionFolder, f'{SEGM_FILE_TYPE}')))
      print(self.predictions_paths)

      try:
        assert len(self.CasesPaths) == (len(self.predictions_paths) or len(self.predictions_paths_NIFTI))
      except AssertionError as e:
        print('Not the same number of Volumes and predictions !')
        msgboxpred = qt.QMessageBox()
        msgboxpred.setText("Not the same number of Volumes and predictions !")
        msgboxpred.exec()
      
      # self.prediction_name = 

  def onLoadPredictionButton(self): 
      # Get list of prediction names
      try:
        self.predictions_names = sorted([re.findall(r'(ID_[a-zA-Z\d]+)_ICH_predictions.seg.nrrd',os.path.split(i)[-1]) for i in self.predictions_paths])
        print(self.predictions_names)
        self.called = False # restart timer
      except AttributeError as e:
            msgnopredloaded=qt.QMessageBox() # Typo correction
            msgnopredloaded.setText('Please select the prediction directory!')
            msgnopredloaded.exec()
            # Then load the browse folder thing for the user
            self.onBrowseFolders_2Button()
      # Match the prediction names that corresponds to the loaded segmentatiion
      # self.currentPrediction_Index, self.currentPrediction_ID = [(i,j) for i,j in enumerate(self.predictions_names) if j == self.currentCase][0]
      self.currentPrediction_Index, self.currentPrediction_ID = [(i, self.predictions_names[i]) for i in range(len(self.predictions_names)) if i == self.currentCase_index][0] # return a list of tuples
      print(f'Current case :: {self.currentCase}')
      print(f'Current prediction ID :: {self.currentPrediction_ID }')
      print(f'Current case index :: {self.currentCase_index}')
      print(f'Current prediction index :: {self.currentPrediction_Index}')
      
      self.currentPredictionPath = self.predictions_paths[self.currentCase_index]
      # print(self.currentPrediction_ID)
      # print(self.currentPrediction_Index)
    
      slicer.util.loadSegmentation(self.currentPredictionPath)
    
      # 'ACTIVATE' segmentation node in Slicer
      # slicer.util.loadSegmentation(self.currentCasePath)
      self.segmentationNode = slicer.util.getNodesByClass('vtkMRMLSegmentationNode')[0]
      self.segmentEditorWidget = slicer.modules.segmenteditor.widgetRepresentation().self().editor
      self.segmentEditorNode =  self.segmentEditorWidget.mrmlSegmentEditorNode()
      self.segmentEditorWidget.setSegmentationNode(self.segmentationNode)
      self.segmentEditorWidget.setMasterVolumeNode(self.VolumeNode)
      # set refenrence geometry to Volume node
      self.segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(self.VolumeNode)
      # self.segmentationNode= slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLSegmentationNode")
      # if self.segmentationNode:
      #       self._parameterNode.SetNodeReferenceID("InputVolume", self.segmentationNode.GetID())
      nn = self.segmentationNode.GetDisplayNode()
      # set Segmentation visible:
      nn.SetAllSegmentsVisibility(True)
      
      # Update the segmentation name (needed for saving the segmentation)
      self.ICH_segm_name = self.segmentationNode.GetName()
      
      #  self.segmentationNode.
      # self.segmentEditorWidget.setSegmentationNode(self.segmentationNode)
      # self.segmentEditorWidget.setMasterVolumeNode(self.VolumeNode)
      # self.segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(self.VolumeNode)
      
      #below with add a 'segment' in the segmentatation node which is called 'self.ICH_segm_name
      #Select Segment (else you need to click on it yourself)
      shn = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)
      items = vtk.vtkIdList()
      sc = shn.GetSceneItemID()
      shn.GetItemChildren(sc, items, True)
      self.ICH_segment_name = shn.GetItemName(items.GetId(2))
      print(f'Segment name :: {self.ICH_segment_name}')
      self.segmentEditorNode.SetSelectedSegmentID(self.ICH_segment_name)
      self.updateCurrentSegmenationLabel()
      # Start timer
      self.startTimer()
      
      # # Set to erase then paint (so you can use the space bar)
      # segmentEditorWidget.setActiveEffectByName("Erase")
      # segmentEditorWidget.setActiveEffectByName("Paint")
      # effect = segmentEditorWidget.activeEffect()
      # effect.setParameter('BrushSphere', 1)

      # ### MASK
      # #Set mask mode
      # segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedEverywhere)
      # #Set if using Editable intensity range (the range is defined below using object.setParameter)
      # segmentEditorNode.SetMasterVolumeIntensityMask(True)
      # segmentEditorNode.SetMasterVolumeIntensityMaskRange(35, 90)
      # #Set overwrite options
      # segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)


  # def setVolumeandSegmentationNodes(self):
  #     self.segmentEditorWidget = slicer.modules.segmenteditor.widgetRepresentation().self().editor
  #     self.segmentEditorWidget.setSegmentationNode(self.segmentationNode)
  #     self.segmentEditorWidget.setMasterVolumeNode(self.VolumeNode)
  #     self.segmentEditorNode = self.segmentEditorWidget.mrmlSegmentEditorNode()
  #     # Set reference geometry
  #     self.segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(self.VolumeNode)
  #     self.addedSegmentID = self.segmentationNode.GetSegmentation().AddEmptySegment(self.ICH_segm_name)
  #     #Select segmetnation 
  #     shn = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)
  #     items = vtk.vtkIdList()
  #     sc = shn.GetSceneItemID()
  #     shn.GetItemChildren(sc, items, True)
  #     self.ICH_segment_name = shn.GetItemName(items.GetId(2))
  #     print('ICH segment name::: {}'.format(self.ICH_segment_name))
  #     self.segmentEditorNode.SetSelectedSegmentID(self.ICH_segment_name)
      #Set mask mode (DOES NOT WORK ???????)

  def onSegmendEditorPushButton(self):

      if self.ui.SegmentWindowPushButton.isChecked():
          self.ui.SegmentWindowPushButton.setStyleSheet("background-color : gray")
          self.ui.SegmentWindowPushButton.setText('Undock Segment Editor')
          slicer.modules.segmenteditor.widgetRepresentation().setParent(None)
          slicer.modules.segmenteditor.widgetRepresentation().show()

      # if it is unchecked (default)
      else:
          self.ui.SegmentWindowPushButton.setStyleSheet("background-color : lightgray")
          self.ui.SegmentWindowPushButton.setText('Dock Segment Editor')
          slicer.modules.segmenteditor.widgetRepresentation().setParent(slicer.util.mainWindow())


      # self.ui.SegmentWindowPushButton.show()


  def onPushButton_1(self):
      print('PushButton_1 pressed')
      # code commented out below has been moved above. 
      # STEP 1
      # # Create a widget to access the segment editor tools 
      # self.segmentEditorWidget = slicer.modules.segmenteditor.widgetRepresentation().self().editor
      # self.segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
      # self.segmentEditorNode = self.segmentEditorWidget.mrmlSegmentEditorNode()
      # # connect widget to editor node (not sure if need was note doing this in the past)
      # self.segmentEditorWidget.setMRMLSegmentEditorNode(self.segmentEditorNode)
      
      # # STEP 2 
      # # Get the currently loaded volume node
      # self.volumeNode =slicer.util.getNodesByClass('vtkMRMLScalarVolumeNode')[0]
      # print(self.volumeNode.GetName())
      # ## Get the currently loaded segmentation node
      # self.segmentationNode= slicer.util.getNodesByClass('vtkMRMLSegmentationNode')[0]
      # print(self.segmentationNode.GetName())
      # # Set the volume and segmentation nodes
      # self. segmentEditorWidget.setSegmentationNode(self.segmentationNode)
      # self.segmentEditorWidget.setMasterVolumeNode(self.volumeNode)
      #Bonus if needed (can be runned without the code below)
      # Get the segment ID (this is going to be used below) - if need to get it check Evernote this is complicated...
      # self.segid = self.egmentationNode.GetSegmentation().GetSegmentIdBySegmentName('Segment_1')
      # print(self.segid)
      # Running the effect:
      # Select the right effect
      self.segmentEditorWidget.setActiveEffectByName("Paint")
      # Note it seems that sometimes you need to activate the effect first with :
      # Assign effect to the segmentEditorWidget using the active effect
      self.effect = self.segmentEditorWidget.activeEffect()
      self.effect.activate()
      self.effect.setParameter('BrushSphere',1)
      #Seems that you need to activate the effect to see it in Slicer
      # Set up the mask parameters (note that PaintAllowed...was changed to EditAllowed)
      self.segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentationNode.EditAllowedEverywhere)
      #Set if using Editable intensity range (the range is defined below using object.setParameter)
      self.segmentEditorNode.SetMasterVolumeIntensityMask(True)
      self.segmentEditorNode.SetMasterVolumeIntensityMaskRange(37, 100)
      self.segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteAllSegments)



  def onPushButton_2(self):
      # Remove fill
      # segmentEditorWidget = slicer.modules.segmenteditor.widgetRepresentation().self().editor
      # segmentEditorWidget.setSegmentationNode(self.Segmentation)
      # segmentEditorWidget.setMasterVolumeNode(self.Volume)
      # segmentationNode = slicer.util.getNode("vtkMRMLSegmentationNode1")
      self.segmentationNode.GetDisplayNode().SetOpacity2DFill(0)

  def onPushButton_3(self):
  #     # Add fill
      self.segmentationNode.GetDisplayNode().SetOpacity2DFill(100)

  def toggleFillButton(self):
      if self.ui.pushButton_ToggleFill.isChecked():
          self.ui.pushButton_ToggleFill.setStyleSheet("background-color : lightgreen")
          self.ui.pushButton_ToggleFill.setText('Fill ON')
          self.segmentationNode.GetDisplayNode().SetOpacity2DFill(0)
      # if it is unchecked
      else:
          self.ui.pushButton_ToggleFill.setStyleSheet("background-color : indianred")
          self.ui.pushButton_ToggleFill.setText('Fill OFF')
          self.segmentationNode.GetDisplayNode().SetOpacity2DFill(100)


  def onPushButton_4(self):
      self.segmentEditorWidget.setActiveEffectByName("Paint")
      # Note it seems that sometimes you need to activate the effect first with :
      # Assign effect to the segmentEditorWidget using the active effect
      self.effect = self.segmentEditorWidget.activeEffect()
      #Seems that you need to activate the effect to see it in Slicer
      self.effect.activate()
      # Set up the mask parameters (note that PaintAllowed...was changed to EditAllowed)
      self.segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentationNode.EditAllowedEverywhere)
      #Set if using Editable intensity range (the range is defined below using object.setParameter)
      self.segmentEditorNode.SetMasterVolumeIntensityMask(False)
      self.segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteAllSegments)
      # Paint mode
      # # Note I added self for segment editor widget but not for the other in an attempt to be able to undo on the same instance...last button... does not workd
      # self.segmentEditorWidget = slicer.modules.segmenteditor.widgetRepresentation().self().editor
      # self.segmentEditorWidget.setSegmentationNode(self.Segmentation)
      # self.segmentEditorWidget.setMasterVolumeNode(self.Volume)
      # segmentEditorNode = self.segmentEditorWidget.mrmlSegmentEditorNode()
      # segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedEverywhere)
      # #Set if using Editable intensity range (the range is defined below using object.setParameter)
      # segmentEditorNode.SetMasterVolumeIntensityMask(False)
      # # Set to erase then paint (so you can use the space bar)
      # self.segmentEditorWidget.setActiveEffectByName("Paint")
      # effect = self.segmentEditorWidget.activeEffect()
      # effect.setParameter('BrushSphere', 0) 

  def onPushButton_5(self):
      self.segmentEditorWidget.setActiveEffectByName("Erase")
      # Note it seems that sometimes you need to activate the effect first with :
      # Assign effect to the segmentEditorWidget using the active effect
      self.effect = self.segmentEditorWidget.activeEffect()
      #Seems that you need to activate the effect to see it in Slicer
      self.effect.activate()
      self.segmentEditorNode.SetMasterVolumeIntensityMask(False)

  def onPushButton_6(self):
      # pass
      # Smoothing
      self.segmentEditorWidget = slicer.modules.segmenteditor.widgetRepresentation().self().editor
      self.segmentEditorWidget.setActiveEffectByName("Smoothing")
      effect = self.segmentEditorWidget.activeEffect()
      effect.setParameter("SmoothingMethod", "MEDIAN")
      effect.setParameter("KernelSizeMm", 3)
      effect.self().onApply()

  def onPushButton_7(self):
      # pass
      #Set mask mode
      self.segmentEditorWidget = slicer.modules.segmenteditor.widgetRepresentation().self().editor
      self.segmentEditorNode = self.segmentEditorWidget.mrmlSegmentEditorNode()
      self.segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentationNode.EditAllowedEverywhere)
      #Set if using Editable intensity range (the range is defined below using object.setParameter)
      self.segmentEditorNode.SetMasterVolumeIntensityMask(True)
      self.segmentEditorNode.SetMasterVolumeIntensityMaskRange(40, 90)
      #Set overwrite options
      self.segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)

  def onPushButton_8(self):
      # pass
      # REMOVE MASK
      # Set mask mode
      segmentEditorWidget = slicer.modules.segmenteditor.widgetRepresentation().self().editor
      segmentEditorNode = segmentEditorWidget.mrmlSegmentEditorNode()
      segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentationNode.EditAllowedEverywhere)
      #Set if using Editable intensity range (the range is defined below using object.setParameter)
      segmentEditorNode.SetMasterVolumeIntensityMask(False)
      #Set overwrite options
      segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
      
  def onPushButton_9(self):
      # pass
      # Fill holes smoothing
      self.segmentEditorWidget = slicer.modules.segmenteditor.widgetRepresentation().self().editor
      self.segmentEditorWidget.setActiveEffectByName("Smoothing")
      effect = self.segmentEditorWidget.activeEffect()
      effect.setParameter("SmoothingMethod", "MORPHOLOGICAL_CLOSING")
      effect.setParameter("KernelSizeMm", 3)
      effect.self().onApply()

  def onPushButton_11(self):
      # Toggle segement editor
      # Set segment editor and get the right segmentations
      slicer.util.selectModule("SegmentEditor")
      # segmentEditorWidget = slicer.modules.segmenteditor.widgetRepresentation().self().editor
      # segmentEditorWidget.setSegmentationNode(self.Segmentation)
      # segmentEditorWidget.setMasterVolumeNode(self.Volume)
      
  def onPushButton_10(self):
      pass

  def onToggleFill(self):
      print('Does not work yet :-( ')
  #     pass


#
# ICH_SEGMENTER_2022_08Logic
#

class ICH_SEGMENTER_2022_08Logic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self):
    """
    Called when the logic class is instantiated. Can be used for initializing member variables.
    """
    ScriptedLoadableModuleLogic.__init__(self)

  def setDefaultParameters(self, parameterNode):
    """
    Initialize parameter node with default settings.
    """
    if not parameterNode.GetParameter("Threshold"):
      parameterNode.SetParameter("Threshold", "100.0")
    if not parameterNode.GetParameter("Invert"):
      parameterNode.SetParameter("Invert", "false")

  def process(self, inputVolume, outputVolume, imageThreshold, invert=False, showResult=True):
    """
    Run the processing algorithm.
    Can be used without GUI widget.
    :param inputVolume: volume to be thresholded
    :param outputVolume: thresholding result
    :param imageThreshold: values above/below this threshold will be set to 0
    :param invert: if True then values above the threshold will be set to 0, otherwise values below are set to 0
    :param showResult: show output volume in slice viewers
    """

    if not inputVolume or not outputVolume:
      raise ValueError("Input or output volume is invalid")

    import time
    startTime = time.time()
    logging.info('Processing started')

    # Compute the thresholded output volume using the "Threshold Scalar Volume" CLI module
    cliParams = {
      'InputVolume': inputVolume.GetID(),
      'OutputVolume': outputVolume.GetID(),
      'ThresholdValue' : imageThreshold,
      'ThresholdType' : 'Above' if invert else 'Below'
      }
    cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True, update_display=showResult)
    # We don't need the CLI module node anymore, remove it to not clutter the scene with it
    slicer.mrmlScene.RemoveNode(cliNode)

    stopTime = time.time()
    logging.info(f'Processing completed in {stopTime-startTime:.2f} seconds')


#
# ICH_SEGMENTER_2022_08Test
#

class ICH_SEGMENTER_2022_08Test(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear()

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_ICH_SEGMENTER_2022_081()

  def test_ICH_SEGMENTER_2022_081(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")

    # Get/create input data

    import SampleData
    registerSampleData()
    inputVolume = SampleData.downloadSample('ICH_SEGMENTER_2022_081')
    self.delayDisplay('Loaded test data set')

    inputScalarRange = inputVolume.GetImageData().GetScalarRange()
    self.assertEqual(inputScalarRange[0], 0)
    self.assertEqual(inputScalarRange[1], 695)

    outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
    threshold = 100

    # Test the module logic

    logic = ICH_SEGMENTER_2022_08Logic()

    # Test algorithm with non-inverted threshold
    logic.process(inputVolume, outputVolume, threshold, True)
    outputScalarRange = outputVolume.GetImageData().GetScalarRange()
    self.assertEqual(outputScalarRange[0], inputScalarRange[0])
    self.assertEqual(outputScalarRange[1], threshold)

    # Test algorithm with inverted threshold
    logic.process(inputVolume, outputVolume, threshold, False)
    outputScalarRange = outputVolume.GetImageData().GetScalarRange()
    self.assertEqual(outputScalarRange[0], inputScalarRange[0])
    self.assertEqual(outputScalarRange[1], inputScalarRange[1])

    self.delayDisplay('Test passed')
