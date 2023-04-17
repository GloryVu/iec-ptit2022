#import tensorflow as tf
import os
import shutil

# from numba import cuda

# device = cuda.get_current_device()
# device.reset()
# os.environ["TF_FORCE_GPU_ALLOW_GROWTH"]="true"
# from IPython import get_ipython
# from models.research.object_detection import model_main
#model_main.main('run_once',checkpoint_dir='model.ckpt-30000', logtostderr=True
 #               ,model_dir='train',pipeline_config_path='models/research/object_detection/samples/configs/ssdlite_mobiledet_edgetpu_320x320_coco_sync_4x4.config')
def train_all():
  # os.chdir('retrain/')
  # os.system('conda activate tf115')
  if os.path.exists('retrain/all/train'):
    shutil.rmtree('retrain/all/train')
  print('Chuẩn bị dữ liệu ...')
  os.system('python retrain/models/research/object_detection/dataset_tools/create_pet_tf_record.py \
        --label_map_path="retrain/all/dataset/label_map.pbtxt" \
        --data_dir="retrain/all/dataset" \
        --output_dir="retrain/all/dataset"')
  # os.system('python retrain/models/research/object_detection/model_main.py')

  print('Huấn luyện mô hình ...')
  os.system(' python retrain/models/research/object_detection/model_main.py \
        --logtostderr=true \
        --model_dir=retrain/all/train \
        --pipeline_config_path=retrain/pipeline_config/config_all.config')

  print("Hoàn thành huấn luyện ...")
    # device = cuda.get_current_device()
    # device.reset()
    #get_ipython().system(' python models/research/object_detection/model_main.py      --logtostderr=true      --model_dir=train      --pipeline_config_path=models/research/object_detection/samples/configs/ssdlite_mobiledet_edgetpu_320x320_coco_sync_4x4.config')
  print("Xuất mô hình ...")
  os.chdir('retrain/all')
  os.system(' python ../models/research/object_detection/export_tflite_ssd_graph.py \
      --pipeline_config_path=../pipeline_config/config_smoke.config \
      --trained_checkpoint_prefix=train/model.ckpt-30000 \
      --output_directory= output_ssdlite_mobiledet \
      --add_postprocessing_op=true ')
  os.chdir('../')
  os.chdir('../')

    # Convert to a tflite file (for CPU)
  os.system(' tflite_convert \
      --output_file="retrain/all/output_ssdlite_mobiledet/all.tflite" \
      --graph_def_file="retrain/all/all.pb" \
      --inference_type=QUANTIZED_UINT8 \
      --input_arrays="normalized_input_image_tensor" \
      --output_arrays="TFLite_Detection_PostProcess,TFLite_Detection_PostProcess:1,TFLite_Detection_PostProcess:2,TFLite_Detection_PostProcess:3" \
      --mean_values=128 \
      --std_dev_values=128 \
      --input_shapes=1,320,320,3 \
      --allow_custom_ops')
  print('-----------------Done------------------')

def train_smoke():
  # os.chdir('retrain/')
  # os.system('conda activate tf115')
  if os.path.exists('retrain/smoke/train'):
    shutil.rmtree('retrain/smoke/train')
  print('Chuẩn bị dữ liệu ...')
  os.system('python retrain/models/research/object_detection/dataset_tools/create_pet_tf_record.py \
        --label_map_path="retrain/smoke/dataset/label_map.pbtxt" \
        --data_dir="retrain/smoke/dataset" \
        --output_dir="retrain/smoke/dataset"')
  # os.system('python retrain/models/research/object_detection/model_main.py')

  print('Huấn luyện mô hình ...')
  os.system(' python retrain/models/research/object_detection/model_main.py \
        --logtostderr=true \
        --model_dir=retrain/smoke/train \
        --pipeline_config_path=retrain/pipeline_config/config_smoke.config')

  print("Hoàn thành huấn luyện ...")
    # device = cuda.get_current_device()
    # device.reset()
    #get_ipython().system(' python models/research/object_detection/model_main.py      --logtostderr=true      --model_dir=train      --pipeline_config_path=models/research/object_detection/samples/configs/ssdlite_mobiledet_edgetpu_320x320_coco_sync_4x4.config')
  print("Xuất mô hình ...")
  os.chdir('retrain/smoke')
  os.system(' python ../models/research/object_detection/export_tflite_ssd_graph.py \
      --pipeline_config_path=../pipeline_config/config_smoke.config \
      --trained_checkpoint_prefix=train/model.ckpt-30000 \
      --output_directory= output_ssdlite_mobiledet \
      --add_postprocessing_op=true ')
  os.chdir('../')
  os.chdir('../')
    # os.system(' python retrain/models/research/object_detection/export_tflite_ssd_graph.py \
    #   --pipeline_config_path=retrain/pipeline_config/config_smoke.config \
    #   --trained_checkpoint_prefix=retrain/smoke/train/model.ckpt-30000 \
    #   --output_directory= retrain/smoke/output_ssdlite_mobiledet/ \
    #   --add_postprocessing_op=true ')


    # Convert to a tflite file (for CPU)
  os.system(' tflite_convert \
      --output_file="retrain/smoke/output_ssdlite_mobiledet/smoke.tflite" \
      --graph_def_file="tflite_graph.pb" \
      --inference_type=QUANTIZED_UINT8 \
      --input_arrays="normalized_input_image_tensor" \
      --output_arrays="TFLite_Detection_PostProcess,TFLite_Detection_PostProcess:1,TFLite_Detection_PostProcess:2,TFLite_Detection_PostProcess:3" \
      --mean_values=128 \
      --std_dev_values=128 \
      --input_shapes=1,320,320,3 \
      --allow_custom_ops')
  print('-----------------Done------------------')
def train_vacantland():
  # os.chdir('retrain/')
  # os.system('conda activate tf115')
  if os.path.exists('retrain/vacantland/train'):
    shutil.rmtree('retrain/vacantland/train')
  print('Chuẩn bị dữ liệu ...')
  os.system('python retrain/models/research/object_detection/dataset_tools/create_pet_tf_record.py \
        --label_map_path="retrain/vacantland/dataset/label_map.pbtxt" \
        --data_dir="retrain/vacantland/dataset" \
        --output_dir="retrain/vacantland/dataset"')
  # os.system('python retrain/models/research/object_detection/model_main.py')

  print('Huấn luyện mô hình ...')
  os.system(' python retrain/models/research/object_detection/model_main.py \
        --logtostderr=true \
        --model_dir=retrain/vacantland/train \
        --pipeline_config_path=retrain/pipeline_config/config_vacantland.config')

  print("Hoàn thành huấn luyện ...")
    # device = cuda.get_current_device()
    # device.reset()
    #get_ipython().system(' python models/research/object_detection/model_main.py      --logtostderr=true      --model_dir=train      --pipeline_config_path=models/research/object_detection/samples/configs/ssdlite_mobiledet_edgetpu_320x320_coco_sync_4x4.config')
  print("Xuất mô hình ...")
  os.chdir('retrain/vacantland')
  os.system(' python ../models/research/object_detection/export_tflite_ssd_graph.py \
      --pipeline_config_path=../pipeline_config/config_smoke.config \
      --trained_checkpoint_prefix=train/model.ckpt-30000 \
      --output_directory= output_ssdlite_mobiledet \
      --add_postprocessing_op=true ')
  os.chdir('../')
  os.chdir('../')

    # Convert to a tflite file (for CPU)
  os.system(' tflite_convert \
      --output_file="retrain/vacantland/output_ssdlite_mobiledet/vacantland.tflite" \
      --graph_def_file="retrain/vacantland/vacantland.pb" \
      --inference_type=QUANTIZED_UINT8 \
      --input_arrays="normalized_input_image_tensor" \
      --output_arrays="TFLite_Detection_PostProcess,TFLite_Detection_PostProcess:1,TFLite_Detection_PostProcess:2,TFLite_Detection_PostProcess:3" \
      --mean_values=128 \
      --std_dev_values=128 \
      --input_shapes=1,320,320,3 \
      --allow_custom_ops')
  print('-----------------Done------------------')
def train_foundationhouse():
  # os.chdir('retrain/')
  # os.system('conda activate tf115')
  if os.path.exists('retrain/foundationhouse/train'):
    shutil.rmtree('retrain/foundationhouse/train')
  print('Chuẩn bị dữ liệu ...')
  os.system('python retrain/models/research/object_detection/dataset_tools/create_pet_tf_record.py \
        --label_map_path="retrain/foundationhouse/dataset/label_map.pbtxt" \
        --data_dir="retrain/foundationhouse/dataset" \
        --output_dir="retrain/foundationhouse/dataset"')
  # os.system('python retrain/models/research/object_detection/model_main.py')

  print('Huấn luyện mô hình ...')
  os.system(' python retrain/models/research/object_detection/model_main.py \
        --logtostderr=true \
        --model_dir=retrain/foundationhouse/train \
        --pipeline_config_path=retrain/pipeline_config/config_foundationhouse.config')

  print("Hoàn thành huấn luyện ...")
    # device = cuda.get_current_device()
    # device.reset()
    #get_ipython().system(' python models/research/object_detection/model_main.py      --logtostderr=true      --model_dir=train      --pipeline_config_path=models/research/object_detection/samples/configs/ssdlite_mobiledet_edgetpu_320x320_coco_sync_4x4.config')
  print("Xuất mô hình ...")
  print("Xuất mô hình ...")
  os.chdir('retrain/foundationhouse')
  os.system(' python ../models/research/object_detection/export_tflite_ssd_graph.py \
      --pipeline_config_path=../pipeline_config/config_smoke.config \
      --trained_checkpoint_prefix=train/model.ckpt-30000 \
      --output_directory= output_ssdlite_mobiledet \
      --add_postprocessing_op=true ')
  os.chdir('../')
  os.chdir('../')


    # Convert to a tflite file (for CPU)
  os.system(' tflite_convert \
      --output_file="retrain/foundationhouse/output_ssdlite_mobiledet/foundationhouse.tflite" \
      --graph_def_file="retrain/foundationhouse/foundationhouse.pb" \
      --inference_type=QUANTIZED_UINT8 \
      --input_arrays="normalized_input_image_tensor" \
      --output_arrays="TFLite_Detection_PostProcess,TFLite_Detection_PostProcess:1,TFLite_Detection_PostProcess:2,TFLite_Detection_PostProcess:3" \
      --mean_values=128 \
      --std_dev_values=128 \
      --input_shapes=1,320,320,3 \
      --allow_custom_ops')
  print('-----------------Done------------------')
def train(type):
  if type == 0:
    train_smoke()
  elif type == 1:
    train_vacantland()
  elif type == 2:
    train_foundationhouse()
  elif type == 3:
    train_all()
if __name__ == '__main__':
    train_smoke()