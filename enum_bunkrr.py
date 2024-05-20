import requests
import threading
import re
from tqdm import tqdm
import queue
regex=re.compile(r"<a href=\"(.*?)(?:\"|\?download=true\")")
#session=requests.Session()
def get(id:int,session):
    resp=session.get(f"https://get.bunkrr.su/file/{id}")
    if resp.status_code==404:
        return id,[]
    return id,regex.findall(resp.text)

THREADS=30
LOCK=threading.Lock()
QUEUE=queue.Queue()
start=int(open("start.txt").read().strip())
pbar=tqdm(total=start)
pbar_good=tqdm()

def worker():
    global start
    session=requests.Session()
    while start>0:
        with LOCK:
            if start<0:
                break
            start-=1
            value=start
        if value%1000==0:
            #pbar.update(1000)
            with open("start.txt","w") as f:
                f.write(str(value))
        pbar.update(1)
        id,links=get(value,session)
        for link in links:
            QUEUE.put((id,link))

END_writer=False
def writer():
    out_file=open("links.txt","a")
    e=0
    while not END_writer or not QUEUE.empty():
        id,link=QUEUE.get()
        out_file.write(f"{id} {link}\n")
        e+=1
        if e%100==0:
            out_file.flush()
        pbar_good.update(1)

threads=[]
for _ in range(THREADS):
    threads.append(threading.Thread(target=worker))
    threads[-1].start()

writer_thread=threading.Thread(target=writer)
writer_thread.start()

for thread in threads:
    thread.join()

END_writer=True
writer_thread.join()