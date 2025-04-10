# RSProduction MachineLearning

This project provides some usefull machine learning functionality.

# Table of Contents

- [1 dataset](#1-dataset)
  - [1.1 HMDB51 : torch.utils.data.dataset.Dataset](#11-hmdb51--torchutilsdatadatasetdataset)
    - [1.1.1 \_\_init\_\_](#111-\_\_init\_\_)
  - [1.2 Kinetics : torch.utils.data.dataset.Dataset](#12-kinetics--torchutilsdatadatasetdataset)
    - [1.2.1 \_\_init\_\_](#121-\_\_init\_\_)
  - [1.3 TUCHRI : torch.utils.data.dataset.Dataset](#13-tuchri--torchutilsdatadatasetdataset)
    - [1.3.1 \_\_init\_\_](#131-\_\_init\_\_)
    - [1.3.2 get\_uniform\_sampler](#132-get\_uniform\_sampler)
    - [1.3.3 load\_backgrounds](#133-load\_backgrounds)
  - [1.4 TUCRID : torch.utils.data.dataset.Dataset](#14-tucrid--torchutilsdatadatasetdataset)
    - [1.4.1 \_\_init\_\_](#141-\_\_init\_\_)
    - [1.4.2 get\_uniform\_sampler](#142-get\_uniform\_sampler)
    - [1.4.3 load\_backgrounds](#143-load\_backgrounds)
  - [1.5 UCF101 : torch.utils.data.dataset.Dataset](#15-ucf101--torchutilsdatadatasetdataset)
    - [1.5.1 \_\_init\_\_](#151-\_\_init\_\_)
  - [1.6 UTKinectAction3D : torch.utils.data.dataset.Dataset](#16-utkinectaction3d--torchutilsdatadatasetdataset)
    - [1.6.1 \_\_init\_\_](#161-\_\_init\_\_)
- [2 metrics](#2-metrics)
  - [2.1 AUROC](#21-auroc)
  - [2.2 F1\_Score](#22-f1\_score)
  - [2.3 FN](#23-fn)
  - [2.4 FP](#24-fp)
  - [2.5 FPR](#25-fpr)
  - [2.6 ROC](#26-roc)
  - [2.7 TN](#27-tn)
  - [2.8 TP](#28-tp)
  - [2.9 TPR](#29-tpr)
  - [2.10 confusion\_matrix](#210-confusion\_matrix)
  - [2.11 plot\_ROC](#211-plot\_roc)
  - [2.12 plot\_confusion\_matrix](#212-plot\_confusion\_matrix)
  - [2.13 precision](#213-precision)
  - [2.14 recall](#214-recall)
  - [2.15 top\_10\_accuracy](#215-top\_10\_accuracy)
  - [2.16 top\_1\_accuracy](#216-top\_1\_accuracy)
  - [2.17 top\_2\_accuracy](#217-top\_2\_accuracy)
  - [2.18 top\_3\_accuracy](#218-top\_3\_accuracy)
  - [2.19 top\_5\_accuracy](#219-top\_5\_accuracy)
  - [2.20 top\_k\_accuracy](#220-top\_k\_accuracy)
- [3 model](#3-model)
  - [3.1 MODELS : enum.Enum](#31-models--enumenum)
  - [3.2 WEIGHTS : enum.Enum](#32-weights--enumenum)
  - [3.3 list\_model\_weights](#33-list\_model\_weights)
  - [3.4 load\_model](#34-load\_model)
  - [3.5 publish\_model](#35-publish\_model)
- [4 module](#4-module)
  - [4.1 MultiHeadSelfAttention : torch.nn.modules.module.Module](#41-multiheadselfattention--torchnnmodulesmodulemodule)
        - [4.1.1 \_wrapped\_call\_impl](#411-\_wrapped\_call\_impl)
    - [4.1.2 \_\_init\_\_](#412-\_\_init\_\_)
        - [4.1.3 \_apply](#413-\_apply)
        - [4.1.4 \_call\_impl](#414-\_call\_impl)
        - [4.1.5 \_get\_backward\_hooks](#415-\_get\_backward\_hooks)
        - [4.1.6 \_get\_backward\_pre\_hooks](#416-\_get\_backward\_pre\_hooks)
        - [4.1.7 \_get\_name](#417-\_get\_name)
        - [4.1.8 \_load\_from\_state\_dict](#418-\_load\_from\_state\_dict)
        - [4.1.9 \_maybe\_warn\_non\_full\_backward\_hook](#419-\_maybe\_warn\_non\_full\_backward\_hook)
        - [4.1.10 \_named\_members](#4110-\_named\_members)
        - [4.1.11 \_register\_load\_state\_dict\_pre\_hook](#4111-\_register\_load\_state\_dict\_pre\_hook)
        - [4.1.12 \_register\_state\_dict\_hook](#4112-\_register\_state\_dict\_hook)
        - [4.1.13 \_replicate\_for\_data\_parallel](#4113-\_replicate\_for\_data\_parallel)
        - [4.1.14 \_save\_to\_state\_dict](#4114-\_save\_to\_state\_dict)
        - [4.1.15 \_slow\_forward](#4115-\_slow\_forward)
        - [4.1.16 \_wrapped\_call\_impl](#4116-\_wrapped\_call\_impl)
        - [4.1.17 add\_module](#4117-add\_module)
        - [4.1.18 apply](#4118-apply)
        - [4.1.19 bfloat16](#4119-bfloat16)
        - [4.1.20 buffers](#4120-buffers)
- [  >>> # xdoctest: +SKIP("undefined vars")](#-->>>-#-xdoctest--+skip("undefined-vars"))
        - [4.1.21 children](#4121-children)
        - [4.1.22 compile](#4122-compile)
        - [4.1.23 cpu](#4123-cpu)
        - [4.1.24 cuda](#4124-cuda)
        - [4.1.25 double](#4125-double)
        - [4.1.26 eval](#4126-eval)
        - [4.1.27 extra\_repr](#4127-extra\_repr)
        - [4.1.28 float](#4128-float)
    - [4.1.29 forward](#4129-forward)
        - [4.1.30 get\_buffer](#4130-get\_buffer)
        - [4.1.31 get\_extra\_state](#4131-get\_extra\_state)
        - [4.1.32 get\_parameter](#4132-get\_parameter)
        - [4.1.33 get\_submodule](#4133-get\_submodule)
        - [4.1.34 half](#4134-half)
        - [4.1.35 ipu](#4135-ipu)
        - [4.1.36 load\_state\_dict](#4136-load\_state\_dict)
        - [4.1.37 modules](#4137-modules)
        - [4.1.38 mtia](#4138-mtia)
        - [4.1.39 named\_buffers](#4139-named\_buffers)
- [  >>> # xdoctest: +SKIP("undefined vars")](#-->>>-#-xdoctest--+skip("undefined-vars"))
        - [4.1.40 named\_children](#4140-named\_children)
- [  >>> # xdoctest: +SKIP("undefined vars")](#-->>>-#-xdoctest--+skip("undefined-vars"))
        - [4.1.41 named\_modules](#4141-named\_modules)
        - [4.1.42 named\_parameters](#4142-named\_parameters)
- [  >>> # xdoctest: +SKIP("undefined vars")](#-->>>-#-xdoctest--+skip("undefined-vars"))
        - [4.1.43 parameters](#4143-parameters)
- [  >>> # xdoctest: +SKIP("undefined vars")](#-->>>-#-xdoctest--+skip("undefined-vars"))
        - [4.1.44 register\_backward\_hook](#4144-register\_backward\_hook)
        - [4.1.45 register\_buffer](#4145-register\_buffer)
- [  >>> # xdoctest: +SKIP("undefined vars")](#-->>>-#-xdoctest--+skip("undefined-vars"))
        - [4.1.46 register\_forward\_hook](#4146-register\_forward\_hook)
        - [4.1.47 register\_forward\_pre\_hook](#4147-register\_forward\_pre\_hook)
        - [4.1.48 register\_full\_backward\_hook](#4148-register\_full\_backward\_hook)
        - [4.1.49 register\_full\_backward\_pre\_hook](#4149-register\_full\_backward\_pre\_hook)
        - [4.1.50 register\_load\_state\_dict\_post\_hook](#4150-register\_load\_state\_dict\_post\_hook)
        - [4.1.51 register\_load\_state\_dict\_pre\_hook](#4151-register\_load\_state\_dict\_pre\_hook)
- [  hook(module, state_dict, prefix, local_metadata, strict, missing_keys, unexpected_keys, error_msgs) -> None  # noqa: B950](#--hook(module,-state_dict,-prefix,-local_metadata,-strict,-missing_keys,-unexpected_keys,-error_msgs)-->-none--#-noqa--b950)
        - [4.1.52 register\_module](#4152-register\_module)
        - [4.1.53 register\_parameter](#4153-register\_parameter)
        - [4.1.54 register\_state\_dict\_post\_hook](#4154-register\_state\_dict\_post\_hook)
        - [4.1.55 register\_state\_dict\_pre\_hook](#4155-register\_state\_dict\_pre\_hook)
        - [4.1.56 requires\_grad\_](#4156-requires\_grad\_)
        - [4.1.57 set\_extra\_state](#4157-set\_extra\_state)
        - [4.1.58 set\_submodule](#4158-set\_submodule)
        - [4.1.59 share\_memory](#4159-share\_memory)
        - [4.1.60 state\_dict](#4160-state\_dict)
- [  >>> # xdoctest: +SKIP("undefined vars")](#-->>>-#-xdoctest--+skip("undefined-vars"))
        - [4.1.61 to](#4161-to)
- [  >>> # xdoctest: +IGNORE_WANT("non-deterministic")](#-->>>-#-xdoctest--+ignore_want("non-deterministic"))
- [  >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_CUDA1)](#-->>>-#-xdoctest--+requires(env-torch_doctest_cuda1))
        - [4.1.62 to\_empty](#4162-to\_empty)
        - [4.1.63 train](#4163-train)
        - [4.1.64 type](#4164-type)
        - [4.1.65 xpu](#4165-xpu)
        - [4.1.66 zero\_grad](#4166-zero\_grad)
  - [4.2 SelfAttention : torch.nn.modules.module.Module](#42-selfattention--torchnnmodulesmodulemodule)
        - [4.2.1 \_wrapped\_call\_impl](#421-\_wrapped\_call\_impl)
    - [4.2.2 \_\_init\_\_](#422-\_\_init\_\_)
        - [4.2.3 \_apply](#423-\_apply)
        - [4.2.4 \_call\_impl](#424-\_call\_impl)
        - [4.2.5 \_get\_backward\_hooks](#425-\_get\_backward\_hooks)
        - [4.2.6 \_get\_backward\_pre\_hooks](#426-\_get\_backward\_pre\_hooks)
        - [4.2.7 \_get\_name](#427-\_get\_name)
        - [4.2.8 \_load\_from\_state\_dict](#428-\_load\_from\_state\_dict)
        - [4.2.9 \_maybe\_warn\_non\_full\_backward\_hook](#429-\_maybe\_warn\_non\_full\_backward\_hook)
        - [4.2.10 \_named\_members](#4210-\_named\_members)
        - [4.2.11 \_register\_load\_state\_dict\_pre\_hook](#4211-\_register\_load\_state\_dict\_pre\_hook)
        - [4.2.12 \_register\_state\_dict\_hook](#4212-\_register\_state\_dict\_hook)
        - [4.2.13 \_replicate\_for\_data\_parallel](#4213-\_replicate\_for\_data\_parallel)
        - [4.2.14 \_save\_to\_state\_dict](#4214-\_save\_to\_state\_dict)
        - [4.2.15 \_slow\_forward](#4215-\_slow\_forward)
        - [4.2.16 \_wrapped\_call\_impl](#4216-\_wrapped\_call\_impl)
        - [4.2.17 add\_module](#4217-add\_module)
        - [4.2.18 apply](#4218-apply)
        - [4.2.19 bfloat16](#4219-bfloat16)
        - [4.2.20 buffers](#4220-buffers)
- [  >>> # xdoctest: +SKIP("undefined vars")](#-->>>-#-xdoctest--+skip("undefined-vars"))
        - [4.2.21 children](#4221-children)
        - [4.2.22 compile](#4222-compile)
        - [4.2.23 cpu](#4223-cpu)
        - [4.2.24 cuda](#4224-cuda)
        - [4.2.25 double](#4225-double)
        - [4.2.26 eval](#4226-eval)
        - [4.2.27 extra\_repr](#4227-extra\_repr)
        - [4.2.28 float](#4228-float)
    - [4.2.29 forward](#4229-forward)
        - [4.2.30 get\_buffer](#4230-get\_buffer)
        - [4.2.31 get\_extra\_state](#4231-get\_extra\_state)
        - [4.2.32 get\_parameter](#4232-get\_parameter)
        - [4.2.33 get\_submodule](#4233-get\_submodule)
        - [4.2.34 half](#4234-half)
        - [4.2.35 ipu](#4235-ipu)
        - [4.2.36 load\_state\_dict](#4236-load\_state\_dict)
        - [4.2.37 modules](#4237-modules)
        - [4.2.38 mtia](#4238-mtia)
        - [4.2.39 named\_buffers](#4239-named\_buffers)
- [  >>> # xdoctest: +SKIP("undefined vars")](#-->>>-#-xdoctest--+skip("undefined-vars"))
        - [4.2.40 named\_children](#4240-named\_children)
- [  >>> # xdoctest: +SKIP("undefined vars")](#-->>>-#-xdoctest--+skip("undefined-vars"))
        - [4.2.41 named\_modules](#4241-named\_modules)
        - [4.2.42 named\_parameters](#4242-named\_parameters)
- [  >>> # xdoctest: +SKIP("undefined vars")](#-->>>-#-xdoctest--+skip("undefined-vars"))
        - [4.2.43 parameters](#4243-parameters)
- [  >>> # xdoctest: +SKIP("undefined vars")](#-->>>-#-xdoctest--+skip("undefined-vars"))
        - [4.2.44 register\_backward\_hook](#4244-register\_backward\_hook)
        - [4.2.45 register\_buffer](#4245-register\_buffer)
- [  >>> # xdoctest: +SKIP("undefined vars")](#-->>>-#-xdoctest--+skip("undefined-vars"))
        - [4.2.46 register\_forward\_hook](#4246-register\_forward\_hook)
        - [4.2.47 register\_forward\_pre\_hook](#4247-register\_forward\_pre\_hook)
        - [4.2.48 register\_full\_backward\_hook](#4248-register\_full\_backward\_hook)
        - [4.2.49 register\_full\_backward\_pre\_hook](#4249-register\_full\_backward\_pre\_hook)
        - [4.2.50 register\_load\_state\_dict\_post\_hook](#4250-register\_load\_state\_dict\_post\_hook)
        - [4.2.51 register\_load\_state\_dict\_pre\_hook](#4251-register\_load\_state\_dict\_pre\_hook)
- [  hook(module, state_dict, prefix, local_metadata, strict, missing_keys, unexpected_keys, error_msgs) -> None  # noqa: B950](#--hook(module,-state_dict,-prefix,-local_metadata,-strict,-missing_keys,-unexpected_keys,-error_msgs)-->-none--#-noqa--b950)
        - [4.2.52 register\_module](#4252-register\_module)
        - [4.2.53 register\_parameter](#4253-register\_parameter)
        - [4.2.54 register\_state\_dict\_post\_hook](#4254-register\_state\_dict\_post\_hook)
        - [4.2.55 register\_state\_dict\_pre\_hook](#4255-register\_state\_dict\_pre\_hook)
        - [4.2.56 requires\_grad\_](#4256-requires\_grad\_)
        - [4.2.57 set\_extra\_state](#4257-set\_extra\_state)
        - [4.2.58 set\_submodule](#4258-set\_submodule)
        - [4.2.59 share\_memory](#4259-share\_memory)
        - [4.2.60 state\_dict](#4260-state\_dict)
- [  >>> # xdoctest: +SKIP("undefined vars")](#-->>>-#-xdoctest--+skip("undefined-vars"))
        - [4.2.61 to](#4261-to)
- [  >>> # xdoctest: +IGNORE_WANT("non-deterministic")](#-->>>-#-xdoctest--+ignore_want("non-deterministic"))
- [  >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_CUDA1)](#-->>>-#-xdoctest--+requires(env-torch_doctest_cuda1))
        - [4.2.62 to\_empty](#4262-to\_empty)
        - [4.2.63 train](#4263-train)
        - [4.2.64 type](#4264-type)
        - [4.2.65 xpu](#4265-xpu)
        - [4.2.66 zero\_grad](#4266-zero\_grad)
- [5 multi\_transforms](#5-multi\_transforms)
  - [5.1 BGR2GRAY : MultiTransform](#51-bgr2gray--multitransform)
    - [5.1.1 \_\_call\_\_](#511-\_\_call\_\_)
    - [5.1.2 \_\_init\_\_](#512-\_\_init\_\_)
  - [5.2 BGR2RGB : MultiTransform](#52-bgr2rgb--multitransform)
    - [5.2.1 \_\_call\_\_](#521-\_\_call\_\_)
    - [5.2.2 \_\_init\_\_](#522-\_\_init\_\_)
  - [5.3 Brightness : MultiTransform](#53-brightness--multitransform)
    - [5.3.1 \_\_call\_\_](#531-\_\_call\_\_)
    - [5.3.2 \_\_init\_\_](#532-\_\_init\_\_)
  - [5.4 CenterCrop : MultiTransform](#54-centercrop--multitransform)
    - [5.4.1 \_\_call\_\_](#541-\_\_call\_\_)
    - [5.4.2 \_\_init\_\_](#542-\_\_init\_\_)
  - [5.5 Color : MultiTransform](#55-color--multitransform)
    - [5.5.1 \_\_call\_\_](#551-\_\_call\_\_)
    - [5.5.2 \_\_init\_\_](#552-\_\_init\_\_)
  - [5.6 Compose : builtins.object](#56-compose--builtinsobject)
    - [5.6.1 \_\_call\_\_](#561-\_\_call\_\_)
    - [5.6.2 \_\_init\_\_](#562-\_\_init\_\_)
  - [5.7 GaussianNoise : MultiTransform](#57-gaussiannoise--multitransform)
    - [5.7.1 \_\_call\_\_](#571-\_\_call\_\_)
    - [5.7.2 \_\_init\_\_](#572-\_\_init\_\_)
  - [5.8 MultiTransform : builtins.object](#58-multitransform--builtinsobject)
    - [5.8.1 \_\_call\_\_](#581-\_\_call\_\_)
    - [5.8.2 \_\_init\_\_](#582-\_\_init\_\_)
  - [5.9 Normalize : MultiTransform](#59-normalize--multitransform)
    - [5.9.1 \_\_call\_\_](#591-\_\_call\_\_)
    - [5.9.2 \_\_init\_\_](#592-\_\_init\_\_)
  - [5.10 RGB2BGR : BGR2RGB](#510-rgb2bgr--bgr2rgb)
    - [5.10.1 \_\_call\_\_](#5101-\_\_call\_\_)
    - [5.10.2 \_\_init\_\_](#5102-\_\_init\_\_)
  - [5.11 RandomCrop : MultiTransform](#511-randomcrop--multitransform)
    - [5.11.1 \_\_call\_\_](#5111-\_\_call\_\_)
    - [5.11.2 \_\_init\_\_](#5112-\_\_init\_\_)
  - [5.12 RandomHorizontalFlip : MultiTransform](#512-randomhorizontalflip--multitransform)
    - [5.12.1 \_\_call\_\_](#5121-\_\_call\_\_)
    - [5.12.2 \_\_init\_\_](#5122-\_\_init\_\_)
  - [5.13 RandomVerticalFlip : MultiTransform](#513-randomverticalflip--multitransform)
    - [5.13.1 \_\_call\_\_](#5131-\_\_call\_\_)
    - [5.13.2 \_\_init\_\_](#5132-\_\_init\_\_)
  - [5.14 RemoveBackgroundAI : MultiTransform](#514-removebackgroundai--multitransform)
    - [5.14.1 \_\_call\_\_](#5141-\_\_call\_\_)
    - [5.14.2 \_\_init\_\_](#5142-\_\_init\_\_)
  - [5.15 ReplaceBackground : MultiTransform](#515-replacebackground--multitransform)
    - [5.15.1 \_\_call\_\_](#5151-\_\_call\_\_)
    - [5.15.2 \_\_init\_\_](#5152-\_\_init\_\_)
  - [5.16 Resize : MultiTransform](#516-resize--multitransform)
    - [5.16.1 \_\_call\_\_](#5161-\_\_call\_\_)
    - [5.16.2 \_\_init\_\_](#5162-\_\_init\_\_)
  - [5.17 Rotate : MultiTransform](#517-rotate--multitransform)
    - [5.17.1 \_\_call\_\_](#5171-\_\_call\_\_)
    - [5.17.2 \_\_init\_\_](#5172-\_\_init\_\_)
  - [5.18 Satturation : MultiTransform](#518-satturation--multitransform)
    - [5.18.1 \_\_call\_\_](#5181-\_\_call\_\_)
    - [5.18.2 \_\_init\_\_](#5182-\_\_init\_\_)
  - [5.19 Scale : MultiTransform](#519-scale--multitransform)
    - [5.19.1 \_\_call\_\_](#5191-\_\_call\_\_)
    - [5.19.2 \_\_init\_\_](#5192-\_\_init\_\_)
  - [5.20 Stack : MultiTransform](#520-stack--multitransform)
    - [5.20.1 \_\_call\_\_](#5201-\_\_call\_\_)
    - [5.20.2 \_\_init\_\_](#5202-\_\_init\_\_)
  - [5.21 ToCVImage : MultiTransform](#521-tocvimage--multitransform)
    - [5.21.1 \_\_call\_\_](#5211-\_\_call\_\_)
    - [5.21.2 \_\_init\_\_](#5212-\_\_init\_\_)
  - [5.22 ToNumpy : MultiTransform](#522-tonumpy--multitransform)
    - [5.22.1 \_\_call\_\_](#5221-\_\_call\_\_)
    - [5.22.2 \_\_init\_\_](#5222-\_\_init\_\_)
  - [5.23 ToPILImage : MultiTransform](#523-topilimage--multitransform)
    - [5.23.1 \_\_call\_\_](#5231-\_\_call\_\_)
    - [5.23.2 \_\_init\_\_](#5232-\_\_init\_\_)
  - [5.24 ToTensor : MultiTransform](#524-totensor--multitransform)
    - [5.24.1 \_\_call\_\_](#5241-\_\_call\_\_)
    - [5.24.2 \_\_init\_\_](#5242-\_\_init\_\_)
- [6 run](#6-run)
  - [6.1 Run : builtins.object](#61-run--builtinsobject)
    - [6.1.1 \_\_init\_\_](#611-\_\_init\_\_)
    - [6.1.2 append](#612-append)
    - [6.1.3 get\_avg](#613-get\_avg)
    - [6.1.4 get\_val](#614-get\_val)
    - [6.1.5 len](#615-len)
    - [6.1.6 load\_best\_state\_dict](#616-load\_best\_state\_dict)
    - [6.1.7 load\_state\_dict](#617-load\_state\_dict)
    - [6.1.8 pickle\_dump](#618-pickle\_dump)
    - [6.1.9 pickle\_load](#619-pickle\_load)
    - [6.1.10 plot](#6110-plot)
    - [6.1.11 recalculate\_moving\_average](#6111-recalculate\_moving\_average)
    - [6.1.12 save](#6112-save)
    - [6.1.13 save\_best\_state\_dict](#6113-save\_best\_state\_dict)
    - [6.1.14 save\_state\_dict](#6114-save\_state\_dict)
    - [6.1.15 train\_epoch](#6115-train\_epoch)
    - [6.1.16 validate\_epoch](#6116-validate\_epoch)




# 1 dataset

[TOC](#table-of-contents)



## 1.1 HMDB51 : torch.utils.data.dataset.Dataset

[TOC](#table-of-contents)

**Description**

Dataset class for HMDB51.

**Example**

```python
from rsp.ml.dataset import HMDB51
import rsp.ml.multi_transforms as multi_transforms
import cv2 as cv

transforms = multi_transforms.Compose([
    multi_transforms.Color(1.5, p=0.5),
    multi_transforms.Stack()
])
ds = HMDB51('train', fold=1, transforms=transforms)

for X, T in ds:
  for x in X.permute(0, 2, 3, 1):
    img_color = x[:, :, :3].numpy()
    img_depth = x[:, :, 3].numpy()

    cv.imshow('color', img_color)
    cv.imshow('depth', img_depth)

    cv.waitKey(30)
```
### 1.1.1 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| split | str | Dataset split [train|val|test] |
| fold | int | Fold number. The dataset is split into 3 folds. If fold is None, all folds will be loaded. |
| cache_dir | str, default = None | Directory to store the downloaded files. If set to `None`, the default cache directory will be used |
| force_reload | bool, default = False | If set to `True`, the dataset will be reloaded |
| target_size | (int, int), default = (400, 400) | Size of the frames. The frames will be resized to this size. |
| sequence_length | int, default = 30 | Length of the sequences |
| transforms | rsp.ml.multi_transforms.Compose = default = rsp.ml.multi_transforms.Compose([]) | Transformations, that will be applied to each input sequence. See documentation of `rsp.ml.multi_transforms` for more details. |
| verbose | bool, default = False | If set to `True`, the progress will be printed. |
## 1.2 Kinetics : torch.utils.data.dataset.Dataset

[TOC](#table-of-contents)

**Description**

Dataset class for the Kinetics dataset.

**Example**

```python
from rsp.ml.dataset import Kinetics

ds = Kinetics(split='train', type=400)

for X, T in ds:
    print(X)
```
### 1.2.1 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| split | str | Dataset split [train|val] |
| sequence_length | int, default = 60 | Length of the sequences |
| type | int, default = 400 | Type of the kineticts dataset. Currently only 400 is supported. |
| frame_size | (int, int), default = (400, 400) | Size of the frames. The frames will be resized to this size. |
| transforms | rsp.ml.multi_transforms.Compose = default = rsp.ml.multi_transforms.Compose([]) | Transformations, that will be applied to each input sequence. See documentation of `rsp.ml.multi_transforms` for more details. |
| cache_dir | str, default = None | Directory to store the downloaded files. If set to `None`, the default cache directory will be used |
| num_threads | int, default = 0 | Number of threads to use for downloading the files. |
| verbose | bool, default = True | If set to `True`, the progress and additional information will be printed. |
## 1.3 TUCHRI : torch.utils.data.dataset.Dataset

[TOC](#table-of-contents)

**Description**

Dataset class for the Robot Interaction Dataset by University of Technology Chemnitz (TUCHRI).


### 1.3.1 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| phase | str | Dataset phase [train|val] |
| load_depth_data | bool, default = True | Load depth data |
| sequence_length | int, default = 30 | Length of the sequences |
| num_classes | int, default = 10 | Number of classes |
| transforms | rsp.ml.multi_transforms.Compose = default = rsp.ml.multi_transforms.Compose([]) | Transformations, that will be applied to each input sequence. See documentation of `rsp.ml.multi_transforms` for more details. |
### 1.3.2 get\_uniform\_sampler

[TOC](#table-of-contents)

### 1.3.3 load\_backgrounds

[TOC](#table-of-contents)

**Description**

Loads the background images.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| load_depth_data | bool, default = True | If set to `True`, the depth images will be loaded as well. |
## 1.4 TUCRID : torch.utils.data.dataset.Dataset

[TOC](#table-of-contents)

**Description**

Dataset class for the Robot Interaction Dataset by University of Technology Chemnitz (TUCRID).

**Example**

```python
from rsp.ml.dataset import TUCRID
from rsp.ml.dataset import ReplaceBackgroundRGBD
import rsp.ml.multi_transforms as multi_transforms
import cv2 as cv

backgrounds = TUCRID.load_backgrounds_color()
transforms = multi_transforms.Compose([
    ReplaceBackgroundRGBD(backgrounds),
    multi_transforms.Stack()
])

ds = TUCRID('train', transforms=transforms)

for X, T in ds:
  for x in X.permute(0, 2, 3, 1):
    img_color = x[:, :, :3].numpy()
    img_depth = x[:, :, 3].numpy()

    cv.imshow('color', img_color)
    cv.imshow('depth', img_depth)

    cv.waitKey(30)
```
### 1.4.1 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| phase | str | Dataset phase [train|val] |
| load_depth_data | bool, default = True | Load depth data |
| sequence_length | int, default = 30 | Length of the sequences |
| num_classes | int, default = 10 | Number of classes |
| transforms | rsp.ml.multi_transforms.Compose = default = rsp.ml.multi_transforms.Compose([]) | Transformations, that will be applied to each input sequence. See documentation of `rsp.ml.multi_transforms` for more details. |
### 1.4.2 get\_uniform\_sampler

[TOC](#table-of-contents)

### 1.4.3 load\_backgrounds

[TOC](#table-of-contents)

**Description**

Loads the background images.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| load_depth_data | bool, default = True | If set to `True`, the depth images will be loaded as well. |
## 1.5 UCF101 : torch.utils.data.dataset.Dataset

[TOC](#table-of-contents)

**Description**

An abstract class representing a :class:`Dataset`.

All datasets that represent a map from keys to data samples should subclass
it. All subclasses should overwrite :meth:`__getitem__`, supporting fetching a
data sample for a given key. Subclasses could also optionally overwrite
:meth:`__len__`, which is expected to return the size of the dataset by many
:class:`~torch.utils.data.Sampler` implementations and the default options
of :class:`~torch.utils.data.DataLoader`. Subclasses could also
optionally implement :meth:`__getitems__`, for speedup batched samples
loading. This method accepts list of indices of samples of batch and returns
list of samples.

.. note::
  :class:`~torch.utils.data.DataLoader` by default constructs an index
  sampler that yields integral indices.  To make it work with a map-style
  dataset with non-integral indices/keys, a custom sampler must be provided.

**Example**

```python
from rsp.ml.dataset import UCF101
import rsp.ml.multi_transforms as multi_transforms
import cv2 as cv

transforms = multi_transforms.Compose([
    multi_transforms.Color(1.5, p=0.5),
    multi_transforms.Stack()
])
ds = UCF101('train', fold=1, transforms=transforms)

for X, T in ds:
  for x in X.permute(0, 2, 3, 1):
    img_color = x[:, :, :3].numpy()
    img_depth = x[:, :, 3].numpy()

    cv.imshow('color', img_color)
    cv.imshow('depth', img_depth)

    cv.waitKey(30)
```
### 1.5.1 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| split | str | Dataset split [train|val|test] |
| fold | int | Fold number. The dataset is split into 3 folds. If fold is None, all folds will be loaded. |
| cache_dir | str, default = None | Directory to store the downloaded files. If set to `None`, the default cache directory will be used |
| force_reload | bool, default = False | If set to `True`, the dataset will be reloaded |
| target_size | (int, int), default = (400, 400) | Size of the frames. The frames will be resized to this size. |
| sequence_length | int, default = 30 | Length of the sequences |
| transforms | rsp.ml.multi_transforms.Compose = default = rsp.ml.multi_transforms.Compose([]) | Transformations, that will be applied to each input sequence. See documentation of `rsp.ml.multi_transforms` for more details. |
| verbose | bool, default = False | If set to `True`, the progress will be printed. |
## 1.6 UTKinectAction3D : torch.utils.data.dataset.Dataset

[TOC](#table-of-contents)

**Description**

Dataset class for the UTKinectAction3D dataset.

Parameters
----------
split : str
    Dataset split [train|val]
cache_dir : str, default = None
    Directory to store the downloaded files. If set to `None`, the default cache directory will be used
force_reload : bool, default = False
    If set to `True`, the dataset will be reloaded
target_size : (int, int), default = (400, 400)
    Size of the frames. The frames will be resized to this size.
sequence_length : int, default = 30
    Length of the sequences
transforms : rsp.ml.multi_transforms.Compose = default = rsp.ml.multi_transforms.Compose([])
    Transformations, that will be applied to each input sequence. See documentation of `rsp.ml.multi_transforms` for more details.
verbose : bool, default = False
    If set to `True`, the progress will be printed.

**Example**

```python
from rsp.ml.dataset import UTKinectAction3D
import rsp.ml.multi_transforms as multi_transforms
import cv2 as cv

transforms = multi_transforms.Compose([
    multi_transforms.Color(1.5, p=0.5),
    multi_transforms.Stack()
])
ds = UTKinectAction3D('train', transforms=transforms)

for X, T in ds:
  for x in X.permute(0, 2, 3, 1):
    img_color = x[:, :, :3].numpy()
    img_depth = x[:, :, 3].numpy()

    cv.imshow('color', img_color)
    cv.imshow('depth', img_depth)

    cv.waitKey(30)
```
### 1.6.1 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initialize self.  See help(type(self)) for accurate signature.

# 2 metrics

[TOC](#table-of-contents)

The module `rsp.ml.metrics` provides some functionality to quantify the quality of predictions.

## 2.1 AUROC

[TOC](#table-of-contents)

**Description**

Calculates the Area under the Receiver Operation Chracteristic Curve.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| num_thresholds | int, default = 100 | Number of thresholds to compute. |

**Returns**

Receiver Operation Chracteristic Area under the Curve : float

## 2.2 F1\_Score

[TOC](#table-of-contents)

**Description**

F1 Score. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

F1 Score : float

**Equations**

$precision = \frac{TP}{TP + FP}$

$recall = \frac{TP}{TP + FN}$

$F_1 = \frac{2 \cdot precision \cdot recall}{precision + recall} = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}$



**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

f1score = m.F1_Score(Y, T)

print(f1score) --> 0.5
```

## 2.3 FN

[TOC](#table-of-contents)

**Description**

False negatives. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

False negatives : int

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

fn = m.FN(Y, T)
print(fn) -> 1
```

## 2.4 FP

[TOC](#table-of-contents)

**Description**

False positives. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

False positives : int

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

fp = m.FP(Y, T)
print(fp) -> 1
```

## 2.5 FPR

[TOC](#table-of-contents)

**Description**

False positive rate. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

False positive rate : float

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

fpr = m.FPR(Y, T)
print(fpr) -> 0.08333333333333333
```

## 2.6 ROC

[TOC](#table-of-contents)

**Description**

Calculates the receiver operating characteristic: computes False Positive Rates and True positive Rates for `num_thresholds` aligned between 0 and 1

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| num_thresholds | int, default = 100 | Number of thresholds to compute. |

**Returns**

(False Positive Rates, True Positive Rates) for 100 different thresholds : (List[float], List[float])

**Example**

```python
import rsp.ml.metrics as m
import torch
import torch.nn.functional as F

num_elements = 100000
num_classes = 7

T = []
for i in range(num_elements):
  true_class = torch.randint(0, num_classes, (1,))
  t = F.one_hot(true_class, num_classes=num_classes)
  T.append(t)
T = torch.cat(T)

dist = torch.normal(T.float(), 1.5)
Y = F.softmax(dist, dim = 1)
FPRs, TPRs = m.ROC(Y, T)
```

## 2.7 TN

[TOC](#table-of-contents)

**Description**

True negatives. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

True negatives : int

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

tn = m.TN(Y, T)
print(tn) -> 11
```

## 2.8 TP

[TOC](#table-of-contents)

**Description**

True positives. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

True positives : int

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

tp = m.TP(Y, T)
print(tp) -> 5
```

## 2.9 TPR

[TOC](#table-of-contents)

**Description**

True positive rate. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

True positive rate : float

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

tpr = m.TPR(Y, T)
print(tpr) -> 0.8333333333333334
```

## 2.10 confusion\_matrix

[TOC](#table-of-contents)

**Description**

Calculates the confusion matrix. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Confusion matrix : torch.Tensor

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

conf_mat = m.confusion_matrix(Y, T)
print(conf_mat) -> tensor([
  [1, 1, 0],
  [0, 2, 0],
  [0, 0, 2]
])
```

## 2.11 plot\_ROC

[TOC](#table-of-contents)

**Description**

Plot the receiver operating characteristic.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| num_thresholds | int, default = 100 | Number of thresholds to compute. |
| title | str, optional, default = 'Confusion Matrix' | Title of the plot |
| class_curves | bool, default = False | Plot ROC curve for each class |
| labels | str, optional, default = None | Class labels -> automatic labeling C000, ..., CXXX if labels is None |
| plt_show | bool, optional, default = False | Set to True to show the plot |
| save_file_name | str, optional, default = None | If not None, the plot is saved under the specified save_file_name. |

**Returns**

Image of the confusion matrix : np.array

![](documentation/image/ROC_AUC.jpg)
## 2.12 plot\_confusion\_matrix

[TOC](#table-of-contents)

**Description**

Plot the confusion matrix

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| confusion_matrix | torch.Tensor | Confusion matrix |
| labels | str, optional, default = None | Class labels -> automatic labeling C000, ..., CXXX if labels is None |
| cmap | str, optional, default = 'Blues' | Seaborn cmap, see https://r02b.github.io/seaborn_palettes/ |
| xlabel | str, optional, default = 'Predicted label' | X-Axis label |
| ylabel | str, optional, default = 'True label' | Y-Axis label |
| title | str, optional, default = 'Confusion Matrix' | Title of the plot |
| plt_show | bool, optional, default = False | Set to True to show the plot |
| save_file_name | str, optional, default = None | If not None, the plot is saved under the specified save_file_name. |

**Returns**

Image of the confusion matrix : np.array

![](documentation/image/confusion_matrix.jpg)
## 2.13 precision

[TOC](#table-of-contents)

**Description**

Precision. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

Precision : float

**Equations**

$precision = \frac{TP}{TP + FP}$



**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

precision = m.precision(Y, T)
print(precision) -> 0.8333333333333334
```

## 2.14 recall

[TOC](#table-of-contents)

**Description**

Recall. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

Recall : float

**Equations**

$recall = \frac{TP}{TP + FN}$



**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

recall = m.recall(Y, T)
print(recall) -> 0.8333333333333334
```

## 2.15 top\_10\_accuracy

[TOC](#table-of-contents)

**Description**

Top 10 accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top 10 accuracy -> top k accuracy | k = 10 : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_10_accuracy = m.top_10_accuracy(Y, T, k = 3)

print(top_10_accuracy) --> 1.0
```

## 2.16 top\_1\_accuracy

[TOC](#table-of-contents)

**Description**

Top 1 accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top 1 accuracy -> top k accuracy | k = 1 : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_1_accuracy = m.top_1_accuracy(Y, T, k = 3)

print(top_1_accuracy) --> 0.8333333333333334
```

## 2.17 top\_2\_accuracy

[TOC](#table-of-contents)

**Description**

Top 2 accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top 2 accuracy -> top k accuracy | k = 2 : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_2_accuracy = m.top_2_accuracy(Y, T, k = 3)

print(top_2_accuracy) --> 1.0
```

## 2.18 top\_3\_accuracy

[TOC](#table-of-contents)

**Description**

Top 3 accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top 3 accuracy -> top k accuracy | k = 3 : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_3_accuracy = m.top_3_accuracy(Y, T, k = 3)

print(top_3_accuracy) --> 1.0
```

## 2.19 top\_5\_accuracy

[TOC](#table-of-contents)

**Description**

Top 5 accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top 5 accuracy -> top k accuracy | k = 5 : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_5_accuracy = m.top_5_accuracy(Y, T, k = 3)

print(top_5_accuracy) --> 1.0
```

## 2.20 top\_k\_accuracy

[TOC](#table-of-contents)

**Description**

Top k accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top k accuracy : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_k_accuracy = m.top_k_accuracy(Y, T, k = 3)

print(top_k_accuracy) --> 1.0
```

# 3 model

[TOC](#table-of-contents)

The module `rsp.ml.model` provides some usefull functionality to store and load pytorch models.

## 3.1 MODELS : enum.Enum

[TOC](#table-of-contents)

**Description**

Create a collection of name/value pairs.

Example enumeration:

>>> class Color(Enum):
...     RED = 1
...     BLUE = 2
...     GREEN = 3

Access them by:

- attribute access::

>>> Color.RED
<Color.RED: 1>

- value lookup:

>>> Color(1)
<Color.RED: 1>

- name lookup:

>>> Color['RED']
<Color.RED: 1>

Enumerations can be iterated over, and know how many members they have:

>>> len(Color)
3

>>> list(Color)
[<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]

Methods can be added to enumerations, and members can have their own
attributes -- see the documentation for details.


## 3.2 WEIGHTS : enum.Enum

[TOC](#table-of-contents)

**Description**

Create a collection of name/value pairs.

Example enumeration:

>>> class Color(Enum):
...     RED = 1
...     BLUE = 2
...     GREEN = 3

Access them by:

- attribute access::

>>> Color.RED
<Color.RED: 1>

- value lookup:

>>> Color(1)
<Color.RED: 1>

- name lookup:

>>> Color['RED']
<Color.RED: 1>

Enumerations can be iterated over, and know how many members they have:

>>> len(Color)
3

>>> list(Color)
[<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]

Methods can be added to enumerations, and members can have their own
attributes -- see the documentation for details.


## 3.3 list\_model\_weights

[TOC](#table-of-contents)

**Description**

Lists all available weight files.


**Returns**

List of (MODEL:str, WEIGHT:str) : List[Tuple(str, str)]

**Example**

```python
import rsp.ml.model as model

model_weight_files = model.list_model_weights()
```

## 3.4 load\_model

[TOC](#table-of-contents)

**Description**

Loads a pretrained PyTorch model from HuggingFace.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| model | MODELS | ID of the model |
| weights | WEIGHTS | ID of the weights |

**Returns**

Pretrained PyTorch model : torch.nn.Module

**Example**

```python
import rsp.ml.model as model

action_recognition_model = model.load_model(MODEL.TUCARC3D, WEIGHTS.TUCAR)
```

## 3.5 publish\_model

[TOC](#table-of-contents)

# 4 module

[TOC](#table-of-contents)



## 4.1 MultiHeadSelfAttention : torch.nn.modules.module.Module

[TOC](#table-of-contents)

**Description**

Base class for all neural network modules.

Your models should also subclass this class.

Modules can also contain other Modules, allowing them to be nested in
a tree structure. You can assign the submodules as regular attributes::

    import torch.nn as nn
    import torch.nn.functional as F

    class Model(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.conv1 = nn.Conv2d(1, 20, 5)
            self.conv2 = nn.Conv2d(20, 20, 5)

        def forward(self, x):
            x = F.relu(self.conv1(x))
            return F.relu(self.conv2(x))

Submodules assigned in this way will be registered, and will also have their
parameters converted when you call :meth:`to`, etc.

.. note::
    As per the example above, an ``__init__()`` call to the parent class
    must be made before assignment on the child.

:ivar training: Boolean represents whether this module is in training or
                evaluation mode.
:vartype training: bool


##### 4.1.1 \_wrapped\_call\_impl

[TOC](#table-of-contents)

### 4.1.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initialize internal Module state, shared by both nn.Module and ScriptModule.

##### 4.1.3 \_apply

[TOC](#table-of-contents)

##### 4.1.4 \_call\_impl

[TOC](#table-of-contents)

##### 4.1.5 \_get\_backward\_hooks

[TOC](#table-of-contents)

**Description**

Return the backward hooks for use in the call function.

It returns two lists, one with the full backward hooks and one with the non-full

backward hooks.

##### 4.1.6 \_get\_backward\_pre\_hooks

[TOC](#table-of-contents)

##### 4.1.7 \_get\_name

[TOC](#table-of-contents)

##### 4.1.8 \_load\_from\_state\_dict

[TOC](#table-of-contents)

**Description**

Copy parameters and buffers from :attr:`state_dict` into only this module, but not its descendants.

This is called on every submodule

in :meth:`~torch.nn.Module.load_state_dict`. Metadata saved for this

module in input :attr:`state_dict` is provided as :attr:`local_metadata`.

For state dicts without metadata, :attr:`local_metadata` is empty.

Subclasses can achieve class-specific backward compatible loading using

the version number at `local_metadata.get("version", None)`.

Additionally, :attr:`local_metadata` can also contain the key

`assign_to_params_buffers` that indicates whether keys should be

assigned their corresponding tensor in the state_dict.

.. note::

    :attr:`state_dict` is not the same object as the input

    :attr:`state_dict` to :meth:`~torch.nn.Module.load_state_dict`. So

    it can be modified.

Args:

    state_dict (dict): a dict containing parameters and

        persistent buffers.

    prefix (str): the prefix for parameters and buffers used in this

        module

    local_metadata (dict): a dict containing the metadata for this module.

        See

    strict (bool): whether to strictly enforce that the keys in

        :attr:`state_dict` with :attr:`prefix` match the names of

        parameters and buffers in this module

    missing_keys (list of str): if ``strict=True``, add missing keys to

        this list

    unexpected_keys (list of str): if ``strict=True``, add unexpected

        keys to this list

    error_msgs (list of str): error messages should be added to this

        list, and will be reported together in

        :meth:`~torch.nn.Module.load_state_dict`

##### 4.1.9 \_maybe\_warn\_non\_full\_backward\_hook

[TOC](#table-of-contents)

##### 4.1.10 \_named\_members

[TOC](#table-of-contents)

**Description**

Help yield various names + members of modules.

##### 4.1.11 \_register\_load\_state\_dict\_pre\_hook

[TOC](#table-of-contents)

**Description**

See :meth:`~torch.nn.Module.register_load_state_dict_pre_hook` for details.

A subtle difference is that if ``with_module`` is set to ``False``, then the

hook will not take the ``module`` as the first argument whereas

:meth:`~torch.nn.Module.register_load_state_dict_pre_hook` always takes the

``module`` as the first argument.

Arguments:

    hook (Callable): Callable hook that will be invoked before

        loading the state dict.

    with_module (bool, optional): Whether or not to pass the module

        instance to the hook as the first parameter.

##### 4.1.12 \_register\_state\_dict\_hook

[TOC](#table-of-contents)

**Description**

Register a post-hook for the :meth:`~torch.nn.Module.state_dict` method.

It should have the following signature::

    hook(module, state_dict, prefix, local_metadata) -> None or state_dict

The registered hooks can modify the ``state_dict`` inplace or return a new one.

If a new ``state_dict`` is returned, it will only be respected if it is the root

module that :meth:`~nn.Module.state_dict` is called from.

##### 4.1.13 \_replicate\_for\_data\_parallel

[TOC](#table-of-contents)

##### 4.1.14 \_save\_to\_state\_dict

[TOC](#table-of-contents)

**Description**

Save module state to the `destination` dictionary.

The `destination` dictionary will contain the state

of the module, but not its descendants. This is called on every

submodule in :meth:`~torch.nn.Module.state_dict`.

In rare cases, subclasses can achieve class-specific behavior by

overriding this method with custom logic.

Args:

    destination (dict): a dict where state will be stored

    prefix (str): the prefix for parameters and buffers used in this

        module

##### 4.1.15 \_slow\_forward

[TOC](#table-of-contents)

##### 4.1.16 \_wrapped\_call\_impl

[TOC](#table-of-contents)

##### 4.1.17 add\_module

[TOC](#table-of-contents)

**Description**

Add a child module to the current module.

The module can be accessed as an attribute using the given name.

Args:

    name (str): name of the child module. The child module can be

        accessed from this module using the given name

    module (Module): child module to be added to the module.

##### 4.1.18 apply

[TOC](#table-of-contents)

**Description**

Apply ``fn`` recursively to every submodule (as returned by ``.children()``) as well as self.

Typical use includes initializing the parameters of a model

(see also :ref:`nn-init-doc`).

Args:

    fn (:class:`Module` -> None): function to be applied to each submodule

Returns:

    Module: self

Example::

    >>> @torch.no_grad()

    >>> def init_weights(m):

    >>>     print(m)

    >>>     if type(m) == nn.Linear:

    >>>         m.weight.fill_(1.0)

    >>>         print(m.weight)

    >>> net = nn.Sequential(nn.Linear(2, 2), nn.Linear(2, 2))

    >>> net.apply(init_weights)

    Linear(in_features=2, out_features=2, bias=True)

    Parameter containing:

    tensor([[1., 1.],

            [1., 1.]], requires_grad=True)

    Linear(in_features=2, out_features=2, bias=True)

    Parameter containing:

    tensor([[1., 1.],

            [1., 1.]], requires_grad=True)

    Sequential(

      (0): Linear(in_features=2, out_features=2, bias=True)

      (1): Linear(in_features=2, out_features=2, bias=True)

    )

##### 4.1.19 bfloat16

[TOC](#table-of-contents)

**Description**

Casts all floating point parameters and buffers to ``bfloat16`` datatype.

.. note::

    This method modifies the module in-place.

Returns:

    Module: self

##### 4.1.20 buffers

[TOC](#table-of-contents)

**Description**

Return an iterator over module buffers.

Args:

    recurse (bool): if True, then yields buffers of this module

        and all submodules. Otherwise, yields only buffers that

        are direct members of this module.

Yields:

    torch.Tensor: module buffer

Example::

    >>> # xdoctest: +SKIP("undefined vars")

    >>> for buf in model.buffers():

    >>>     print(type(buf), buf.size())

    <class 'torch.Tensor'> (20L,)

    <class 'torch.Tensor'> (20L, 1L, 5L, 5L)

##### 4.1.21 children

[TOC](#table-of-contents)

**Description**

Return an iterator over immediate children modules.

Yields:

    Module: a child module

##### 4.1.22 compile

[TOC](#table-of-contents)

**Description**

Compile this Module's forward using :func:`torch.compile`.

This Module's `__call__` method is compiled and all arguments are passed as-is

to :func:`torch.compile`.

See :func:`torch.compile` for details on the arguments for this function.

##### 4.1.23 cpu

[TOC](#table-of-contents)

**Description**

Move all model parameters and buffers to the CPU.

.. note::

    This method modifies the module in-place.

Returns:

    Module: self

##### 4.1.24 cuda

[TOC](#table-of-contents)

**Description**

Move all model parameters and buffers to the GPU.

This also makes associated parameters and buffers different objects. So

it should be called before constructing the optimizer if the module will

live on GPU while being optimized.

.. note::

    This method modifies the module in-place.

Args:

    device (int, optional): if specified, all parameters will be

        copied to that device

Returns:

    Module: self

##### 4.1.25 double

[TOC](#table-of-contents)

**Description**

Casts all floating point parameters and buffers to ``double`` datatype.

.. note::

    This method modifies the module in-place.

Returns:

    Module: self

##### 4.1.26 eval

[TOC](#table-of-contents)

**Description**

Set the module in evaluation mode.

This has an effect only on certain modules. See the documentation of

particular modules for details of their behaviors in training/evaluation

mode, i.e. whether they are affected, e.g. :class:`Dropout`, :class:`BatchNorm`,

etc.

This is equivalent with :meth:`self.train(False) <torch.nn.Module.train>`.

See :ref:`locally-disable-grad-doc` for a comparison between

`.eval()` and several similar mechanisms that may be confused with it.

Returns:

    Module: self

##### 4.1.27 extra\_repr

[TOC](#table-of-contents)

**Description**

Return the extra representation of the module.

To print customized extra information, you should re-implement

this method in your own modules. Both single-line and multi-line

strings are acceptable.

##### 4.1.28 float

[TOC](#table-of-contents)

**Description**

Casts all floating point parameters and buffers to ``float`` datatype.

.. note::

    This method modifies the module in-place.

Returns:

    Module: self

### 4.1.29 forward

[TOC](#table-of-contents)

**Description**

Define the computation performed at every call.

Should be overridden by all subclasses.

.. note::

    Although the recipe for forward pass needs to be defined within

    this function, one should call the :class:`Module` instance afterwards

    instead of this since the former takes care of running the

    registered hooks while the latter silently ignores them.

##### 4.1.30 get\_buffer

[TOC](#table-of-contents)

**Description**

Return the buffer given by ``target`` if it exists, otherwise throw an error.

See the docstring for ``get_submodule`` for a more detailed

explanation of this method's functionality as well as how to

correctly specify ``target``.

Args:

    target: The fully-qualified string name of the buffer

        to look for. (See ``get_submodule`` for how to specify a

        fully-qualified string.)

Returns:

    torch.Tensor: The buffer referenced by ``target``

Raises:

    AttributeError: If the target string references an invalid

        path or resolves to something that is not a

        buffer

##### 4.1.31 get\_extra\_state

[TOC](#table-of-contents)

**Description**

Return any extra state to include in the module's state_dict.

Implement this and a corresponding :func:`set_extra_state` for your module

if you need to store extra state. This function is called when building the

module's `state_dict()`.

Note that extra state should be picklable to ensure working serialization

of the state_dict. We only provide backwards compatibility guarantees

for serializing Tensors; other objects may break backwards compatibility if

their serialized pickled form changes.

Returns:

    object: Any extra state to store in the module's state_dict

##### 4.1.32 get\_parameter

[TOC](#table-of-contents)

**Description**

Return the parameter given by ``target`` if it exists, otherwise throw an error.

See the docstring for ``get_submodule`` for a more detailed

explanation of this method's functionality as well as how to

correctly specify ``target``.

Args:

    target: The fully-qualified string name of the Parameter

        to look for. (See ``get_submodule`` for how to specify a

        fully-qualified string.)

Returns:

    torch.nn.Parameter: The Parameter referenced by ``target``

Raises:

    AttributeError: If the target string references an invalid

        path or resolves to something that is not an

        ``nn.Parameter``

##### 4.1.33 get\_submodule

[TOC](#table-of-contents)

**Description**

Return the submodule given by ``target`` if it exists, otherwise throw an error.

For example, let's say you have an ``nn.Module`` ``A`` that

looks like this:

.. code-block:: text

    A(

        (net_b): Module(

            (net_c): Module(

                (conv): Conv2d(16, 33, kernel_size=(3, 3), stride=(2, 2))

            )

            (linear): Linear(in_features=100, out_features=200, bias=True)

        )

    )

(The diagram shows an ``nn.Module`` ``A``. ``A`` which has a nested

submodule ``net_b``, which itself has two submodules ``net_c``

and ``linear``. ``net_c`` then has a submodule ``conv``.)

To check whether or not we have the ``linear`` submodule, we

would call ``get_submodule("net_b.linear")``. To check whether

we have the ``conv`` submodule, we would call

``get_submodule("net_b.net_c.conv")``.

The runtime of ``get_submodule`` is bounded by the degree

of module nesting in ``target``. A query against

``named_modules`` achieves the same result, but it is O(N) in

the number of transitive modules. So, for a simple check to see

if some submodule exists, ``get_submodule`` should always be

used.

Args:

    target: The fully-qualified string name of the submodule

        to look for. (See above example for how to specify a

        fully-qualified string.)

Returns:

    torch.nn.Module: The submodule referenced by ``target``

Raises:

    AttributeError: If the target string references an invalid

        path or resolves to something that is not an

        ``nn.Module``

##### 4.1.34 half

[TOC](#table-of-contents)

**Description**

Casts all floating point parameters and buffers to ``half`` datatype.

.. note::

    This method modifies the module in-place.

Returns:

    Module: self

##### 4.1.35 ipu

[TOC](#table-of-contents)

**Description**

Move all model parameters and buffers to the IPU.

This also makes associated parameters and buffers different objects. So

it should be called before constructing the optimizer if the module will

live on IPU while being optimized.

.. note::

    This method modifies the module in-place.

Arguments:

    device (int, optional): if specified, all parameters will be

        copied to that device

Returns:

    Module: self

##### 4.1.36 load\_state\_dict

[TOC](#table-of-contents)

**Description**

Copy parameters and buffers from :attr:`state_dict` into this module and its descendants.

If :attr:`strict` is ``True``, then

the keys of :attr:`state_dict` must exactly match the keys returned

by this module's :meth:`~torch.nn.Module.state_dict` function.

.. warning::

    If :attr:`assign` is ``True`` the optimizer must be created after

    the call to :attr:`load_state_dict` unless

    :func:`~torch.__future__.get_swap_module_params_on_conversion` is ``True``.

Args:

    state_dict (dict): a dict containing parameters and

        persistent buffers.

    strict (bool, optional): whether to strictly enforce that the keys

        in :attr:`state_dict` match the keys returned by this module's

        :meth:`~torch.nn.Module.state_dict` function. Default: ``True``

    assign (bool, optional): When set to ``False``, the properties of the tensors

        in the current module are preserved whereas setting it to ``True`` preserves

        properties of the Tensors in the state dict. The only

        exception is the ``requires_grad`` field of :class:`~torch.nn.Parameter`s

        for which the value from the module is preserved.

        Default: ``False``

Returns:

    ``NamedTuple`` with ``missing_keys`` and ``unexpected_keys`` fields:

        * **missing_keys** is a list of str containing any keys that are expected

            by this module but missing from the provided ``state_dict``.

        * **unexpected_keys** is a list of str containing the keys that are not

            expected by this module but present in the provided ``state_dict``.

Note:

    If a parameter or buffer is registered as ``None`` and its corresponding key

    exists in :attr:`state_dict`, :meth:`load_state_dict` will raise a

    ``RuntimeError``.

##### 4.1.37 modules

[TOC](#table-of-contents)

**Description**

Return an iterator over all modules in the network.

Yields:

    Module: a module in the network

Note:

    Duplicate modules are returned only once. In the following

    example, ``l`` will be returned only once.

Example::

    >>> l = nn.Linear(2, 2)

    >>> net = nn.Sequential(l, l)

    >>> for idx, m in enumerate(net.modules()):

    ...     print(idx, '->', m)

    0 -> Sequential(

      (0): Linear(in_features=2, out_features=2, bias=True)

      (1): Linear(in_features=2, out_features=2, bias=True)

    )

    1 -> Linear(in_features=2, out_features=2, bias=True)

##### 4.1.38 mtia

[TOC](#table-of-contents)

**Description**

Move all model parameters and buffers to the MTIA.

This also makes associated parameters and buffers different objects. So

it should be called before constructing the optimizer if the module will

live on MTIA while being optimized.

.. note::

    This method modifies the module in-place.

Arguments:

    device (int, optional): if specified, all parameters will be

        copied to that device

Returns:

    Module: self

##### 4.1.39 named\_buffers

[TOC](#table-of-contents)

**Description**

Return an iterator over module buffers, yielding both the name of the buffer as well as the buffer itself.

Args:

    prefix (str): prefix to prepend to all buffer names.

    recurse (bool, optional): if True, then yields buffers of this module

        and all submodules. Otherwise, yields only buffers that

        are direct members of this module. Defaults to True.

    remove_duplicate (bool, optional): whether to remove the duplicated buffers in the result. Defaults to True.

Yields:

    (str, torch.Tensor): Tuple containing the name and buffer

Example::

    >>> # xdoctest: +SKIP("undefined vars")

    >>> for name, buf in self.named_buffers():

    >>>     if name in ['running_var']:

    >>>         print(buf.size())

##### 4.1.40 named\_children

[TOC](#table-of-contents)

**Description**

Return an iterator over immediate children modules, yielding both the name of the module as well as the module itself.

Yields:

    (str, Module): Tuple containing a name and child module

Example::

    >>> # xdoctest: +SKIP("undefined vars")

    >>> for name, module in model.named_children():

    >>>     if name in ['conv4', 'conv5']:

    >>>         print(module)

##### 4.1.41 named\_modules

[TOC](#table-of-contents)

**Description**

Return an iterator over all modules in the network, yielding both the name of the module as well as the module itself.

Args:

    memo: a memo to store the set of modules already added to the result

    prefix: a prefix that will be added to the name of the module

    remove_duplicate: whether to remove the duplicated module instances in the result

        or not

Yields:

    (str, Module): Tuple of name and module

Note:

    Duplicate modules are returned only once. In the following

    example, ``l`` will be returned only once.

Example::

    >>> l = nn.Linear(2, 2)

    >>> net = nn.Sequential(l, l)

    >>> for idx, m in enumerate(net.named_modules()):

    ...     print(idx, '->', m)

    0 -> ('', Sequential(

      (0): Linear(in_features=2, out_features=2, bias=True)

      (1): Linear(in_features=2, out_features=2, bias=True)

    ))

    1 -> ('0', Linear(in_features=2, out_features=2, bias=True))

##### 4.1.42 named\_parameters

[TOC](#table-of-contents)

**Description**

Return an iterator over module parameters, yielding both the name of the parameter as well as the parameter itself.

Args:

    prefix (str): prefix to prepend to all parameter names.

    recurse (bool): if True, then yields parameters of this module

        and all submodules. Otherwise, yields only parameters that

        are direct members of this module.

    remove_duplicate (bool, optional): whether to remove the duplicated

        parameters in the result. Defaults to True.

Yields:

    (str, Parameter): Tuple containing the name and parameter

Example::

    >>> # xdoctest: +SKIP("undefined vars")

    >>> for name, param in self.named_parameters():

    >>>     if name in ['bias']:

    >>>         print(param.size())

##### 4.1.43 parameters

[TOC](#table-of-contents)

**Description**

Return an iterator over module parameters.

This is typically passed to an optimizer.

Args:

    recurse (bool): if True, then yields parameters of this module

        and all submodules. Otherwise, yields only parameters that

        are direct members of this module.

Yields:

    Parameter: module parameter

Example::

    >>> # xdoctest: +SKIP("undefined vars")

    >>> for param in model.parameters():

    >>>     print(type(param), param.size())

    <class 'torch.Tensor'> (20L,)

    <class 'torch.Tensor'> (20L, 1L, 5L, 5L)

##### 4.1.44 register\_backward\_hook

[TOC](#table-of-contents)

**Description**

Register a backward hook on the module.

This function is deprecated in favor of :meth:`~torch.nn.Module.register_full_backward_hook` and

the behavior of this function will change in future versions.

Returns:

    :class:`torch.utils.hooks.RemovableHandle`:

        a handle that can be used to remove the added hook by calling

        ``handle.remove()``

##### 4.1.45 register\_buffer

[TOC](#table-of-contents)

**Description**

Add a buffer to the module.

This is typically used to register a buffer that should not to be

considered a model parameter. For example, BatchNorm's ``running_mean``

is not a parameter, but is part of the module's state. Buffers, by

default, are persistent and will be saved alongside parameters. This

behavior can be changed by setting :attr:`persistent` to ``False``. The

only difference between a persistent buffer and a non-persistent buffer

is that the latter will not be a part of this module's

:attr:`state_dict`.

Buffers can be accessed as attributes using given names.

Args:

    name (str): name of the buffer. The buffer can be accessed

        from this module using the given name

    tensor (Tensor or None): buffer to be registered. If ``None``, then operations

        that run on buffers, such as :attr:`cuda`, are ignored. If ``None``,

        the buffer is **not** included in the module's :attr:`state_dict`.

    persistent (bool): whether the buffer is part of this module's

        :attr:`state_dict`.

Example::

    >>> # xdoctest: +SKIP("undefined vars")

    >>> self.register_buffer('running_mean', torch.zeros(num_features))

##### 4.1.46 register\_forward\_hook

[TOC](#table-of-contents)

**Description**

Register a forward hook on the module.

The hook will be called every time after :func:`forward` has computed an output.

If ``with_kwargs`` is ``False`` or not specified, the input contains only

the positional arguments given to the module. Keyword arguments won't be

passed to the hooks and only to the ``forward``. The hook can modify the

output. It can modify the input inplace but it will not have effect on

forward since this is called after :func:`forward` is called. The hook

should have the following signature::

    hook(module, args, output) -> None or modified output

If ``with_kwargs`` is ``True``, the forward hook will be passed the

``kwargs`` given to the forward function and be expected to return the

output possibly modified. The hook should have the following signature::

    hook(module, args, kwargs, output) -> None or modified output

Args:

    hook (Callable): The user defined hook to be registered.

    prepend (bool): If ``True``, the provided ``hook`` will be fired

        before all existing ``forward`` hooks on this

        :class:`torch.nn.modules.Module`. Otherwise, the provided

        ``hook`` will be fired after all existing ``forward`` hooks on

        this :class:`torch.nn.modules.Module`. Note that global

        ``forward`` hooks registered with

        :func:`register_module_forward_hook` will fire before all hooks

        registered by this method.

        Default: ``False``

    with_kwargs (bool): If ``True``, the ``hook`` will be passed the

        kwargs given to the forward function.

        Default: ``False``

    always_call (bool): If ``True`` the ``hook`` will be run regardless of

        whether an exception is raised while calling the Module.

        Default: ``False``

Returns:

    :class:`torch.utils.hooks.RemovableHandle`:

        a handle that can be used to remove the added hook by calling

        ``handle.remove()``

##### 4.1.47 register\_forward\_pre\_hook

[TOC](#table-of-contents)

**Description**

Register a forward pre-hook on the module.

The hook will be called every time before :func:`forward` is invoked.

If ``with_kwargs`` is false or not specified, the input contains only

the positional arguments given to the module. Keyword arguments won't be

passed to the hooks and only to the ``forward``. The hook can modify the

input. User can either return a tuple or a single modified value in the

hook. We will wrap the value into a tuple if a single value is returned

(unless that value is already a tuple). The hook should have the

following signature::

    hook(module, args) -> None or modified input

If ``with_kwargs`` is true, the forward pre-hook will be passed the

kwargs given to the forward function. And if the hook modifies the

input, both the args and kwargs should be returned. The hook should have

the following signature::

    hook(module, args, kwargs) -> None or a tuple of modified input and kwargs

Args:

    hook (Callable): The user defined hook to be registered.

    prepend (bool): If true, the provided ``hook`` will be fired before

        all existing ``forward_pre`` hooks on this

        :class:`torch.nn.modules.Module`. Otherwise, the provided

        ``hook`` will be fired after all existing ``forward_pre`` hooks

        on this :class:`torch.nn.modules.Module`. Note that global

        ``forward_pre`` hooks registered with

        :func:`register_module_forward_pre_hook` will fire before all

        hooks registered by this method.

        Default: ``False``

    with_kwargs (bool): If true, the ``hook`` will be passed the kwargs

        given to the forward function.

        Default: ``False``

Returns:

    :class:`torch.utils.hooks.RemovableHandle`:

        a handle that can be used to remove the added hook by calling

        ``handle.remove()``

##### 4.1.48 register\_full\_backward\_hook

[TOC](#table-of-contents)

**Description**

Register a backward hook on the module.

The hook will be called every time the gradients with respect to a module

are computed, i.e. the hook will execute if and only if the gradients with

respect to module outputs are computed. The hook should have the following

signature::

    hook(module, grad_input, grad_output) -> tuple(Tensor) or None

The :attr:`grad_input` and :attr:`grad_output` are tuples that contain the gradients

with respect to the inputs and outputs respectively. The hook should

not modify its arguments, but it can optionally return a new gradient with

respect to the input that will be used in place of :attr:`grad_input` in

subsequent computations. :attr:`grad_input` will only correspond to the inputs given

as positional arguments and all kwarg arguments are ignored. Entries

in :attr:`grad_input` and :attr:`grad_output` will be ``None`` for all non-Tensor

arguments.

For technical reasons, when this hook is applied to a Module, its forward function will

receive a view of each Tensor passed to the Module. Similarly the caller will receive a view

of each Tensor returned by the Module's forward function.

.. warning ::

    Modifying inputs or outputs inplace is not allowed when using backward hooks and

    will raise an error.

Args:

    hook (Callable): The user-defined hook to be registered.

    prepend (bool): If true, the provided ``hook`` will be fired before

        all existing ``backward`` hooks on this

        :class:`torch.nn.modules.Module`. Otherwise, the provided

        ``hook`` will be fired after all existing ``backward`` hooks on

        this :class:`torch.nn.modules.Module`. Note that global

        ``backward`` hooks registered with

        :func:`register_module_full_backward_hook` will fire before

        all hooks registered by this method.

Returns:

    :class:`torch.utils.hooks.RemovableHandle`:

        a handle that can be used to remove the added hook by calling

        ``handle.remove()``

##### 4.1.49 register\_full\_backward\_pre\_hook

[TOC](#table-of-contents)

**Description**

Register a backward pre-hook on the module.

The hook will be called every time the gradients for the module are computed.

The hook should have the following signature::

    hook(module, grad_output) -> tuple[Tensor] or None

The :attr:`grad_output` is a tuple. The hook should

not modify its arguments, but it can optionally return a new gradient with

respect to the output that will be used in place of :attr:`grad_output` in

subsequent computations. Entries in :attr:`grad_output` will be ``None`` for

all non-Tensor arguments.

For technical reasons, when this hook is applied to a Module, its forward function will

receive a view of each Tensor passed to the Module. Similarly the caller will receive a view

of each Tensor returned by the Module's forward function.

.. warning ::

    Modifying inputs inplace is not allowed when using backward hooks and

    will raise an error.

Args:

    hook (Callable): The user-defined hook to be registered.

    prepend (bool): If true, the provided ``hook`` will be fired before

        all existing ``backward_pre`` hooks on this

        :class:`torch.nn.modules.Module`. Otherwise, the provided

        ``hook`` will be fired after all existing ``backward_pre`` hooks

        on this :class:`torch.nn.modules.Module`. Note that global

        ``backward_pre`` hooks registered with

        :func:`register_module_full_backward_pre_hook` will fire before

        all hooks registered by this method.

Returns:

    :class:`torch.utils.hooks.RemovableHandle`:

        a handle that can be used to remove the added hook by calling

        ``handle.remove()``

##### 4.1.50 register\_load\_state\_dict\_post\_hook

[TOC](#table-of-contents)

**Description**

Register a post-hook to be run after module's :meth:`~nn.Module.load_state_dict` is called.

It should have the following signature::

    hook(module, incompatible_keys) -> None

The ``module`` argument is the current module that this hook is registered

on, and the ``incompatible_keys`` argument is a ``NamedTuple`` consisting

of attributes ``missing_keys`` and ``unexpected_keys``. ``missing_keys``

is a ``list`` of ``str`` containing the missing keys and

``unexpected_keys`` is a ``list`` of ``str`` containing the unexpected keys.

The given incompatible_keys can be modified inplace if needed.

Note that the checks performed when calling :func:`load_state_dict` with

``strict=True`` are affected by modifications the hook makes to

``missing_keys`` or ``unexpected_keys``, as expected. Additions to either

set of keys will result in an error being thrown when ``strict=True``, and

clearing out both missing and unexpected keys will avoid an error.

Returns:

    :class:`torch.utils.hooks.RemovableHandle`:

        a handle that can be used to remove the added hook by calling

        ``handle.remove()``

##### 4.1.51 register\_load\_state\_dict\_pre\_hook

[TOC](#table-of-contents)

**Description**

Register a pre-hook to be run before module's :meth:`~nn.Module.load_state_dict` is called.

It should have the following signature::

    hook(module, state_dict, prefix, local_metadata, strict, missing_keys, unexpected_keys, error_msgs) -> None  # noqa: B950

Arguments:

    hook (Callable): Callable hook that will be invoked before

        loading the state dict.

##### 4.1.52 register\_module

[TOC](#table-of-contents)

**Description**

Alias for :func:`add_module`.

##### 4.1.53 register\_parameter

[TOC](#table-of-contents)

**Description**

Add a parameter to the module.

The parameter can be accessed as an attribute using given name.

Args:

    name (str): name of the parameter. The parameter can be accessed

        from this module using the given name

    param (Parameter or None): parameter to be added to the module. If

        ``None``, then operations that run on parameters, such as :attr:`cuda`,

        are ignored. If ``None``, the parameter is **not** included in the

        module's :attr:`state_dict`.

##### 4.1.54 register\_state\_dict\_post\_hook

[TOC](#table-of-contents)

**Description**

Register a post-hook for the :meth:`~torch.nn.Module.state_dict` method.

It should have the following signature::

    hook(module, state_dict, prefix, local_metadata) -> None

The registered hooks can modify the ``state_dict`` inplace.

##### 4.1.55 register\_state\_dict\_pre\_hook

[TOC](#table-of-contents)

**Description**

Register a pre-hook for the :meth:`~torch.nn.Module.state_dict` method.

It should have the following signature::

    hook(module, prefix, keep_vars) -> None

The registered hooks can be used to perform pre-processing before the ``state_dict``

call is made.

##### 4.1.56 requires\_grad\_

[TOC](#table-of-contents)

**Description**

Change if autograd should record operations on parameters in this module.

This method sets the parameters' :attr:`requires_grad` attributes

in-place.

This method is helpful for freezing part of the module for finetuning

or training parts of a model individually (e.g., GAN training).

See :ref:`locally-disable-grad-doc` for a comparison between

`.requires_grad_()` and several similar mechanisms that may be confused with it.

Args:

    requires_grad (bool): whether autograd should record operations on

                          parameters in this module. Default: ``True``.

Returns:

    Module: self

##### 4.1.57 set\_extra\_state

[TOC](#table-of-contents)

**Description**

Set extra state contained in the loaded `state_dict`.

This function is called from :func:`load_state_dict` to handle any extra state

found within the `state_dict`. Implement this function and a corresponding

:func:`get_extra_state` for your module if you need to store extra state within its

`state_dict`.

Args:

    state (dict): Extra state from the `state_dict`

##### 4.1.58 set\_submodule

[TOC](#table-of-contents)

**Description**

Set the submodule given by ``target`` if it exists, otherwise throw an error.

For example, let's say you have an ``nn.Module`` ``A`` that

looks like this:

.. code-block:: text

    A(

        (net_b): Module(

            (net_c): Module(

                (conv): Conv2d(16, 33, kernel_size=(3, 3), stride=(2, 2))

            )

            (linear): Linear(in_features=100, out_features=200, bias=True)

        )

    )

(The diagram shows an ``nn.Module`` ``A``. ``A`` has a nested

submodule ``net_b``, which itself has two submodules ``net_c``

and ``linear``. ``net_c`` then has a submodule ``conv``.)

To overide the ``Conv2d`` with a new submodule ``Linear``, you

would call

``set_submodule("net_b.net_c.conv", nn.Linear(33, 16))``.

Args:

    target: The fully-qualified string name of the submodule

        to look for. (See above example for how to specify a

        fully-qualified string.)

    module: The module to set the submodule to.

Raises:

    ValueError: If the target string is empty

    AttributeError: If the target string references an invalid

        path or resolves to something that is not an

        ``nn.Module``

##### 4.1.59 share\_memory

[TOC](#table-of-contents)

**Description**

See :meth:`torch.Tensor.share_memory_`.

##### 4.1.60 state\_dict

[TOC](#table-of-contents)

**Description**

Return a dictionary containing references to the whole state of the module.

Both parameters and persistent buffers (e.g. running averages) are

included. Keys are corresponding parameter and buffer names.

Parameters and buffers set to ``None`` are not included.

.. note::

    The returned object is a shallow copy. It contains references

    to the module's parameters and buffers.

.. warning::

    Currently ``state_dict()`` also accepts positional arguments for

    ``destination``, ``prefix`` and ``keep_vars`` in order. However,

    this is being deprecated and keyword arguments will be enforced in

    future releases.

.. warning::

    Please avoid the use of argument ``destination`` as it is not

    designed for end-users.

Args:

    destination (dict, optional): If provided, the state of module will

        be updated into the dict and the same object is returned.

        Otherwise, an ``OrderedDict`` will be created and returned.

        Default: ``None``.

    prefix (str, optional): a prefix added to parameter and buffer

        names to compose the keys in state_dict. Default: ``''``.

    keep_vars (bool, optional): by default the :class:`~torch.Tensor` s

        returned in the state dict are detached from autograd. If it's

        set to ``True``, detaching will not be performed.

        Default: ``False``.

Returns:

    dict:

        a dictionary containing a whole state of the module

Example::

    >>> # xdoctest: +SKIP("undefined vars")

    >>> module.state_dict().keys()

    ['bias', 'weight']

##### 4.1.61 to

[TOC](#table-of-contents)

**Description**

Move and/or cast the parameters and buffers.

This can be called as

.. function:: to(device=None, dtype=None, non_blocking=False)

   :noindex:

.. function:: to(dtype, non_blocking=False)

   :noindex:

.. function:: to(tensor, non_blocking=False)

   :noindex:

.. function:: to(memory_format=torch.channels_last)

   :noindex:

Its signature is similar to :meth:`torch.Tensor.to`, but only accepts

floating point or complex :attr:`dtype`\ s. In addition, this method will

only cast the floating point or complex parameters and buffers to :attr:`dtype`

(if given). The integral parameters and buffers will be moved

:attr:`device`, if that is given, but with dtypes unchanged. When

:attr:`non_blocking` is set, it tries to convert/move asynchronously

with respect to the host if possible, e.g., moving CPU Tensors with

pinned memory to CUDA devices.

See below for examples.

.. note::

    This method modifies the module in-place.

Args:

    device (:class:`torch.device`): the desired device of the parameters

        and buffers in this module

    dtype (:class:`torch.dtype`): the desired floating point or complex dtype of

        the parameters and buffers in this module

    tensor (torch.Tensor): Tensor whose dtype and device are the desired

        dtype and device for all parameters and buffers in this module

    memory_format (:class:`torch.memory_format`): the desired memory

        format for 4D parameters and buffers in this module (keyword

        only argument)

Returns:

    Module: self

Examples::

    >>> # xdoctest: +IGNORE_WANT("non-deterministic")

    >>> linear = nn.Linear(2, 2)

    >>> linear.weight

    Parameter containing:

    tensor([[ 0.1913, -0.3420],

            [-0.5113, -0.2325]])

    >>> linear.to(torch.double)

    Linear(in_features=2, out_features=2, bias=True)

    >>> linear.weight

    Parameter containing:

    tensor([[ 0.1913, -0.3420],

            [-0.5113, -0.2325]], dtype=torch.float64)

    >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_CUDA1)

    >>> gpu1 = torch.device("cuda:1")

    >>> linear.to(gpu1, dtype=torch.half, non_blocking=True)

    Linear(in_features=2, out_features=2, bias=True)

    >>> linear.weight

    Parameter containing:

    tensor([[ 0.1914, -0.3420],

            [-0.5112, -0.2324]], dtype=torch.float16, device='cuda:1')

    >>> cpu = torch.device("cpu")

    >>> linear.to(cpu)

    Linear(in_features=2, out_features=2, bias=True)

    >>> linear.weight

    Parameter containing:

    tensor([[ 0.1914, -0.3420],

            [-0.5112, -0.2324]], dtype=torch.float16)

    >>> linear = nn.Linear(2, 2, bias=None).to(torch.cdouble)

    >>> linear.weight

    Parameter containing:

    tensor([[ 0.3741+0.j,  0.2382+0.j],

            [ 0.5593+0.j, -0.4443+0.j]], dtype=torch.complex128)

    >>> linear(torch.ones(3, 2, dtype=torch.cdouble))

    tensor([[0.6122+0.j, 0.1150+0.j],

            [0.6122+0.j, 0.1150+0.j],

            [0.6122+0.j, 0.1150+0.j]], dtype=torch.complex128)

##### 4.1.62 to\_empty

[TOC](#table-of-contents)

**Description**

Move the parameters and buffers to the specified device without copying storage.

Args:

    device (:class:`torch.device`): The desired device of the parameters

        and buffers in this module.

    recurse (bool): Whether parameters and buffers of submodules should

        be recursively moved to the specified device.

Returns:

    Module: self

##### 4.1.63 train

[TOC](#table-of-contents)

**Description**

Set the module in training mode.

This has an effect only on certain modules. See the documentation of

particular modules for details of their behaviors in training/evaluation

mode, i.e., whether they are affected, e.g. :class:`Dropout`, :class:`BatchNorm`,

etc.

Args:

    mode (bool): whether to set training mode (``True``) or evaluation

                 mode (``False``). Default: ``True``.

Returns:

    Module: self

##### 4.1.64 type

[TOC](#table-of-contents)

**Description**

Casts all parameters and buffers to :attr:`dst_type`.

.. note::

    This method modifies the module in-place.

Args:

    dst_type (type or string): the desired type

Returns:

    Module: self

##### 4.1.65 xpu

[TOC](#table-of-contents)

**Description**

Move all model parameters and buffers to the XPU.

This also makes associated parameters and buffers different objects. So

it should be called before constructing optimizer if the module will

live on XPU while being optimized.

.. note::

    This method modifies the module in-place.

Arguments:

    device (int, optional): if specified, all parameters will be

        copied to that device

Returns:

    Module: self

##### 4.1.66 zero\_grad

[TOC](#table-of-contents)

**Description**

Reset gradients of all model parameters.

See similar function under :class:`torch.optim.Optimizer` for more context.

Args:

    set_to_none (bool): instead of setting to zero, set the grads to None.

        See :meth:`torch.optim.Optimizer.zero_grad` for details.

## 4.2 SelfAttention : torch.nn.modules.module.Module

[TOC](#table-of-contents)

**Description**

Base class for all neural network modules.

Your models should also subclass this class.

Modules can also contain other Modules, allowing them to be nested in
a tree structure. You can assign the submodules as regular attributes::

    import torch.nn as nn
    import torch.nn.functional as F

    class Model(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.conv1 = nn.Conv2d(1, 20, 5)
            self.conv2 = nn.Conv2d(20, 20, 5)

        def forward(self, x):
            x = F.relu(self.conv1(x))
            return F.relu(self.conv2(x))

Submodules assigned in this way will be registered, and will also have their
parameters converted when you call :meth:`to`, etc.

.. note::
    As per the example above, an ``__init__()`` call to the parent class
    must be made before assignment on the child.

:ivar training: Boolean represents whether this module is in training or
                evaluation mode.
:vartype training: bool


##### 4.2.1 \_wrapped\_call\_impl

[TOC](#table-of-contents)

### 4.2.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initialize internal Module state, shared by both nn.Module and ScriptModule.

##### 4.2.3 \_apply

[TOC](#table-of-contents)

##### 4.2.4 \_call\_impl

[TOC](#table-of-contents)

##### 4.2.5 \_get\_backward\_hooks

[TOC](#table-of-contents)

**Description**

Return the backward hooks for use in the call function.

It returns two lists, one with the full backward hooks and one with the non-full

backward hooks.

##### 4.2.6 \_get\_backward\_pre\_hooks

[TOC](#table-of-contents)

##### 4.2.7 \_get\_name

[TOC](#table-of-contents)

##### 4.2.8 \_load\_from\_state\_dict

[TOC](#table-of-contents)

**Description**

Copy parameters and buffers from :attr:`state_dict` into only this module, but not its descendants.

This is called on every submodule

in :meth:`~torch.nn.Module.load_state_dict`. Metadata saved for this

module in input :attr:`state_dict` is provided as :attr:`local_metadata`.

For state dicts without metadata, :attr:`local_metadata` is empty.

Subclasses can achieve class-specific backward compatible loading using

the version number at `local_metadata.get("version", None)`.

Additionally, :attr:`local_metadata` can also contain the key

`assign_to_params_buffers` that indicates whether keys should be

assigned their corresponding tensor in the state_dict.

.. note::

    :attr:`state_dict` is not the same object as the input

    :attr:`state_dict` to :meth:`~torch.nn.Module.load_state_dict`. So

    it can be modified.

Args:

    state_dict (dict): a dict containing parameters and

        persistent buffers.

    prefix (str): the prefix for parameters and buffers used in this

        module

    local_metadata (dict): a dict containing the metadata for this module.

        See

    strict (bool): whether to strictly enforce that the keys in

        :attr:`state_dict` with :attr:`prefix` match the names of

        parameters and buffers in this module

    missing_keys (list of str): if ``strict=True``, add missing keys to

        this list

    unexpected_keys (list of str): if ``strict=True``, add unexpected

        keys to this list

    error_msgs (list of str): error messages should be added to this

        list, and will be reported together in

        :meth:`~torch.nn.Module.load_state_dict`

##### 4.2.9 \_maybe\_warn\_non\_full\_backward\_hook

[TOC](#table-of-contents)

##### 4.2.10 \_named\_members

[TOC](#table-of-contents)

**Description**

Help yield various names + members of modules.

##### 4.2.11 \_register\_load\_state\_dict\_pre\_hook

[TOC](#table-of-contents)

**Description**

See :meth:`~torch.nn.Module.register_load_state_dict_pre_hook` for details.

A subtle difference is that if ``with_module`` is set to ``False``, then the

hook will not take the ``module`` as the first argument whereas

:meth:`~torch.nn.Module.register_load_state_dict_pre_hook` always takes the

``module`` as the first argument.

Arguments:

    hook (Callable): Callable hook that will be invoked before

        loading the state dict.

    with_module (bool, optional): Whether or not to pass the module

        instance to the hook as the first parameter.

##### 4.2.12 \_register\_state\_dict\_hook

[TOC](#table-of-contents)

**Description**

Register a post-hook for the :meth:`~torch.nn.Module.state_dict` method.

It should have the following signature::

    hook(module, state_dict, prefix, local_metadata) -> None or state_dict

The registered hooks can modify the ``state_dict`` inplace or return a new one.

If a new ``state_dict`` is returned, it will only be respected if it is the root

module that :meth:`~nn.Module.state_dict` is called from.

##### 4.2.13 \_replicate\_for\_data\_parallel

[TOC](#table-of-contents)

##### 4.2.14 \_save\_to\_state\_dict

[TOC](#table-of-contents)

**Description**

Save module state to the `destination` dictionary.

The `destination` dictionary will contain the state

of the module, but not its descendants. This is called on every

submodule in :meth:`~torch.nn.Module.state_dict`.

In rare cases, subclasses can achieve class-specific behavior by

overriding this method with custom logic.

Args:

    destination (dict): a dict where state will be stored

    prefix (str): the prefix for parameters and buffers used in this

        module

##### 4.2.15 \_slow\_forward

[TOC](#table-of-contents)

##### 4.2.16 \_wrapped\_call\_impl

[TOC](#table-of-contents)

##### 4.2.17 add\_module

[TOC](#table-of-contents)

**Description**

Add a child module to the current module.

The module can be accessed as an attribute using the given name.

Args:

    name (str): name of the child module. The child module can be

        accessed from this module using the given name

    module (Module): child module to be added to the module.

##### 4.2.18 apply

[TOC](#table-of-contents)

**Description**

Apply ``fn`` recursively to every submodule (as returned by ``.children()``) as well as self.

Typical use includes initializing the parameters of a model

(see also :ref:`nn-init-doc`).

Args:

    fn (:class:`Module` -> None): function to be applied to each submodule

Returns:

    Module: self

Example::

    >>> @torch.no_grad()

    >>> def init_weights(m):

    >>>     print(m)

    >>>     if type(m) == nn.Linear:

    >>>         m.weight.fill_(1.0)

    >>>         print(m.weight)

    >>> net = nn.Sequential(nn.Linear(2, 2), nn.Linear(2, 2))

    >>> net.apply(init_weights)

    Linear(in_features=2, out_features=2, bias=True)

    Parameter containing:

    tensor([[1., 1.],

            [1., 1.]], requires_grad=True)

    Linear(in_features=2, out_features=2, bias=True)

    Parameter containing:

    tensor([[1., 1.],

            [1., 1.]], requires_grad=True)

    Sequential(

      (0): Linear(in_features=2, out_features=2, bias=True)

      (1): Linear(in_features=2, out_features=2, bias=True)

    )

##### 4.2.19 bfloat16

[TOC](#table-of-contents)

**Description**

Casts all floating point parameters and buffers to ``bfloat16`` datatype.

.. note::

    This method modifies the module in-place.

Returns:

    Module: self

##### 4.2.20 buffers

[TOC](#table-of-contents)

**Description**

Return an iterator over module buffers.

Args:

    recurse (bool): if True, then yields buffers of this module

        and all submodules. Otherwise, yields only buffers that

        are direct members of this module.

Yields:

    torch.Tensor: module buffer

Example::

    >>> # xdoctest: +SKIP("undefined vars")

    >>> for buf in model.buffers():

    >>>     print(type(buf), buf.size())

    <class 'torch.Tensor'> (20L,)

    <class 'torch.Tensor'> (20L, 1L, 5L, 5L)

##### 4.2.21 children

[TOC](#table-of-contents)

**Description**

Return an iterator over immediate children modules.

Yields:

    Module: a child module

##### 4.2.22 compile

[TOC](#table-of-contents)

**Description**

Compile this Module's forward using :func:`torch.compile`.

This Module's `__call__` method is compiled and all arguments are passed as-is

to :func:`torch.compile`.

See :func:`torch.compile` for details on the arguments for this function.

##### 4.2.23 cpu

[TOC](#table-of-contents)

**Description**

Move all model parameters and buffers to the CPU.

.. note::

    This method modifies the module in-place.

Returns:

    Module: self

##### 4.2.24 cuda

[TOC](#table-of-contents)

**Description**

Move all model parameters and buffers to the GPU.

This also makes associated parameters and buffers different objects. So

it should be called before constructing the optimizer if the module will

live on GPU while being optimized.

.. note::

    This method modifies the module in-place.

Args:

    device (int, optional): if specified, all parameters will be

        copied to that device

Returns:

    Module: self

##### 4.2.25 double

[TOC](#table-of-contents)

**Description**

Casts all floating point parameters and buffers to ``double`` datatype.

.. note::

    This method modifies the module in-place.

Returns:

    Module: self

##### 4.2.26 eval

[TOC](#table-of-contents)

**Description**

Set the module in evaluation mode.

This has an effect only on certain modules. See the documentation of

particular modules for details of their behaviors in training/evaluation

mode, i.e. whether they are affected, e.g. :class:`Dropout`, :class:`BatchNorm`,

etc.

This is equivalent with :meth:`self.train(False) <torch.nn.Module.train>`.

See :ref:`locally-disable-grad-doc` for a comparison between

`.eval()` and several similar mechanisms that may be confused with it.

Returns:

    Module: self

##### 4.2.27 extra\_repr

[TOC](#table-of-contents)

**Description**

Return the extra representation of the module.

To print customized extra information, you should re-implement

this method in your own modules. Both single-line and multi-line

strings are acceptable.

##### 4.2.28 float

[TOC](#table-of-contents)

**Description**

Casts all floating point parameters and buffers to ``float`` datatype.

.. note::

    This method modifies the module in-place.

Returns:

    Module: self

### 4.2.29 forward

[TOC](#table-of-contents)

**Description**

Define the computation performed at every call.

Should be overridden by all subclasses.

.. note::

    Although the recipe for forward pass needs to be defined within

    this function, one should call the :class:`Module` instance afterwards

    instead of this since the former takes care of running the

    registered hooks while the latter silently ignores them.

##### 4.2.30 get\_buffer

[TOC](#table-of-contents)

**Description**

Return the buffer given by ``target`` if it exists, otherwise throw an error.

See the docstring for ``get_submodule`` for a more detailed

explanation of this method's functionality as well as how to

correctly specify ``target``.

Args:

    target: The fully-qualified string name of the buffer

        to look for. (See ``get_submodule`` for how to specify a

        fully-qualified string.)

Returns:

    torch.Tensor: The buffer referenced by ``target``

Raises:

    AttributeError: If the target string references an invalid

        path or resolves to something that is not a

        buffer

##### 4.2.31 get\_extra\_state

[TOC](#table-of-contents)

**Description**

Return any extra state to include in the module's state_dict.

Implement this and a corresponding :func:`set_extra_state` for your module

if you need to store extra state. This function is called when building the

module's `state_dict()`.

Note that extra state should be picklable to ensure working serialization

of the state_dict. We only provide backwards compatibility guarantees

for serializing Tensors; other objects may break backwards compatibility if

their serialized pickled form changes.

Returns:

    object: Any extra state to store in the module's state_dict

##### 4.2.32 get\_parameter

[TOC](#table-of-contents)

**Description**

Return the parameter given by ``target`` if it exists, otherwise throw an error.

See the docstring for ``get_submodule`` for a more detailed

explanation of this method's functionality as well as how to

correctly specify ``target``.

Args:

    target: The fully-qualified string name of the Parameter

        to look for. (See ``get_submodule`` for how to specify a

        fully-qualified string.)

Returns:

    torch.nn.Parameter: The Parameter referenced by ``target``

Raises:

    AttributeError: If the target string references an invalid

        path or resolves to something that is not an

        ``nn.Parameter``

##### 4.2.33 get\_submodule

[TOC](#table-of-contents)

**Description**

Return the submodule given by ``target`` if it exists, otherwise throw an error.

For example, let's say you have an ``nn.Module`` ``A`` that

looks like this:

.. code-block:: text

    A(

        (net_b): Module(

            (net_c): Module(

                (conv): Conv2d(16, 33, kernel_size=(3, 3), stride=(2, 2))

            )

            (linear): Linear(in_features=100, out_features=200, bias=True)

        )

    )

(The diagram shows an ``nn.Module`` ``A``. ``A`` which has a nested

submodule ``net_b``, which itself has two submodules ``net_c``

and ``linear``. ``net_c`` then has a submodule ``conv``.)

To check whether or not we have the ``linear`` submodule, we

would call ``get_submodule("net_b.linear")``. To check whether

we have the ``conv`` submodule, we would call

``get_submodule("net_b.net_c.conv")``.

The runtime of ``get_submodule`` is bounded by the degree

of module nesting in ``target``. A query against

``named_modules`` achieves the same result, but it is O(N) in

the number of transitive modules. So, for a simple check to see

if some submodule exists, ``get_submodule`` should always be

used.

Args:

    target: The fully-qualified string name of the submodule

        to look for. (See above example for how to specify a

        fully-qualified string.)

Returns:

    torch.nn.Module: The submodule referenced by ``target``

Raises:

    AttributeError: If the target string references an invalid

        path or resolves to something that is not an

        ``nn.Module``

##### 4.2.34 half

[TOC](#table-of-contents)

**Description**

Casts all floating point parameters and buffers to ``half`` datatype.

.. note::

    This method modifies the module in-place.

Returns:

    Module: self

##### 4.2.35 ipu

[TOC](#table-of-contents)

**Description**

Move all model parameters and buffers to the IPU.

This also makes associated parameters and buffers different objects. So

it should be called before constructing the optimizer if the module will

live on IPU while being optimized.

.. note::

    This method modifies the module in-place.

Arguments:

    device (int, optional): if specified, all parameters will be

        copied to that device

Returns:

    Module: self

##### 4.2.36 load\_state\_dict

[TOC](#table-of-contents)

**Description**

Copy parameters and buffers from :attr:`state_dict` into this module and its descendants.

If :attr:`strict` is ``True``, then

the keys of :attr:`state_dict` must exactly match the keys returned

by this module's :meth:`~torch.nn.Module.state_dict` function.

.. warning::

    If :attr:`assign` is ``True`` the optimizer must be created after

    the call to :attr:`load_state_dict` unless

    :func:`~torch.__future__.get_swap_module_params_on_conversion` is ``True``.

Args:

    state_dict (dict): a dict containing parameters and

        persistent buffers.

    strict (bool, optional): whether to strictly enforce that the keys

        in :attr:`state_dict` match the keys returned by this module's

        :meth:`~torch.nn.Module.state_dict` function. Default: ``True``

    assign (bool, optional): When set to ``False``, the properties of the tensors

        in the current module are preserved whereas setting it to ``True`` preserves

        properties of the Tensors in the state dict. The only

        exception is the ``requires_grad`` field of :class:`~torch.nn.Parameter`s

        for which the value from the module is preserved.

        Default: ``False``

Returns:

    ``NamedTuple`` with ``missing_keys`` and ``unexpected_keys`` fields:

        * **missing_keys** is a list of str containing any keys that are expected

            by this module but missing from the provided ``state_dict``.

        * **unexpected_keys** is a list of str containing the keys that are not

            expected by this module but present in the provided ``state_dict``.

Note:

    If a parameter or buffer is registered as ``None`` and its corresponding key

    exists in :attr:`state_dict`, :meth:`load_state_dict` will raise a

    ``RuntimeError``.

##### 4.2.37 modules

[TOC](#table-of-contents)

**Description**

Return an iterator over all modules in the network.

Yields:

    Module: a module in the network

Note:

    Duplicate modules are returned only once. In the following

    example, ``l`` will be returned only once.

Example::

    >>> l = nn.Linear(2, 2)

    >>> net = nn.Sequential(l, l)

    >>> for idx, m in enumerate(net.modules()):

    ...     print(idx, '->', m)

    0 -> Sequential(

      (0): Linear(in_features=2, out_features=2, bias=True)

      (1): Linear(in_features=2, out_features=2, bias=True)

    )

    1 -> Linear(in_features=2, out_features=2, bias=True)

##### 4.2.38 mtia

[TOC](#table-of-contents)

**Description**

Move all model parameters and buffers to the MTIA.

This also makes associated parameters and buffers different objects. So

it should be called before constructing the optimizer if the module will

live on MTIA while being optimized.

.. note::

    This method modifies the module in-place.

Arguments:

    device (int, optional): if specified, all parameters will be

        copied to that device

Returns:

    Module: self

##### 4.2.39 named\_buffers

[TOC](#table-of-contents)

**Description**

Return an iterator over module buffers, yielding both the name of the buffer as well as the buffer itself.

Args:

    prefix (str): prefix to prepend to all buffer names.

    recurse (bool, optional): if True, then yields buffers of this module

        and all submodules. Otherwise, yields only buffers that

        are direct members of this module. Defaults to True.

    remove_duplicate (bool, optional): whether to remove the duplicated buffers in the result. Defaults to True.

Yields:

    (str, torch.Tensor): Tuple containing the name and buffer

Example::

    >>> # xdoctest: +SKIP("undefined vars")

    >>> for name, buf in self.named_buffers():

    >>>     if name in ['running_var']:

    >>>         print(buf.size())

##### 4.2.40 named\_children

[TOC](#table-of-contents)

**Description**

Return an iterator over immediate children modules, yielding both the name of the module as well as the module itself.

Yields:

    (str, Module): Tuple containing a name and child module

Example::

    >>> # xdoctest: +SKIP("undefined vars")

    >>> for name, module in model.named_children():

    >>>     if name in ['conv4', 'conv5']:

    >>>         print(module)

##### 4.2.41 named\_modules

[TOC](#table-of-contents)

**Description**

Return an iterator over all modules in the network, yielding both the name of the module as well as the module itself.

Args:

    memo: a memo to store the set of modules already added to the result

    prefix: a prefix that will be added to the name of the module

    remove_duplicate: whether to remove the duplicated module instances in the result

        or not

Yields:

    (str, Module): Tuple of name and module

Note:

    Duplicate modules are returned only once. In the following

    example, ``l`` will be returned only once.

Example::

    >>> l = nn.Linear(2, 2)

    >>> net = nn.Sequential(l, l)

    >>> for idx, m in enumerate(net.named_modules()):

    ...     print(idx, '->', m)

    0 -> ('', Sequential(

      (0): Linear(in_features=2, out_features=2, bias=True)

      (1): Linear(in_features=2, out_features=2, bias=True)

    ))

    1 -> ('0', Linear(in_features=2, out_features=2, bias=True))

##### 4.2.42 named\_parameters

[TOC](#table-of-contents)

**Description**

Return an iterator over module parameters, yielding both the name of the parameter as well as the parameter itself.

Args:

    prefix (str): prefix to prepend to all parameter names.

    recurse (bool): if True, then yields parameters of this module

        and all submodules. Otherwise, yields only parameters that

        are direct members of this module.

    remove_duplicate (bool, optional): whether to remove the duplicated

        parameters in the result. Defaults to True.

Yields:

    (str, Parameter): Tuple containing the name and parameter

Example::

    >>> # xdoctest: +SKIP("undefined vars")

    >>> for name, param in self.named_parameters():

    >>>     if name in ['bias']:

    >>>         print(param.size())

##### 4.2.43 parameters

[TOC](#table-of-contents)

**Description**

Return an iterator over module parameters.

This is typically passed to an optimizer.

Args:

    recurse (bool): if True, then yields parameters of this module

        and all submodules. Otherwise, yields only parameters that

        are direct members of this module.

Yields:

    Parameter: module parameter

Example::

    >>> # xdoctest: +SKIP("undefined vars")

    >>> for param in model.parameters():

    >>>     print(type(param), param.size())

    <class 'torch.Tensor'> (20L,)

    <class 'torch.Tensor'> (20L, 1L, 5L, 5L)

##### 4.2.44 register\_backward\_hook

[TOC](#table-of-contents)

**Description**

Register a backward hook on the module.

This function is deprecated in favor of :meth:`~torch.nn.Module.register_full_backward_hook` and

the behavior of this function will change in future versions.

Returns:

    :class:`torch.utils.hooks.RemovableHandle`:

        a handle that can be used to remove the added hook by calling

        ``handle.remove()``

##### 4.2.45 register\_buffer

[TOC](#table-of-contents)

**Description**

Add a buffer to the module.

This is typically used to register a buffer that should not to be

considered a model parameter. For example, BatchNorm's ``running_mean``

is not a parameter, but is part of the module's state. Buffers, by

default, are persistent and will be saved alongside parameters. This

behavior can be changed by setting :attr:`persistent` to ``False``. The

only difference between a persistent buffer and a non-persistent buffer

is that the latter will not be a part of this module's

:attr:`state_dict`.

Buffers can be accessed as attributes using given names.

Args:

    name (str): name of the buffer. The buffer can be accessed

        from this module using the given name

    tensor (Tensor or None): buffer to be registered. If ``None``, then operations

        that run on buffers, such as :attr:`cuda`, are ignored. If ``None``,

        the buffer is **not** included in the module's :attr:`state_dict`.

    persistent (bool): whether the buffer is part of this module's

        :attr:`state_dict`.

Example::

    >>> # xdoctest: +SKIP("undefined vars")

    >>> self.register_buffer('running_mean', torch.zeros(num_features))

##### 4.2.46 register\_forward\_hook

[TOC](#table-of-contents)

**Description**

Register a forward hook on the module.

The hook will be called every time after :func:`forward` has computed an output.

If ``with_kwargs`` is ``False`` or not specified, the input contains only

the positional arguments given to the module. Keyword arguments won't be

passed to the hooks and only to the ``forward``. The hook can modify the

output. It can modify the input inplace but it will not have effect on

forward since this is called after :func:`forward` is called. The hook

should have the following signature::

    hook(module, args, output) -> None or modified output

If ``with_kwargs`` is ``True``, the forward hook will be passed the

``kwargs`` given to the forward function and be expected to return the

output possibly modified. The hook should have the following signature::

    hook(module, args, kwargs, output) -> None or modified output

Args:

    hook (Callable): The user defined hook to be registered.

    prepend (bool): If ``True``, the provided ``hook`` will be fired

        before all existing ``forward`` hooks on this

        :class:`torch.nn.modules.Module`. Otherwise, the provided

        ``hook`` will be fired after all existing ``forward`` hooks on

        this :class:`torch.nn.modules.Module`. Note that global

        ``forward`` hooks registered with

        :func:`register_module_forward_hook` will fire before all hooks

        registered by this method.

        Default: ``False``

    with_kwargs (bool): If ``True``, the ``hook`` will be passed the

        kwargs given to the forward function.

        Default: ``False``

    always_call (bool): If ``True`` the ``hook`` will be run regardless of

        whether an exception is raised while calling the Module.

        Default: ``False``

Returns:

    :class:`torch.utils.hooks.RemovableHandle`:

        a handle that can be used to remove the added hook by calling

        ``handle.remove()``

##### 4.2.47 register\_forward\_pre\_hook

[TOC](#table-of-contents)

**Description**

Register a forward pre-hook on the module.

The hook will be called every time before :func:`forward` is invoked.

If ``with_kwargs`` is false or not specified, the input contains only

the positional arguments given to the module. Keyword arguments won't be

passed to the hooks and only to the ``forward``. The hook can modify the

input. User can either return a tuple or a single modified value in the

hook. We will wrap the value into a tuple if a single value is returned

(unless that value is already a tuple). The hook should have the

following signature::

    hook(module, args) -> None or modified input

If ``with_kwargs`` is true, the forward pre-hook will be passed the

kwargs given to the forward function. And if the hook modifies the

input, both the args and kwargs should be returned. The hook should have

the following signature::

    hook(module, args, kwargs) -> None or a tuple of modified input and kwargs

Args:

    hook (Callable): The user defined hook to be registered.

    prepend (bool): If true, the provided ``hook`` will be fired before

        all existing ``forward_pre`` hooks on this

        :class:`torch.nn.modules.Module`. Otherwise, the provided

        ``hook`` will be fired after all existing ``forward_pre`` hooks

        on this :class:`torch.nn.modules.Module`. Note that global

        ``forward_pre`` hooks registered with

        :func:`register_module_forward_pre_hook` will fire before all

        hooks registered by this method.

        Default: ``False``

    with_kwargs (bool): If true, the ``hook`` will be passed the kwargs

        given to the forward function.

        Default: ``False``

Returns:

    :class:`torch.utils.hooks.RemovableHandle`:

        a handle that can be used to remove the added hook by calling

        ``handle.remove()``

##### 4.2.48 register\_full\_backward\_hook

[TOC](#table-of-contents)

**Description**

Register a backward hook on the module.

The hook will be called every time the gradients with respect to a module

are computed, i.e. the hook will execute if and only if the gradients with

respect to module outputs are computed. The hook should have the following

signature::

    hook(module, grad_input, grad_output) -> tuple(Tensor) or None

The :attr:`grad_input` and :attr:`grad_output` are tuples that contain the gradients

with respect to the inputs and outputs respectively. The hook should

not modify its arguments, but it can optionally return a new gradient with

respect to the input that will be used in place of :attr:`grad_input` in

subsequent computations. :attr:`grad_input` will only correspond to the inputs given

as positional arguments and all kwarg arguments are ignored. Entries

in :attr:`grad_input` and :attr:`grad_output` will be ``None`` for all non-Tensor

arguments.

For technical reasons, when this hook is applied to a Module, its forward function will

receive a view of each Tensor passed to the Module. Similarly the caller will receive a view

of each Tensor returned by the Module's forward function.

.. warning ::

    Modifying inputs or outputs inplace is not allowed when using backward hooks and

    will raise an error.

Args:

    hook (Callable): The user-defined hook to be registered.

    prepend (bool): If true, the provided ``hook`` will be fired before

        all existing ``backward`` hooks on this

        :class:`torch.nn.modules.Module`. Otherwise, the provided

        ``hook`` will be fired after all existing ``backward`` hooks on

        this :class:`torch.nn.modules.Module`. Note that global

        ``backward`` hooks registered with

        :func:`register_module_full_backward_hook` will fire before

        all hooks registered by this method.

Returns:

    :class:`torch.utils.hooks.RemovableHandle`:

        a handle that can be used to remove the added hook by calling

        ``handle.remove()``

##### 4.2.49 register\_full\_backward\_pre\_hook

[TOC](#table-of-contents)

**Description**

Register a backward pre-hook on the module.

The hook will be called every time the gradients for the module are computed.

The hook should have the following signature::

    hook(module, grad_output) -> tuple[Tensor] or None

The :attr:`grad_output` is a tuple. The hook should

not modify its arguments, but it can optionally return a new gradient with

respect to the output that will be used in place of :attr:`grad_output` in

subsequent computations. Entries in :attr:`grad_output` will be ``None`` for

all non-Tensor arguments.

For technical reasons, when this hook is applied to a Module, its forward function will

receive a view of each Tensor passed to the Module. Similarly the caller will receive a view

of each Tensor returned by the Module's forward function.

.. warning ::

    Modifying inputs inplace is not allowed when using backward hooks and

    will raise an error.

Args:

    hook (Callable): The user-defined hook to be registered.

    prepend (bool): If true, the provided ``hook`` will be fired before

        all existing ``backward_pre`` hooks on this

        :class:`torch.nn.modules.Module`. Otherwise, the provided

        ``hook`` will be fired after all existing ``backward_pre`` hooks

        on this :class:`torch.nn.modules.Module`. Note that global

        ``backward_pre`` hooks registered with

        :func:`register_module_full_backward_pre_hook` will fire before

        all hooks registered by this method.

Returns:

    :class:`torch.utils.hooks.RemovableHandle`:

        a handle that can be used to remove the added hook by calling

        ``handle.remove()``

##### 4.2.50 register\_load\_state\_dict\_post\_hook

[TOC](#table-of-contents)

**Description**

Register a post-hook to be run after module's :meth:`~nn.Module.load_state_dict` is called.

It should have the following signature::

    hook(module, incompatible_keys) -> None

The ``module`` argument is the current module that this hook is registered

on, and the ``incompatible_keys`` argument is a ``NamedTuple`` consisting

of attributes ``missing_keys`` and ``unexpected_keys``. ``missing_keys``

is a ``list`` of ``str`` containing the missing keys and

``unexpected_keys`` is a ``list`` of ``str`` containing the unexpected keys.

The given incompatible_keys can be modified inplace if needed.

Note that the checks performed when calling :func:`load_state_dict` with

``strict=True`` are affected by modifications the hook makes to

``missing_keys`` or ``unexpected_keys``, as expected. Additions to either

set of keys will result in an error being thrown when ``strict=True``, and

clearing out both missing and unexpected keys will avoid an error.

Returns:

    :class:`torch.utils.hooks.RemovableHandle`:

        a handle that can be used to remove the added hook by calling

        ``handle.remove()``

##### 4.2.51 register\_load\_state\_dict\_pre\_hook

[TOC](#table-of-contents)

**Description**

Register a pre-hook to be run before module's :meth:`~nn.Module.load_state_dict` is called.

It should have the following signature::

    hook(module, state_dict, prefix, local_metadata, strict, missing_keys, unexpected_keys, error_msgs) -> None  # noqa: B950

Arguments:

    hook (Callable): Callable hook that will be invoked before

        loading the state dict.

##### 4.2.52 register\_module

[TOC](#table-of-contents)

**Description**

Alias for :func:`add_module`.

##### 4.2.53 register\_parameter

[TOC](#table-of-contents)

**Description**

Add a parameter to the module.

The parameter can be accessed as an attribute using given name.

Args:

    name (str): name of the parameter. The parameter can be accessed

        from this module using the given name

    param (Parameter or None): parameter to be added to the module. If

        ``None``, then operations that run on parameters, such as :attr:`cuda`,

        are ignored. If ``None``, the parameter is **not** included in the

        module's :attr:`state_dict`.

##### 4.2.54 register\_state\_dict\_post\_hook

[TOC](#table-of-contents)

**Description**

Register a post-hook for the :meth:`~torch.nn.Module.state_dict` method.

It should have the following signature::

    hook(module, state_dict, prefix, local_metadata) -> None

The registered hooks can modify the ``state_dict`` inplace.

##### 4.2.55 register\_state\_dict\_pre\_hook

[TOC](#table-of-contents)

**Description**

Register a pre-hook for the :meth:`~torch.nn.Module.state_dict` method.

It should have the following signature::

    hook(module, prefix, keep_vars) -> None

The registered hooks can be used to perform pre-processing before the ``state_dict``

call is made.

##### 4.2.56 requires\_grad\_

[TOC](#table-of-contents)

**Description**

Change if autograd should record operations on parameters in this module.

This method sets the parameters' :attr:`requires_grad` attributes

in-place.

This method is helpful for freezing part of the module for finetuning

or training parts of a model individually (e.g., GAN training).

See :ref:`locally-disable-grad-doc` for a comparison between

`.requires_grad_()` and several similar mechanisms that may be confused with it.

Args:

    requires_grad (bool): whether autograd should record operations on

                          parameters in this module. Default: ``True``.

Returns:

    Module: self

##### 4.2.57 set\_extra\_state

[TOC](#table-of-contents)

**Description**

Set extra state contained in the loaded `state_dict`.

This function is called from :func:`load_state_dict` to handle any extra state

found within the `state_dict`. Implement this function and a corresponding

:func:`get_extra_state` for your module if you need to store extra state within its

`state_dict`.

Args:

    state (dict): Extra state from the `state_dict`

##### 4.2.58 set\_submodule

[TOC](#table-of-contents)

**Description**

Set the submodule given by ``target`` if it exists, otherwise throw an error.

For example, let's say you have an ``nn.Module`` ``A`` that

looks like this:

.. code-block:: text

    A(

        (net_b): Module(

            (net_c): Module(

                (conv): Conv2d(16, 33, kernel_size=(3, 3), stride=(2, 2))

            )

            (linear): Linear(in_features=100, out_features=200, bias=True)

        )

    )

(The diagram shows an ``nn.Module`` ``A``. ``A`` has a nested

submodule ``net_b``, which itself has two submodules ``net_c``

and ``linear``. ``net_c`` then has a submodule ``conv``.)

To overide the ``Conv2d`` with a new submodule ``Linear``, you

would call

``set_submodule("net_b.net_c.conv", nn.Linear(33, 16))``.

Args:

    target: The fully-qualified string name of the submodule

        to look for. (See above example for how to specify a

        fully-qualified string.)

    module: The module to set the submodule to.

Raises:

    ValueError: If the target string is empty

    AttributeError: If the target string references an invalid

        path or resolves to something that is not an

        ``nn.Module``

##### 4.2.59 share\_memory

[TOC](#table-of-contents)

**Description**

See :meth:`torch.Tensor.share_memory_`.

##### 4.2.60 state\_dict

[TOC](#table-of-contents)

**Description**

Return a dictionary containing references to the whole state of the module.

Both parameters and persistent buffers (e.g. running averages) are

included. Keys are corresponding parameter and buffer names.

Parameters and buffers set to ``None`` are not included.

.. note::

    The returned object is a shallow copy. It contains references

    to the module's parameters and buffers.

.. warning::

    Currently ``state_dict()`` also accepts positional arguments for

    ``destination``, ``prefix`` and ``keep_vars`` in order. However,

    this is being deprecated and keyword arguments will be enforced in

    future releases.

.. warning::

    Please avoid the use of argument ``destination`` as it is not

    designed for end-users.

Args:

    destination (dict, optional): If provided, the state of module will

        be updated into the dict and the same object is returned.

        Otherwise, an ``OrderedDict`` will be created and returned.

        Default: ``None``.

    prefix (str, optional): a prefix added to parameter and buffer

        names to compose the keys in state_dict. Default: ``''``.

    keep_vars (bool, optional): by default the :class:`~torch.Tensor` s

        returned in the state dict are detached from autograd. If it's

        set to ``True``, detaching will not be performed.

        Default: ``False``.

Returns:

    dict:

        a dictionary containing a whole state of the module

Example::

    >>> # xdoctest: +SKIP("undefined vars")

    >>> module.state_dict().keys()

    ['bias', 'weight']

##### 4.2.61 to

[TOC](#table-of-contents)

**Description**

Move and/or cast the parameters and buffers.

This can be called as

.. function:: to(device=None, dtype=None, non_blocking=False)

   :noindex:

.. function:: to(dtype, non_blocking=False)

   :noindex:

.. function:: to(tensor, non_blocking=False)

   :noindex:

.. function:: to(memory_format=torch.channels_last)

   :noindex:

Its signature is similar to :meth:`torch.Tensor.to`, but only accepts

floating point or complex :attr:`dtype`\ s. In addition, this method will

only cast the floating point or complex parameters and buffers to :attr:`dtype`

(if given). The integral parameters and buffers will be moved

:attr:`device`, if that is given, but with dtypes unchanged. When

:attr:`non_blocking` is set, it tries to convert/move asynchronously

with respect to the host if possible, e.g., moving CPU Tensors with

pinned memory to CUDA devices.

See below for examples.

.. note::

    This method modifies the module in-place.

Args:

    device (:class:`torch.device`): the desired device of the parameters

        and buffers in this module

    dtype (:class:`torch.dtype`): the desired floating point or complex dtype of

        the parameters and buffers in this module

    tensor (torch.Tensor): Tensor whose dtype and device are the desired

        dtype and device for all parameters and buffers in this module

    memory_format (:class:`torch.memory_format`): the desired memory

        format for 4D parameters and buffers in this module (keyword

        only argument)

Returns:

    Module: self

Examples::

    >>> # xdoctest: +IGNORE_WANT("non-deterministic")

    >>> linear = nn.Linear(2, 2)

    >>> linear.weight

    Parameter containing:

    tensor([[ 0.1913, -0.3420],

            [-0.5113, -0.2325]])

    >>> linear.to(torch.double)

    Linear(in_features=2, out_features=2, bias=True)

    >>> linear.weight

    Parameter containing:

    tensor([[ 0.1913, -0.3420],

            [-0.5113, -0.2325]], dtype=torch.float64)

    >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_CUDA1)

    >>> gpu1 = torch.device("cuda:1")

    >>> linear.to(gpu1, dtype=torch.half, non_blocking=True)

    Linear(in_features=2, out_features=2, bias=True)

    >>> linear.weight

    Parameter containing:

    tensor([[ 0.1914, -0.3420],

            [-0.5112, -0.2324]], dtype=torch.float16, device='cuda:1')

    >>> cpu = torch.device("cpu")

    >>> linear.to(cpu)

    Linear(in_features=2, out_features=2, bias=True)

    >>> linear.weight

    Parameter containing:

    tensor([[ 0.1914, -0.3420],

            [-0.5112, -0.2324]], dtype=torch.float16)

    >>> linear = nn.Linear(2, 2, bias=None).to(torch.cdouble)

    >>> linear.weight

    Parameter containing:

    tensor([[ 0.3741+0.j,  0.2382+0.j],

            [ 0.5593+0.j, -0.4443+0.j]], dtype=torch.complex128)

    >>> linear(torch.ones(3, 2, dtype=torch.cdouble))

    tensor([[0.6122+0.j, 0.1150+0.j],

            [0.6122+0.j, 0.1150+0.j],

            [0.6122+0.j, 0.1150+0.j]], dtype=torch.complex128)

##### 4.2.62 to\_empty

[TOC](#table-of-contents)

**Description**

Move the parameters and buffers to the specified device without copying storage.

Args:

    device (:class:`torch.device`): The desired device of the parameters

        and buffers in this module.

    recurse (bool): Whether parameters and buffers of submodules should

        be recursively moved to the specified device.

Returns:

    Module: self

##### 4.2.63 train

[TOC](#table-of-contents)

**Description**

Set the module in training mode.

This has an effect only on certain modules. See the documentation of

particular modules for details of their behaviors in training/evaluation

mode, i.e., whether they are affected, e.g. :class:`Dropout`, :class:`BatchNorm`,

etc.

Args:

    mode (bool): whether to set training mode (``True``) or evaluation

                 mode (``False``). Default: ``True``.

Returns:

    Module: self

##### 4.2.64 type

[TOC](#table-of-contents)

**Description**

Casts all parameters and buffers to :attr:`dst_type`.

.. note::

    This method modifies the module in-place.

Args:

    dst_type (type or string): the desired type

Returns:

    Module: self

##### 4.2.65 xpu

[TOC](#table-of-contents)

**Description**

Move all model parameters and buffers to the XPU.

This also makes associated parameters and buffers different objects. So

it should be called before constructing optimizer if the module will

live on XPU while being optimized.

.. note::

    This method modifies the module in-place.

Arguments:

    device (int, optional): if specified, all parameters will be

        copied to that device

Returns:

    Module: self

##### 4.2.66 zero\_grad

[TOC](#table-of-contents)

**Description**

Reset gradients of all model parameters.

See similar function under :class:`torch.optim.Optimizer` for more context.

Args:

    set_to_none (bool): instead of setting to zero, set the grads to None.

        See :meth:`torch.optim.Optimizer.zero_grad` for details.

# 5 multi\_transforms

[TOC](#table-of-contents)

The module `rsp.ml.multi_transforms` is based on `torchvision.transforms`, which is made for single images. `rsp.ml.multi_transforms` extends this functionality by providing transformations for sequences of images, which could be usefull for video augmentation.

## 5.1 BGR2GRAY : MultiTransform

[TOC](#table-of-contents)

**Description**

Converts a sequence of BGR images to grayscale images.


### 5.1.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.1.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.2 BGR2RGB : MultiTransform

[TOC](#table-of-contents)

**Description**

Converts sequence of BGR images to RGB images.


### 5.2.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.2.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.3 Brightness : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 5.3.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.3.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.4 CenterCrop : MultiTransform

[TOC](#table-of-contents)

**Description**

Crops Images at the center after upscaling them. Dimensions kept the same.

![](documentation/image/multi_transforms.CenterCrop.png)


### 5.4.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.4.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| max_scale | float | Images are scaled randomly between 1. and max_scale before cropping to original size. |
## 5.5 Color : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 5.5.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.5.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.6 Compose : builtins.object

[TOC](#table-of-contents)

**Description**

Composes several MultiTransforms together.

**Example**

```python
import rsp.ml.multi_transforms as t

transforms = t.Compose([
  t.BGR2GRAY(),
  t.Scale(0.5)
])
```
### 5.6.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

### 5.6.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| children | List[MultiTransform] | List of MultiTransforms to compose. |
## 5.7 GaussianNoise : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 5.7.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.7.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.8 MultiTransform : builtins.object

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 5.8.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.8.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.9 Normalize : MultiTransform

[TOC](#table-of-contents)

**Description**

Normalize images with mean and standard deviation. Given mean: (mean[1],...,mean[n]) and std: (std[1],..,std[n]) for n channels, this transform will normalize each channel of the input torch.*Tensor i.e., output[channel] = (input[channel] - mean[channel]) / std[channel]

> Based on torchvision.transforms.Normalize


### 5.9.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.9.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| mean | List[float] | Sequence of means for each channel. |
| std | List[float] | Sequence of standard deviations for each channel. |
| inplace | bool | Set to True make this operation in-place. |
## 5.10 RGB2BGR : BGR2RGB

[TOC](#table-of-contents)

**Description**

Converts sequence of RGB images to BGR images.


### 5.10.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.10.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.11 RandomCrop : MultiTransform

[TOC](#table-of-contents)

**Description**

Crops Images at a random location after upscaling them. Dimensions kept the same.

![](documentation/image/multi_transforms.RandomCrop.png)


### 5.11.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.11.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| max_scale | float | Images are scaled randomly between 1. and max_scale before cropping to original size. |
## 5.12 RandomHorizontalFlip : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 5.12.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.12.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.13 RandomVerticalFlip : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 5.13.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.13.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.14 RemoveBackgroundAI : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 5.14.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.14.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.15 ReplaceBackground : MultiTransform

[TOC](#table-of-contents)

**Description**

Transformation for background replacement based on HSV values. Supports depth background replacement. backgrounds have to be passed as list of tuples of rgb and depth images.

**Example**

```python
from rsp.nl.dataset import TUCRID
import rsp.ml.multi_transforms as multi_transforms

USE_DEPTH_DATA = False
backgrounds = TUCRID.load_backgrounds(USE_DEPTH_DATA)
tranforms_train = multi_transforms.Compose([
    multi_transforms.ReplaceBackground(
        backgrounds = backgrounds,
        hsv_filter=[(69, 87, 139, 255, 52, 255)],
        p = 0.8
    ),
    multi_transforms.Stack()
])
tucrid = TUCRID('train', load_depth_data=USE_DEPTH_DATA, transforms=tranforms_train)

for X, T in tucrid:
    for x in X:
        img = x.permute(1, 2, 0).numpy()

        cv.imshow('img', img)
        cv.waitKey(30)
```
### 5.15.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.15.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Transformation for background replacement based on HSV values. Supports depth background replacement. backgrounds have to be passed as list of tuples of rgb and depth images.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| backgrounds | List[np.array] | List of background images |
| hsv_filter | List[tuple[int, int, int, int, int, int]] | List of HSV filters |
| p | float, default = 1. | Probability of applying the transformation |
| rotate | float, default = 5 | Maximum rotation angle |
| max_scale | float, default = 2 | Maximum scaling factor |
| max_noise | float, default = 0.002 | Maximum noise level |
## 5.16 Resize : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 5.16.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.16.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.17 Rotate : MultiTransform

[TOC](#table-of-contents)

**Description**

Randomly rotates images.

**Equations**

$angle = -max\_angle + 2 \cdot random() \cdot max\_angle$

![](documentation/image/multi_transforms.Rotate.png)


### 5.17.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.17.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Iitializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| max_angle | float | Maximal rotation in degrees | -max_angle <= rotate <= max_angle |
| auto_scale | bool, default = True | Image will be resized when auto scale is activated to avoid black margins. |
## 5.18 Satturation : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 5.18.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.18.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.19 Scale : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 5.19.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.19.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.20 Stack : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 5.20.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.20.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.21 ToCVImage : MultiTransform

[TOC](#table-of-contents)

**Description**

Converts a `torch.Tensor`to Open CV image by changing dimensions (d0, d1, d2) -> (d1, d2, d0) and converting `torch.Tensor` to `numpy`.


### 5.21.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.21.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.22 ToNumpy : MultiTransform

[TOC](#table-of-contents)

**Description**

Converts a `torch.Tensor`to `numpy`


### 5.22.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.22.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.23 ToPILImage : MultiTransform

[TOC](#table-of-contents)

**Description**

Converts sequence of images to sequence of `PIL.Image`.


### 5.23.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.23.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 5.24 ToTensor : MultiTransform

[TOC](#table-of-contents)

**Description**

Converts a sequence of images to torch.Tensor.


### 5.24.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 5.24.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

# 6 run

[TOC](#table-of-contents)

The module `rsp.ml.run` provides some tools for storing, loading and visualizing data during training of models using PyTorch. 

## 6.1 Run : builtins.object

[TOC](#table-of-contents)

**Description**

Run class to store and manage training

**Example**

```python
from rsp.ml.run import Run
import rsp.ml.metrics as m

metrics = [
    m.top_1_accuracy
]
config = {
    m.top_1_accuracy.__name__: {
        'ymin': 0,
        'ymax': 1
    }
}
run = Run(id='run0001', metrics=metrics, config=config, ignore_outliers_in_chart_scaling=True)

for epoch in range(100):
    """here goes some training code, giving us inputs, predictions and targets"""
    acc = m.top_1_accuracy(predictions, targets)
    run.append(m.top_1_accuracy.__name__, 'train', acc)
```
### 6.1.1 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Run class to store and manage training

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| id | str, default = None | Id of the run. If None, a new id is generated |
| moving_average_epochs | int, default = 1 | Number of epochs to average over |
| metrics | list, default = None | List of metrics to compute. Each metric should be a function that takes Y and T as input. |
| device | str, default = None | torch device to run on |
| ignore_outliers_in_chart_scaling | bool, default = False | Ignore outliers when scaling charts |
| config | dict, default = {} | Configuration dictionary. Keys are metric names and values are dictionaries with keys 'ymin' and 'ymax' |
### 6.1.2 append

[TOC](#table-of-contents)

**Description**

Append value to key in phase.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| key | str | Key to append to |
| phase | str | Phase to append to |
| value | float | Value to append |
### 6.1.3 get\_avg

[TOC](#table-of-contents)

**Description**

Get last average value of key in phase

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| key | str | Key to get |
| phase | str | Phase to get from |

**Returns**

Last average value of key in phase. If key is not in data, returns np.nan : value : float

### 6.1.4 get\_val

[TOC](#table-of-contents)

**Description**

Get last value of key in phase

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| key | str | Key to get |
| phase | str | Phase to get from |

**Returns**

Last value of key in phase. If key is not in data, returns np.nan : value : float

### 6.1.5 len

[TOC](#table-of-contents)

**Description**

Get length of longest phase

### 6.1.6 load\_best\_state\_dict

[TOC](#table-of-contents)

**Description**

Load best state_dict from runs/{id}/{fname}

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| model | torch.nn.Module | Model to load state_dict into |
| fname | str, default = 'state_dict.pt' | Filename to load from |
| verbose | bool, default = False | Print loaded file |
### 6.1.7 load\_state\_dict

[TOC](#table-of-contents)

**Description**

Load state_dict from runs/{id}/{fname}

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| model | torch.nn.Module | Model to load state_dict into |
| fname | str, default = None | Filename to load from |
### 6.1.8 pickle\_dump

[TOC](#table-of-contents)

**Description**

Pickle model to runs/{id}/{fname}

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| model | torch.nn.Module | Model to pickle |
| fname | str, default = 'model.pkl' | Filename to save to |
### 6.1.9 pickle\_load

[TOC](#table-of-contents)

**Description**

Load model from runs/{id}/{fname}

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| fname | str, default = 'model.pkl' | Filename to load from |
### 6.1.10 plot

[TOC](#table-of-contents)

**Description**

Plot all keys to runs/{id}/plot/{key}.jpg

### 6.1.11 recalculate\_moving\_average

[TOC](#table-of-contents)

**Description**

Recalculate moving average

### 6.1.12 save

[TOC](#table-of-contents)

**Description**

Save data to runs/{id}/data.json

### 6.1.13 save\_best\_state\_dict

[TOC](#table-of-contents)

**Description**

Save state_dict if new_acc is better than previous best

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| state_dict | dict | State dict to save |
| new_acc | float | New accuracy |
| epoch | int, default = None | Epoch to save |
| fname | str, default = 'state_dict.pt' | Filename to save to |
### 6.1.14 save\_state\_dict

[TOC](#table-of-contents)

**Description**

Save state_dict to runs/{id}/{fname}

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| state_dict | dict | State dict to save |
| fname | str, default = 'state_dict.pt' | Filename to save to |
### 6.1.15 train\_epoch

[TOC](#table-of-contents)

**Description**

Train one epoch.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| dataloader | DataLoader | DataLoader to train on |
| model | torch.nn.Module | Model to train |
| optimizer | torch.optim.Optimizer | Optimizer to use |
| criterion | torch.nn.Module | Criterion to use |
| num_batches | int, default = None | Number of batches to train on. If None, train on all batches |
| return_YT | bool, default = False | Append Y and T to results |

**Returns**

Dictionary with results : results : dict

### 6.1.16 validate\_epoch

[TOC](#table-of-contents)

**Description**

Validate one epoch.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| dataloader | DataLoader | DataLoader to validate on |
| model | torch.nn.Module | Model to validate |
| optimizer | torch.optim.Optimizer | Optimizer to use |
| criterion | torch.nn.Module | Criterion to use |
| num_batches | int, default = None | Number of batches to validate on. If None, validate on all batches |
| return_YT | bool, default = False | Append Y and T to results |

**Returns**

Dictionary with results : results : dict

