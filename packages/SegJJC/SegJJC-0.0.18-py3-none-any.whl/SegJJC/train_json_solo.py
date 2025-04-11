import os
import json
from .train_jsonit import (trainyolo, trainfcn,trainEfficientNet,
                           export_fcn,export_yolo,export_efficient,
                           testimage_fcn,testimage_yolo)
from .othermodules import CaseInsensitiveDict

def yoloit_train(alljsondir,aimode=None):
    with open(alljsondir, 'r',encoding='utf-8', errors='ignore') as f:
        TrainParams = json.load(f)
    # 在加载后立即添加这一行:
    TrainParams = CaseInsensitiveDict(TrainParams)
    modeltype = TrainParams['modeltype']
    datadir=None
    ###是否进行训练
    if modeltype=='yolo':
        YOLOParams=TrainParams['YOLOParams']
        modeldir, weightdir,yaml_datadir = trainyolo(YOLOParams,datadir=datadir if datadir else YOLOParams["datadir"])
        # modeldir, weightdir = trainyolo(datadir=datadir,
        #                                 modelpath=modelpath,
        #                                 epochs=epochs, batch=batch,
        #                                 workers=workers,
        #                                 amp=amp,
        #                                 imgsz=imgsz,
        #                                 patience=patience,
        #                                 device=device,
        #                                 resume=resume)
    if modeltype == 'fcn':
        FCNParams = TrainParams['FCNParams']
        modeldir=trainfcn(FCNParams)

    if modeltype == 'efficient':
        EfficientNetParams = TrainParams['EfficientNetParams']
        modeldir=trainEfficientNet(EfficientNetParams)

def yoloit_export(alljsondir,aimode=None):
    with open(alljsondir, 'r',encoding='utf-8', errors='ignore') as f:
        Allparams = json.load(f)
    # 在加载后立即添加这一行:
    ExportParams= CaseInsensitiveDict(Allparams)
    modeltype = ExportParams['modeltype']

    datadir=None
    modeldir, weightdir,yaml_datadir=None,None,None

    if modeltype == 'yolo':
        ExportParams=ExportParams["ExportParams_YOLO"]
        export_yolo(ExportParams,model_path=modeldir if modeldir else ExportParams["model_to_export"])
        weightdir_export=weightdir if weightdir else os.path.dirname(ExportParams["model_to_export"])
        exportmodel_format=ExportParams["export_format"]
    if modeltype == 'fcn':
        ExportParams = ExportParams["ExportParams_FCN"]
        # export_fcn(FCNParams, ExportParams, model_path=modeldir)
        export_fcn(ExportParams,model_path=modeldir if modeldir else ExportParams["model_to_export"])
        weightdir_export = os.path.dirname(modeldir) if modeldir else os.path.dirname(ExportParams["model_to_export"])
        exportmodel_format = ExportParams["export_format"]
        #######继续修改，怎么导出########
    if modeltype == 'efficient':
        ExportParams = ExportParams["ExportParams_EfficientNet"]
        # export_efficient(EfficientNetParams, ExportParams, model_path=modeldir)
        export_efficient(ExportParams,model_path=modeldir if modeldir else ExportParams["model_to_export"])#######继续修改，怎么导出########

def yoloit_test(alljsondir,aimode=None):
    with open(alljsondir, 'r',encoding='utf-8', errors='ignore') as f:
        TestParams = json.load(f)
    # 在加载后立即添加这一行:
    TestParams = CaseInsensitiveDict(TestParams)
    modeltype = TestParams['modeltype']
    datadir=None
    modeldir, weightdir,yaml_datadir=None,None,None
    weightdir_export=None
    exportmodel_format = None
    ###是否进行测试
    if modeltype == 'yolo':
        TestParams = TestParams["TestParams_YOLO"]
        # testimage(cur_path=inferedimg, infermodeldir=weightdir_export if weightdir_export else params["infermodeldir"],
        #           testimgpath=testimg, format=format)
        ##如果训练时输出test图片的路径就放在训练输出一起，训练参数还需要添加一个“da_testimg”:true/false,如果json文件没有这个关键词，默认为True
        if weightdir:
            test_oudir=os.path.join(os.path.dirname(weightdir),'test')
            if not os.path.exists(test_oudir):
                os.makedirs(test_oudir)
            autolabel_dir = os.path.join(test_oudir, 'autolabel')
            inferedimg_dir=os.path.join(test_oudir, 'inferedimg')
            if not os.path.exists(autolabel_dir):
                os.makedirs(autolabel_dir)
            if not os.path.exists(inferedimg_dir):
                os.makedirs(inferedimg_dir)
            TestParams["resultjson_path"]=autolabel_dir
            TestParams["inferedimg"] = inferedimg_dir
        ##如果训练时输出test图片的路径就放在训练输出一起
        testimage_yolo(TestParams,yaml_datadir,infermodeldir=weightdir_export if weightdir_export else TestParams["infermodeldir"],testformat=exportmodel_format if exportmodel_format else TestParams["infer_format"])

    if modeltype == 'fcn':
        TestParams = TestParams["TestParams_FCN"]
        testimage_fcn(TestParams,
                      infermodeldir=weightdir_export if weightdir_export else TestParams["infermodeldir"],
                      testformat=exportmodel_format if exportmodel_format else TestParams["infer_format"])
    if modeltype == 'efficient':
        print('efficient test not support now!! to developing')