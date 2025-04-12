from . import tf

def get_list_from_path(ls_path, match_str = None):
    file_names = list()
    for path in ls_path:
        if match_str:
            query = path +"/*"+match_str+"*.tfrec"
        else:
            query = path +"/*.tfrec"            
        #print(query)
        file_names += tf.io.gfile.glob(query)
    return file_names

def inspect(tfrecPATH):
    ds_raw = tf.data.TFRecordDataset(tfrecPATH)
    for raw_record in ds_raw.take(1):
        example = tf.train.Example()
        example.ParseFromString(raw_record.numpy())

    tfrec_dtype = {}

    for key, feature in example.features.feature.items():
        kind = feature.WhichOneof('kind')
        tfrec_dtype[key] = kind

    return tfrec_dtype

def generate_format(dictionary_obj):
    tfrec_format= dict()
    for key, value in dictionary_obj.items():
        if value == "bytes_list":
            tfrec_format[key] = tf.io.FixedLenFeature([], tf.string)
        elif value == "int64_list":
            tfrec_format[key] = tf.io.FixedLenFeature([], tf.int64)
        # elif value == "float": #Not tested
        #     tfrec_format[key] = tf.io.FixedLenFeature([], tf.int64)
    return tfrec_format

def parse_image_classification_dataset(example, 
                                       TFREC_FORMAT,
                                       IMAGE_KEY):    
    example = tf.io.parse_single_example(example, TFREC_FORMAT)
    image = tf.io.decode_jpeg(example[IMAGE_KEY], 
                                           channels=3)
    example[IMAGE_KEY] = image_to_float(image)
    return example

def ImageClassificationDataset(ls_tfrecs, image_key = "image"):
    raw_dataset = tf.data.TFRecordDataset(ls_tfrecs)
    tfrec_dict = inspect(ls_tfrecs)
    tfrec_features = generate_format(tfrec_dict)
    image_ds = raw_dataset.map( lambda example: 
        parse_image_classification_dataset(example, 
    TFREC_FORMAT = tfrec_features,
    IMAGE_KEY =  image_key))
    return image_ds

def image_to_float(image_int):
    image = tf.cast(image_int, dtype = tf.float32) / 255.0
    return image

def get_image_and_label(example, 
                        LABEL_KEY,
                        IMAGE_KEY = 'image'):
    image = example[IMAGE_KEY]
    label = example[LABEL_KEY]
    return image, label
    



