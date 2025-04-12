# ebench

**Ebench** is a modular and extensible benchmarking framework for evaluating image and video enhancement models. It supports inference, evaluation, and dataset tagging management while ensuring a structured workflow for fair and reproducible comparisons.

## Usage

Ebench conducts a minimum development granularity evaluation and analysis for different usage scenarios.

All proceduer follow below pipeline:

1. prepare benchmark videos/images or using existed sets;
    - ps: the video will together to yield a image by using first frame
2. submit your enhancement videos or select enhancement algorithm;
3. select index to split dataset, select evaluators, select enhancement to compare;
4. download or view your report.

```bash
# set environment variables
export THEA_ROOT=/cephFS/video_lab/thirdparty/thea-release
export LD_LIBRARY_PATH=$THEA_ROOT/lib:$THEA_ROOT/thirdparty/cuda/lib:$THEA_ROOT/thirdparty/cudnn/lib:$THEA_ROOT/thirdparty/dodo/lib:$THEA_ROOT/thirdparty/eagle/lib:$THEA_ROOT/thirdparty/eagle/thirdparty/opencv/lib:$THEA_ROOT/thirdparty/falcon/lib:$THEA_ROOT/thirdparty/openvino/lib/intel64:$THEA_ROOT/thirdparty/openvino/3rdparty/tbb/lib:$THEA_ROOT/thirdparty/tensorrt/lib:$LD_LIBRARY_PATH
```

### 1. prepare datasets

- search all videos and images
- zip them into a package for download
- it will put all data into local folder and make a filelist

```bash
python -m ebench.dataset -t prepare -f /cephFS/yangying/VSR2024/assets/faceratio_bigolive_videos -d face0409
```

- tagging dataset by using evaluators
- it will yield a list with each item with a tagging file

```bash
# initialize the dataset
python -m ebench.dataset -t tag -n face0409 -e vqa_v4_4
# add more tag or update tag
python -m ebench.dataset -t tag -n face0409 -e vsc_v4
```

- check dataset information

```bash
python -m ebench.dataset -t view -n face0409
```

### 2. evaluate enhancement videos

- submit your enhancement result according to dataset format
- pay attention to keep same folder structure with datasets

```bash
python -m ebench.dataset -t prepare -f /cephFS/yangying/VSR2024/assets/faceratio_bigolive_videos_bfsr48 -d face0409_bfsr48
python -m ebench.dataset -t tag -n face0409_bfsr48 -e vqa_v4_4
python -m ebench.dataset -t view -n face0409_bfsr48
```

### 3. compare your dataset with baseline

- splits dataset into different parts according to specific tagging info
- select evaluator indices to compare, the order will be:
    - (bench.ind1, enh1.ind1, enh2.ind1), (bench.ind2, enh1.ind2, enh2.ind2), ...
- yield a csv file with current timestamp: 202504091619.csv

```bash
python -m ebench -t compare -n dataset dataset_vls_v2 dataset_vls_v3 -s vqa.y -e vqa.qs_tech vqa.qs_tech_fg vqa.qs_tech_face
```

### 4. use pre-defined enhancement algorithm

- using step4 method to generate an enhanced dataset (skip step2)

```bash
# using thea binary to generate enhanced results
python -m ebench.predict -t thea -n face0409 -d face0409_vls_v2 -m thea_demo_vls_v2
```

### 5. summary the results using AI-report

- 

### 6. start a web service to check

```bash
python -m ebench -t app -p 8811
```


```bash
```

## Supports

### 1. pre-defined datasets

### 2. pre-defined algorithms

### 3. pre-defined evaluators
