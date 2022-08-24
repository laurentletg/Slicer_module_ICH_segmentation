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
      self.ui.FileIndex.setText('{} / {}'.format(index,len(self.Cases)))

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
  
  def startTimer(self):
      print('ICH segment name::: {}'.format(self.ICH_segment_name))
      self.start_time = time.perf_counter()
      print("STARTING TIMER !!!!")


  
        
  def onSaveSegmentationButton(self):
      # Note that perf_counter should only be used for interval counting, returns float of time in SECONDS
      #By default creates a new folder in the volume directory 
      # FUTURE IMPROVEMENT: add the name of the segmenter and level in the name
      self.output_dir_labels= os.path.join(self.CurrentFolder, 'Labels')
      os.makedirs(self.output_dir_labels, exist_ok= True)
      # add a subfolder with nifti segmentations
      self.output_dir_labels_nii = os.path.join(self.CurrentFolder, 'Labels_nii')
      os.makedirs(self.output_dir_labels_nii, exist_ok= True)
      #    print(self.AnnotatorDegree.currentText) 
          
      try:
        print('STOPPING TIMER!')
        self.total_time = round((time.perf_counter() - self.start_time), 2)
        print(f"Total segmentation time: {self.total_time} seconds")
      except AttributeError as e:
        print(f'!!! YOU DID NOT START THE COUNTER !!! :: {e}')    
      # TOTAL TIME
      # Save time to csv
      # Create separate folder
      print('Saving time')
      self.output_dir_time= os.path.join(self.CurrentFolder, 'Time')
      os.makedirs(self.output_dir_time, exist_ok= True)
      annotator_name = self.ui.Annotator_name.text
      
      if annotator_name:
            df = pd.DataFrame({'Case number':[self.currentCase],'Annotator Name':[annotator_name], 'Time':[str(self.total_time)]})
            df.to_csv(os.path.join(self.output_dir_time,'{}_Case_{}_time.csv'.format(annotator_name,self.currentCase)))
      else:
            print('Empty annotator name !!!')
            msgboxtime = qt.QMessageBox()
            msgboxtime.setText("Segmentation not saved : no annotator name !  \n Please save again with your name!")
            msgboxtime.exec()
      # Msg box if no segmentation 
      if self.ICH_segm_name:
            self.segmentEditorNode.SetSelectedSegmentID(self.ICH_segm_name)
      else:
            msgbox_no_segm = qt.QMessageBox()
            msgbox_no_segm.setText("No segmentation loaded !")
            msgbox_no_segm.exec()
            
      # #Remove segmentation fill
      # segmentationNode.GetDisplayNode().SetOpa``city2DFill(0)
      self.outputSegmFile = os.path.join(self.output_dir_labels,"{}_{}.seg.nrrd".format(self.ICH_segm_name, annotator_name))
      slicer.util.saveNode(self.segmentationNode, self.outputSegmFile)
      # Save alternative nitfi 
      # Export segmentation to a labelmap volume
      # Note to save to nifti you need to convert to labelmapVolumeNode
      labelmapVolumeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLabelMapVolumeNode')
      slicer.modules.segmentations.logic().ExportVisibleSegmentsToLabelmapNode(self.segmentationNode, labelmapVolumeNode, self.VolumeNode)   
      self.outputSegmFileNifti = os.path.join(self.output_dir_labels_nii,"{}_{}.nii.gz".format(self.ICH_segm_name, annotator_name))
      slicer.util.saveNode(labelmapVolumeNode, self.outputSegmFileNifti)
      #Saving messages
      print((f'Saving case : {self.VolumeNode.GetName()}'))
      self.ui.CurrentSegmenationLabel.setText(f'Case {self.VolumeNode.GetName()} saved !')
      
      try:
        self.SlicerVolumeName = re.findall('Volume_(ID_[a-zA-Z\d]+)', self.VolumeNode.GetName())[0]
        print(f'Volume Node accoding to slicer :: {self.SlicerVolumeName}')
        print('Volume Name according to GUI: {}'.format(self.currentCase))
        assert self.currentCase == self.SlicerVolumeName
        print('Matched Volume number (sanity check)!')
      except AssertionError as e:
        print('Mismatch in case error :: {}'.format(str(e)))
        
      
  def onBrowseFolders_2Button(self):
      self.predictionFolder= qt.QFileDialog.getExistingDirectory(None,"Open a folder", self.DefaultDir, qt.QFileDialog.ShowDirsOnly)
      self.predictions_paths = sorted(glob(os.path.join(self.predictionFolder, f'{SEGM_FILE_TYPE}')))
      print(self.predictions_paths)
      try:
        assert len(self.CasesPaths)==len(self.predictions_paths)
      except AssertionError as e:
        print('Not the same number of Volumes and predictions !')
        msgboxpred = qt.QMessageBox()
        msgboxpred.setText("Not the same number of Volumes and predictions !")
        msgboxpred.exec()
      
      # self.prediction_name = 

  def onLoadPredictionButton(self): 
      # Get list of prediction names
      try:
        self.predictions_names = sorted([re.findall(r'(ID_[a-zA-Z\d]+)_ICH_pred.seg.nrrd',os.path.split(i)[-1])[0] for i in self.predictions_paths])
        print(self.predictions_names)
      except AttributeError as e:
            msgnopredloaded=qt.QMessapgeBox()
            msgnopredloaded.setText('Please select the prediction directory!')
            msgnopredloaded.exec()
            # Then load the browse folder thing for the user
            self.onBrowseFolders_2Button()
      # Match the prediction names that corresponds to the loaded segmentatiion
      self.currentPrediction_Index,self.currentPrediction_ID = [(i,j) for i,j in enumerate(self.predictions_names) if j == self.currentCase][0]
      print(f'Current case :: {self.currentCase}')
      print(f'Current pred ID :: {self.currentPrediction_ID }')
      print(f'Current case index :: {self.currentCase_index}')
      print(f'Current pred index :: {self.currentPrediction_Index}')
      
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
      print(f'Segment name {self.ICH_segment_name}')
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
