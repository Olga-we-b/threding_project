import concurrent
import time
import concurrent.futures as futures

start = time.time()
def do_something(seconds):
    print("Going to sleep")
    time.sleep(seconds)
    return "Done sleeping"

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(do_something, 1) for _ in range(10)]
    for f in concurrent.futures.as_completed(results):
        print(f.result())

finish = time.time()
f_time = round(finish - start, 2)
print("Finished in {} seconds".format(f_time))