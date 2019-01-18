import numpy as np
from sympy import *
import math
import start
import pandas as pd

RATE=0.3
class Sim:

    def __init__(self,training_data_path,testing_data_path):
        self.starter = start.Starter()
        self.w=np.random.random(11)
        self.c=np.random.random()
        self.training_data_matrix=np.loadtxt(training_data_path)
        self.testing_data_matrix = np.loadtxt(testing_data_path)
    def cal_sim_function(self,report_id_1,report_id_2):
        dict=self.starter.calculate(int(report_id_1),int(report_id_2))
        w1 = symbols("w1")
        w2 = symbols("w2")
        w3 = symbols("w3")
        w4 = symbols("w4")
        w5 = symbols("w5")
        w6 = symbols("w6")
        w7 = symbols("w7")
        w8 = symbols("w8")
        w9 = symbols("w9")
        w10 = symbols("w10")
        w11 = symbols("w11")
        sim=dict['exception']*w1+dict['field_isdup']*w2+dict['field_dup_index']*w3+dict[ 'field_deep']*w4+dict['field_length']*w5+dict['field_interest_issame']*w6+dict['field_interest_length']*w7+dict['callstack_inner']*w8+dict['callstack_outer_1']*w9+dict['callstack_outer_2']*w10+dict[ 'callstack_all']*w11
        return sim

    def cal_sim(self,sim_function):
        return sim_function.subs('w1', self.w[0]).subs('w2', self.w[1]).subs('w3', self.w[2]).subs('w4', self.w[3]).subs('w5',
                                                                                                                 self.w[
                                                                                                                     4]).subs(
            'w6', self.w[5]).subs('w7', self.w[6]).subs('w8', self.w[7]).subs('w9', self.w[8]).subs('w10',
                                                                                                    self.w[9]).subs(
            'w11', self.w[10])
    def get_RNC(self,i):
        sima=self.cal_sim_function(i[2],i[0])
        simb=self.cal_sim_function(i[1],i[0])
        Y=sima-simb
        q=1+pow(math.e,Y)

        return log(q),(self.cal_sim(sima)+self.cal_sim(simb))/2

    def diff_RNC(self,RNC,x):
        dify = diff(RNC,x)  # 求导
        return dify.subs('w1', self.w[0]).subs('w2', self.w[1]).subs('w3', self.w[2]).subs('w4', self.w[3]).subs('w5', self.w[4]).subs('w6', self.w[5]).subs('w7', self.w[6]).subs('w8', self.w[7]).subs('w9', self.w[8]).subs('w10', self.w[9]).subs('w11', self.w[10])



    def do_w_tranning(self):
        it=0.01
        learning_rate=RATE
        count=0
        for i in self.training_data_matrix:
            it += 0.01
            count += 1
            print('进度',count/len(self.training_data_matrix))
            learning_rate=pow(0.99,it)*learning_rate
            RNC,threshold=self.get_RNC(i)
            for j in range(11):
                self.w[j]=self.w[j]-learning_rate*self.diff_RNC(RNC,"w%s"%(str(j+1)))
            if self.c<threshold:
                self.c=self.c+0.01*(threshold-self.c)
            else:
                self.c = self.c - 0.01 * (self.c-threshold)
            print(self.w)
            print(self.c)


    def judge(self,i,j):
        sim=self.cal_sim(self.cal_sim_function(i,j))
        if  sim>= self.c:
            return 1
        else:
            return 0


    def testing(self):
        totle_size=0
        right_num=0
        for i in self.testing_data_matrix:
            if self.cal_sim(self.cal_sim_function(i[0],i[1]))>=self.c:
                right_num+=1

            if self.cal_sim(self.cal_sim_function(i[0],i[2]))<self.c:
                right_num+=1
            totle_size+=2

        return right_num/totle_size

    def form_csv(self,path):
        arr=np.loadtxt(path)
        result=[]
        for i in range(len(arr)):
            print(i)
            for j in range(i+1,len(arr)):
                a=[]
                a.append(arr[i])
                a.append(arr[j])
                a.append(self.judge(arr[i],arr[j]))
                result.append(a)
        data1 = pd.DataFrame(result)
        data1.to_csv('data.csv')
        print(data1)

def main():
    sim= Sim('./sim_data/traning.txt','./sim_data/testing.txt')
    sim.do_w_tranning()
    print(sim.testing())
    sim.form_csv('../../dataset/true_data.txt')


main()
