import center_function as cf

from brain_target import *
from multiprocessing import Process, Queue



def do_work(array, result):
    running_version = 0
    Target = S1_re
    Target_name = 'S1'
    number_of_trandcucer = 1200

    for i in array:
        print('iteration now '+str(i))
        number_of_beamlines = i
        dummy  = cf.main_cal(running_version,Target,Target_name,number_of_trandcucer,number_of_beamlines)
    return dummy

if __name__ == "__main__":
    array = [10,20,30,40]
    array2 = [50,60,70,80,90]
    array3 = [100,200,300,400,500]
    array4 =  [600,700,800,900,1000]


    result = Queue()
    pr1 = Process(target=do_work,args=(array,result))
    pr2 = Process(target=do_work,args=(array2,result))
    pr3 = Process(target=do_work,args=(array3,result))
    pr4 = Process(target=do_work,args=(array4,result))
    pr1.start()
    pr2.start()
    pr3.start()
    pr4.start()
    pr1.join()
    pr2.join()
    pr3.join()
    pr4.join()
    result.put('STOP')
    sum = 0
