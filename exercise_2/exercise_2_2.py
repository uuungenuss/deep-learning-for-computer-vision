import logging
import numpy as np
import tensorflow as tf
from load_data import load_data, _file


def weight(shape):
    initial_weight = tf.truncated_normal(shape, stddev=.1)
    return tf.Variable(initial_weight)


def bias(shape):
    initial_bias = tf.constant(.1, shape=shape)
    return tf.Variable(initial_bias)


def conv2d(x, w):
    return tf.nn.conv2d(x, w, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def minibatches(inputs, targets, mbs, shuffle):

    if shuffle:
        idx = np.arange(len(inputs))
        np.random.shuffle(idx)
    for i in range(0, len(inputs) - mbs + 1, mbs):
        if shuffle:
            batch_idx = idx[i:i + mbs]
        else:
            batch_idx = slice(i, idx)
        yield inputs[batch_idx], targets[batch_idx]



def main(file):

    epochs = 60
    num_classes = 10
    mbs = 32

    logger.info('loading data from file  {}'.format(file))
    x_tr, y_tr, x_te, y_te = load_data(file, num_classes)
    logger.info('loading finished')

    x = tf.placeholder(tf.float32, [None, 784])
    y = tf.placeholder(tf.float32, [None, 10])
    w = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))

    w_conv1 = weight([5, 5, 1, 32])
    b_conv1 = bias([32])
    h_conv1 = tf.nn.relu(conv2d(x, w_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    w_conv2 = weight([5, 5, 32, 64])
    b_conv2 = bias([64])
    h_conv2 = tf.nn.relu(conv2d(h_pool1, w_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    w_fc = weight([7 * 7 * 64, 1024])
    b_fc = bias([1024])
    h_pool_fc = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
    h_fc = tf.nn.relu(tf.matmul(h_pool_fc, w_fc) + b_fc)

    w_out = weight([1024, 10])
    b_out = bias([10])

    pred = tf.matmul(h_fc, w_out) + b_out

    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=pred))
    train = tf.train.AdamOptimizer(1e-4).minimize(loss)
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    acc = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for e in epochs:
            for b in minibatches(x_tr, y_tr, mbs, shuffle=True):
                batch_x, batch_y = b
                sess.run(train, feed_dict={x: batch_x, y: batch_y})

    pass


if __name__ == '__main__':

    logger = logging.getLogger('ex2_2')
    logger.setLevel(logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())

    main(file=_file)