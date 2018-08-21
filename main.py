import center_function as cf

from brain_target import *
from multiprocessing import Process, Queue



def do_work(array, result):
    running_version = 0
    Target = S1
    Target_name = 'S1'
    number_of_trandcucer = 1250

    for i in array:
        print('iteration now '+str(i))
        number_of_beamlines = i
        dummy  = cf.main_cal(running_version,Target,Target_name,number_of_trandcucer,number_of_beamlines)
    return dummy

if __name__ == "__main__":
    array = [10,20,30,40,50]
    array1 = [60,70,80,90,]
    array2 = [100,200]
    array3 = [300,400]
    array4 =  [500,600]
    array4 =  [700]
    array5 =  [800]
    array6 = [900]
    array7 = [1000]


    result = Queue()
    pr1 = Process(target=do_work,args=(array,result))
    pr2 = Process(target=do_work,args=(array1,result))
    pr3 = Process(target=do_work,args=(array3,result))
    pr4 = Process(target=do_work,args=(array4,result))
    pr5 = Process(target=do_work,args=(array5,result))
    pr6 = Process(target=do_work,args=(array6,result))
    pr7 = Process(target=do_work,args=(array7,result))
    pr8 = Process(target=do_work,args=(array2,result))


    pr1.start()
    pr2.start()
    pr3.start()
    pr4.start()
    pr5.start()
    pr6.start()
    pr7.start()
    pr8.start()


    pr1.join()
    pr2.join()
    pr3.join()
    pr4.join()
    pr5.join()
    pr6.join()
    pr7.join()
    pr8.join()

    result.put('STOP')
    sum = 0
