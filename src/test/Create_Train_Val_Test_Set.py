#!---* coding: utf-8 --*--
#!/usr/bin/python
'''
Created on 2018年1月30日
将数据集随机分成训练集、验证集、测试集
@author: ljt
'''
import unittest
from PIL import Image, ImageFile
import random
import os, time
import logging
logger = logging.getLogger(__name__)
ImageFile.LOAD_TRUNCATED_IMAGES = True


class CreateDataSet:
      """
      创建train、val、test数据集
      """
      def __init__(self):
          pass
  

      @staticmethod
      def randNumber(li,num):
          temp_li=li
          res=random.sample(li,num)
          for i in res:
              temp_li.remove(i)
          #print ("res len=%d"%len(res))
          #print ("temp_li len=%d"%len(temp_li))
          return res,temp_li
          

      @staticmethod
      def openImage(image):
          return Image.open(image, mode="r")
 
      @staticmethod
      def saveImage(image, path):
          image.save(path)
 
 
def makeDir(path):
      try:
          if not os.path.exists(path):
                if not os.path.isfile(path):
                   # os.mkdir(path)
                    os.makedirs(path)
                    return 0
          else:
                return 1
      except Exception as e:
          print (str(e))
          return -2
 
 
def save(image, des_path, class_name,file_name): 
      temp_name=os.path.join(des_path,class_name)
      file_name=os.path.join(temp_name,file_name)
      CreateDataSet.saveImage(image, file_name)
 
 
is_create_test=0
ratio=0.1

def create(path, new_path):
      """
        多线程处理事务
        :param src_path: 资源文件
        :param des_path: 目的地文件
        :return:
      """
      train_sample_path=os.path.join(new_path, "train")
      val_sample_path=os.path.join(new_path, "val")
      test_sample_path=os.path.join(new_path, "test")

      if (os.path.isdir(new_path)):
          if makeDir(train_sample_path) == -1: 
               print ('create train dir failure')
               return -1    
          if makeDir(val_sample_path) == -1: 
               print ('create val dir failure')
               return -1   
          if(is_create_test==1):
               if makeDir(test_sample_path) == -1: 
                    print ('create test dir failure')
                    return -1    
      else:
          print ('the input param new_path is not the dir')
          return -1
      if os.path.isdir(path):
          class_names = os.listdir(path)
      else:
          print ('the input param path is not the dir')
          return -1
      for name in class_names:
          print ("process class name=%s"%name)
          tmp_class_name = os.path.join(path, name)
          val_sample_num=0;
          test_sample_num=0;
          val_total_sample_num=0;
          test_total_sample_num=0;
          if (os.path.isdir(tmp_class_name)):
                image_names=os.listdir(tmp_class_name)
                total=len(image_names)
                li = [i for i in range(total)] 
                val_total_sample_num=int(total*ratio)
                val_name_list,remain_list=CreateDataSet.randNumber(li,val_total_sample_num)
                if(is_create_test==1):
                      test_total_sample_num=int(total*ratio)    
                      test_name_list,remain_list=CreateDataSet.randNumber(remain_list,test_total_sample_num)
                #read val sample
                if makeDir(os.path.join(val_sample_path,name)) == -1: 
                    print ('create val class dir failure')
                    return -1 
                print ("val sample number=%d"%val_total_sample_num)
                #print val_name_list
                while(val_sample_num<val_total_sample_num):
                      index=val_name_list[val_sample_num]
                      temp_img_name=os.path.join(tmp_class_name,image_names[index])
                      if(os.path.isfile(temp_img_name)):
                            image = CreateDataSet.openImage(temp_img_name)
                            save(image,val_sample_path,name,image_names[index])
                      val_sample_num=val_sample_num+1
                #read  test sample
                if(is_create_test==1):
                      if makeDir(os.path.join(test_sample_path,name)) == -1: 
                           print ('create test class dir failure')
                           return -1 
                      print ("test sample number=%d"%test_total_sample_num)
                      #print test_name_list
                while(test_sample_num<test_total_sample_num):
                      index=test_name_list[test_sample_num]
                      temp_img_name=os.path.join(tmp_class_name,image_names[index])
                      if(os.path.isfile(temp_img_name)):
                            image = CreateDataSet.openImage(temp_img_name)
                            save(image,test_sample_path,name,image_names[index])
                      test_sample_num=test_sample_num+1
                #read train sample
                if makeDir(os.path.join(train_sample_path,name)) == -1: 
                    print ('create train class dir failure')
                    return -1 
                print ("train sample number=%d"%len(remain_list))
                #print remain_list
                for train in remain_list:
                      temp_img_name=os.path.join(tmp_class_name,image_names[train])
                      if(os.path.isfile(temp_img_name)):
                            image = CreateDataSet.openImage(temp_img_name)
                            save(image,train_sample_path,name,image_names[train])
                print ("finish")

class Test(unittest.TestCase):


    def testName(self):
        pass



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
#     unittest.main()
    create("H:\\Finetuning-899","H:\\Finetuning-899_new")
    