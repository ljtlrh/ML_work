# -*- coding:utf-8 -*-
from urllib.request import urlretrieve
import time,  random, os
import cv2

'''
1.数据预处理
首先，数据预处理分为两个部分，第一部分是读取图片，并划分训练集和测试集。因为整个数据集为6W张图片，所以我们可以让训练集为5W张，测试集为1W张。随后，虽然标签是文件名，我们认识，但是机器是不认识的，因此我们要使用text2vec，将标签进行向量化。明确了目的，那开始实践吧！
读取数据：
我们通过定义rate，来确定划分比例。例如：测试集1W张，训练集5W张，那么rate=1W/5W=0.2。
'''
def get_imgs(rate=0.2):
    """
    获取图片，并划分训练集和测试集
    Parameters:
      rate:测试集和训练集的比例，即测试集个数/训练集个数
    Returns:
      test_imgs:测试集
      test_labels:测试集标签
      train_imgs:训练集
      test_labels:训练集标签
    """
    data_path = './Discuz'
    # 读取图片
    imgs = os.listdir(data_path)
    # 打乱图片顺序
    random.shuffle(imgs)

    # 数据集总共个数
    imgs_num = len(imgs)
    # 按照比例求出测试集个数
    test_num = int(imgs_num * rate / (1 + rate))
    # 测试集
    test_imgs = imgs[:test_num]
    # 根据文件名获取测试集标签
    test_labels = list(map(lambda x: x.split('.')[0], test_imgs))
    # 训练集
    train_imgs = imgs[test_num:]
    # 根据文件名获取训练集标签
    train_labels = list(map(lambda x: x.split('.')[0], train_imgs))

    return test_imgs, test_labels, train_imgs, train_labels

'''
标签向量化：
既然需要将标签向量化，那么，我们也需要将向量化的标签还原回来。
这里我们包括了63个字符的转化，0-9 a-z A-Z _(验证码如果小于4，用_补齐)。
'''
import numpy as np
def text2vec(text):
    """
    文本转向量
    Parameters:
      text:文本
    Returns:
      vector:向量
    """
    if len(text) > 4:
        raise ValueError('验证码最长4个字符')

        vector = np.zeros(4 * 63)

    def char2pos(c):
        if c == '_':
            k = 62
            return k
        k = ord(c) - 48
        if k > 9:
            k = ord(c) - 55
            if k > 35:
                k = ord(c) - 61
                if k > 61:
                    raise ValueError('No Map')
        return k

    for i, c in enumerate(text):
        idx = i * 63 + char2pos(c)
        vector[idx] = 1
    return vector


def vec2text(vec):
    """
    向量转文本
    Parameters:
      vec:向量
    Returns:
      文本
    """
    char_pos = vec.nonzero()[0]
    text = []
    for i, c in enumerate(char_pos):
        char_at_pos = i  # c/63
        char_idx = c % 63
        if char_idx < 10:
            char_code = char_idx + ord('0')
        elif char_idx < 36:
            char_code = char_idx - 10 + ord('A')
        elif char_idx < 62:
            char_code = char_idx - 36 + ord('a')
        elif char_idx == 62:
            char_code = ord('_')
        else:
            raise ValueError('error')
        text.append(chr(char_code))
    return "".join(text)

'''

2.根据batch_size获取数据
我们在训练模型的时候，需要根据不同的batch_size"喂"数据。这就需要我们写个函数，从整体数据集中获取指定batch_size大小的数据。
下面代码无法运行，这是我封装到类里的函数，整体代码会在文末放出。现在理解下这代码，我们通过train_flag来确定是从训练集获取数据还是测试集获取数据，通过batch_size来获取指定大小的数据。获取数据之后，将batch_size大小的图片数据和经过向量化处理的标签存放到numpy数组中。
'''


def get_next_batch(self, train_flag=True, batch_size=100):
    """
    获得batch_size大小的数据集
    Parameters:
      batch_size:batch_size大小
      train_flag:是否从训练集获取数据
    Returns:
      batch_x:大小为batch_size的数据x
      batch_y:大小为batch_size的数据y
    """
    # 从训练集获取数据
    if train_flag == True:
        if (batch_size + self.train_ptr) < self.train_size:
            trains = self.train_imgs[self.train_ptr:(self.train_ptr + batch_size)]
            labels = self.train_labels[self.train_ptr:(self.train_ptr + batch_size)]
            self.train_ptr += batch_size
        else:
            new_ptr = (self.train_ptr + batch_size) % self.train_size
            trains = self.train_imgs[self.train_ptr:] + self.train_imgs[:new_ptr]
            labels = self.train_labels[self.train_ptr:] + self.train_labels[:new_ptr]
            self.train_ptr = new_ptr

        batch_x = np.zeros([batch_size, self.heigth * self.width])
        batch_y = np.zeros([batch_size, self.max_captcha * self.char_set_len])

        for index, train in enumerate(trains):
            img = np.mean(cv2.imread(self.data_path + train), -1)
            # 将多维降维1维
            batch_x[index, :] = img.flatten() / 255
        for index, label in enumerate(labels):
            batch_y[index, :] = self.text2vec(label)

    # 从测试集获取数据
    else:
        if (batch_size + self.test_ptr) < self.test_size:
            tests = self.test_imgs[self.test_ptr:(self.test_ptr + batch_size)]
            labels = self.test_labels[self.test_ptr:(self.test_ptr + batch_size)]
            self.test_ptr += batch_size
        else:
            new_ptr = (self.test_ptr + batch_size) % self.test_size
            tests = self.test_imgs[self.test_ptr:] + self.test_imgs[:new_ptr]
            labels = self.test_labels[self.test_ptr:] + self.test_labels[:new_ptr]
            self.test_ptr = new_ptr

        batch_x = np.zeros([batch_size, self.heigth * self.width])
        batch_y = np.zeros([batch_size, self.max_captcha * self.char_set_len])

        for index, test in enumerate(tests):
            img = np.mean(cv2.imread(self.data_path + test), -1)
            # 将多维降维1维
            batch_x[index, :] = img.flatten() / 255
        for index, label in enumerate(labels):
            batch_y[index, :] = self.text2vec(label)

    return batch_x, batch_y
'''
3.CNN模型

网络模型如下：3卷积层+1全链接层。
继续看下我封装到类里的函数：
'''


def crack_captcha_cnn(self, w_alpha=0.01, b_alpha=0.1):
    """
    定义CNN
    Parameters:
      w_alpha:权重系数
      b_alpha:偏置系数
    Returns:
      out:CNN输出
    """
    import tensorflow as tf
    # 卷积的input: 一个Tensor。数据维度是四维[batch, in_height, in_width, in_channels]
    # 具体含义是[batch大小, 图像高度, 图像宽度, 图像通道数]
    # 因为是灰度图，所以是单通道的[?, 100, 30, 1]
    x = tf.reshape(self.X, shape=[-1, self.heigth, self.width, 1])
    # 卷积的filter:一个Tensor。数据维度是四维[filter_height, filter_width, in_channels, out_channels]
    # 具体含义是[卷积核的高度, 卷积核的宽度, 图像通道数, 卷积核个数]
    w_c1 = tf.Variable(w_alpha * tf.random_normal([3, 3, 1, 32]))
    # 偏置项bias
    b_c1 = tf.Variable(b_alpha * tf.random_normal([32]))
    # conv2d卷积层输入:
    #  strides: 一个长度是4的一维整数类型数组，每一维度对应的是 input 中每一维的对应移动步数
    #  padding：一个字符串，取值为 SAME 或者 VALID 前者使得卷积后图像尺寸不变, 后者尺寸变化
    # conv2d卷积层输出:
    #   一个四维的Tensor, 数据维度为 [batch, out_width, out_height, in_channels * out_channels]
    #  [?, 100, 30, 32]
    #   输出计算公式H0 = (H - F + 2 * P) / S + 1
    #    对于本卷积层而言,因为padding为SAME,所以P为1。
    #  其中H为图像高度,F为卷积核高度,P为边填充,S为步长
    # 学习参数:
    #  32*(3*3+1)=320
    # 连接个数:
    #  100*30*30*100=9000000个连接

    # bias_add:将偏差项bias加到value上。这个操作可以看做是tf.add的一个特例，其中bias是必须的一维。
    # 该API支持广播形式，因此value可以是任何维度。但是，该API又不像tf.add，可以让bias的维度和value的最后一维不同，
    conv1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(x, w_c1, strides=[1, 1, 1, 1], padding='SAME'), b_c1))
    # max_pool池化层输入：
    #  ksize:池化窗口的大小，取一个四维向量，一般是[1, height, width, 1]
    #    因为我们不想在batch和channels上做池化，所以这两个维度设为了1
    #  strides:和卷积类似，窗口在每一个维度上滑动的步长，一般也是[1, stride,stride, 1]
    #  padding:和卷积类似，可以取'VALID' 或者'SAME'
    # max_pool池化层输出：
    #  返回一个Tensor，类型不变，shape仍然是[batch, out_width, out_height, in_channels]这种形式
    #   [?, 50, 15, 32]
    # 学习参数:
    #  2*32
    # 连接个数:
    #  15*50*32*(2*2+1)=120000
    conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    w_c2 = tf.Variable(w_alpha * tf.random_normal([3, 3, 32, 64]))
    b_c2 = tf.Variable(b_alpha * tf.random_normal([64]))
    # [?, 50, 15, 64]
    conv2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv1, w_c2, strides=[1, 1, 1, 1], padding='SAME'), b_c2))
    # [?, 25, 8, 64]
    conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    w_c3 = tf.Variable(w_alpha * tf.random_normal([3, 3, 64, 64]))
    b_c3 = tf.Variable(b_alpha * tf.random_normal([64]))
    # [?, 25, 8, 64]
    conv3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv2, w_c3, strides=[1, 1, 1, 1], padding='SAME'), b_c3))
    # [?, 13, 4, 64]
    conv3 = tf.nn.max_pool(conv3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    # [3328, 1024]
    w_d = tf.Variable(w_alpha * tf.random_normal([4 * 13 * 64, 1024]))
    b_d = tf.Variable(b_alpha * tf.random_normal([1024]))
    # [?, 3328]
    dense = tf.reshape(conv3, [-1, w_d.get_shape().as_list()[0]])
    # [?, 1024]
    dense = tf.nn.relu(tf.add(tf.matmul(dense, w_d), b_d))
    dense = tf.nn.dropout(dense, self.keep_prob)
    # [1024, 63*4=252]
    w_out = tf.Variable(w_alpha * tf.random_normal([1024, self.max_captcha * self.char_set_len]))

    b_out = tf.Variable(b_alpha * tf.random_normal([self.max_captcha * self.char_set_len]))
    # [?, 252]
    out = tf.add(tf.matmul(dense, w_out), b_out)
    return out
'''
4.训练函数

准备工作都做好了，我们就可以开始训练了。
'''


def train_crack_captcha_cnn(self):
    """
    训练函数
    """
    output = self.crack_captcha_cnn()

    # 创建损失函数
    # loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=output, labels=self.Y))
    diff = tf.nn.sigmoid_cross_entropy_with_logits(logits=output, labels=self.Y)
    loss = tf.reduce_mean(diff)
    tf.summary.scalar('loss', loss)

    # 使用AdamOptimizer优化器训练模型，最小化交叉熵损失
    optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

    # 计算准确率
    y = tf.reshape(output, [-1, self.max_captcha, self.char_set_len])
    y_ = tf.reshape(self.Y, [-1, self.max_captcha, self.char_set_len])
    correct_pred = tf.equal(tf.argmax(y, 2), tf.argmax(y_, 2))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
    tf.summary.scalar('accuracy', accuracy)

    merged = tf.summary.merge_all()
    saver = tf.train.Saver()
    with tf.Session(config=self.config) as sess:
        # 写到指定的磁盘路径中
        train_writer = tf.summary.FileWriter(self.log_dir + '/train', sess.graph)
        test_writer = tf.summary.FileWriter(self.log_dir + '/test')
        sess.run(tf.global_variables_initializer())

        # 遍历self.max_steps次
        for i in range(self.max_steps):
            # 迭代500次，打乱一下数据集
            if i % 499 == 0:
                self.test_imgs, self.test_labels, self.train_imgs, self.train_labels = self.get_imgs()
            # 每10次，使用测试集，测试一下准确率
            if i % 10 == 0:
                batch_x_test, batch_y_test = self.get_next_batch(False, 100)
                summary, acc = sess.run([merged, accuracy],
                                        feed_dict={self.X: batch_x_test, self.Y: batch_y_test, self.keep_prob: 1})
                print('迭代第%d次 accuracy:%f' % (i + 1, acc))
                test_writer.add_summary(summary, i)

                # 如果准确率大于90%，则保存模型并退出。
                if acc > 0.90:
                    train_writer.close()
                    test_writer.close()
                    saver.save(sess, "crack_capcha.model", global_step=i)
                    break
            # 一直训练,不实用dropout
            else:
                batch_x, batch_y = self.get_next_batch(True, 100)
                loss_value, _ = sess.run([loss, optimizer],
                                         feed_dict={self.X: batch_x, self.Y: batch_y, self.keep_prob: 1})
                print('迭代第%d次 loss:%f' % (i + 1, loss_value))
                curve = sess.run(merged, feed_dict={self.X: batch_x_test, self.Y: batch_y_test, self.keep_prob: 1})
                train_writer.add_summary(curve, i)

        train_writer.close()
        test_writer.close()
        saver.save(sess, "crack_capcha.model", global_step=self.max_steps)

if __name__ == '__main__':
    print(text2vec('abcd'))
    print(vec2text(text2vec('abcd')))