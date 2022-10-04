import threading, time
import multiprocessing

class Worker(threading.Thread):
    def __init__(self, jobs, output, id):
        threading.Thread.__init__(self)
        self.jobs = jobs
        self.output = output
        self.id = id

    def run(self):
        while not self.jobs.empty():
            t = time.time()
            job = self.jobs.get()
            name, method, path = job[0], job[1], job[2]
            chart = method()
            chart.render_to_file(job[2])
            self.output[name] = path+"?cache="+str(t)
            self.jobs.task_done()
            
def mp_Worker(proc_id, job, return_dict):
    #while not jobs.empty():
    name, method, path = job[0], job[1], job[2]
    chart = method()
    chart.render_to_file(job[2])
    return_dict[name] = path+"?cache="+str(time.time())