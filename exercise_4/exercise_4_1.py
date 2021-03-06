import numpy as np
import tensorflow as tf

def calc_values(inp, out):
    strides = []
    for i in range(2, 10):
        for j in range(2, 10):
            x = np.floor(((np.floor((inp - 1) / i) + 1) - 1) / j) + 1
            if x == out:
                if inp == 64:
                    strides.append((i, j))
                    print('x3: {}, x7: {}'.format(i, j))
                elif inp == 48:
                    strides.append((i, j))
                    print('x4: {}, x8: {}'.format(i, j))
    return strides

# if this function doesn't crash/throw an exception given values are valid
def val_values(x3, x4, x7, x8):

    inp = np.ones(shape=(1, 64, 48, 17))
    out = np.zeros(shape=(1, 11, 4, 13))

    x1 = 17
    x2 = x5 = 15
    x6 = 13

    x = tf.placeholder(np.float32, [None, 64, 48, 17])
    y = tf.placeholder(np.float32, [None, 11, 4, 13])

    W1 = tf.Variable(tf.zeros([3, 3, x1, x2]))
    layer1 = tf.nn.conv2d(x, W1, strides=[1, x3, x4, 1], padding='SAME')
    W2 = tf.Variable(tf.zeros([3, 3, x5, x6]))
    layer2 = tf.nn.conv2d(layer1, W2, strides=[1, x7, x8, 1], padding='SAME')

    output = layer2 + y

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        _ = sess.run(output, feed_dict={x:inp, y:out})


def ex_4_1a():
    strides_y = calc_values(64,11)
    strides_x = calc_values(48, 4)

    for y in strides_y:
        for x in strides_x:
            val_values(y[0], x[0], y[1], x[1])

'''
when using conv2d_transpose one has to define the desired output shape, because as u can see in the formula one has to floor.
for example:

stride = 2

np.floor((64 - 1) / stride) + 1 = 32
and so is
np.floor((65 - 1) / stride) + 1 = 32

so you could have shape 64 or 65 in matters of exercise 4.1
'''
def ex_4_1b():

    inp = np.ones(shape=(1, 64, 48, 17))
    out = np.zeros(shape=(1, 64, 48, 17))

    x = tf.placeholder(np.float32, [1, 64, 48, 17])
    y = tf.placeholder(np.float32, [1, 64, 48, 17])

    # encoder
    W1 = tf.Variable(tf.zeros([3, 3, 17, 15]))
    layer1 = tf.nn.conv2d(x, W1, strides=[1, 2, 3, 1], padding='SAME')
    W2 = tf.Variable(tf.zeros([3, 3, 15, 13]))
    layer2 = tf.nn.conv2d(layer1, W2, strides=[1, 3, 4, 1], padding='SAME')

    # decoder
    W3 = tf.Variable(tf.zeros([3, 3, 15, 13]))
    layer3 = tf.nn.conv2d_transpose(layer2, W3, output_shape=[1, 32, 16, 15],strides=[1, 3, 4, 1], padding='SAME')
    W4 = tf.Variable(tf.zeros([3, 3, 17, 15]))
    layer4 = tf.nn.conv2d_transpose(layer3, W4, output_shape=[1, 64, 48, 17], strides=[1, 2, 3, 1], padding='SAME')

    output = layer4 + y

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        _ = sess.run(output, feed_dict={x:inp, y:out})

if __name__ == '__main__':
    # ex_4_1a()
    ex_4_1b()