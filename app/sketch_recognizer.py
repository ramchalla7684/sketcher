import os
import sys
import numpy
from matplotlib import pyplot as plot
from sklearn.neighbors import NearestNeighbors

sys.path.append('../lib/caffe/python/')
import caffe

caffe.set_mode_gpu()

sketch_net = caffe.Net('../lib/caffe/models/triplet_googlenet/triplet_googlenet_sketch_deploy.prototxt', 
                       '../lib/caffe/models/triplet_googlenet/triplet_googlenet_finegrain.caffemodel',
                       caffe.TEST)

transformer = caffe.io.Transformer({'data': numpy.shape(sketch_net.blobs['data'].data)})

transformer.set_mean('data', numpy.load('../lib/caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1))
transformer.set_transpose('data', (2, 0, 1))
transformer.set_channel_swap('data', (2, 1, 0))
transformer.set_raw_scale('data', 255.0)

features = numpy.load('../data/features.npy')
images = numpy.load('../data/images.npy')

def recognize(sketch_path):
    sketch = transformer.preprocess('data', caffe.io.load_image(sketch_path))
    sketch_reshaped = numpy.reshape(sketch, sketch_net.blobs['data'].data.shape)

    features_sketch_all_layers = sketch_net.forward(data=sketch_reshaped)
    features_sketch_output_layer = numpy.copy(features_sketch_all_layers['pool5/7x7_s1_s'])

    k = 3
    neighbors = NearestNeighbors(
        n_neighbors=k, 
        algorithm='brute', 
        metric='cosine'
    ).fit(features)

    distances, indices = neighbors.kneighbors(numpy.reshape(features_sketch_output_layer, [numpy.shape(features_sketch_output_layer)[1]]).reshape(1, -1))

    result = []
    for i in range(k):
        result.append(images[indices[0][i]])

    return result