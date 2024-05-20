from bs4 import BeautifulSoup

def parse_page(content):
    ret =  []

    soup = BeautifulSoup(content, "html.parser")
    thread_list = soup.find_all("table", {"class": "tborder clear"})
    assert(len(thread_list)==1)
    threads = thread_list[0].find_all("tr", {"class": "inline_row"})
    assert(len(threads))

    for thread in threads:
        thread_data = {}
        title_tmp = thread.find_all("span", {"class": "subject_new"})
        if len(title_tmp) != 1:
            continue
        thread_data["title"] = title_tmp[0].getText().strip()
        thread_data["author"] = thread.find("span", {"class": "author smalltext"}).find("span").getText().strip()
        tmp = thread.find("span", {"class": "forum-display__thread-date"})
        if tmp.find("span"):
            thread_data["posted_at"] = thread.find("span", {"class": "forum-display__thread-date"}).find("span")["title"].strip()
        else:
            thread_data["posted_at"] = tmp.getText().strip()
        thread_data["id"] = int(title_tmp[0]["id"].split("_")[1])
        thread_data["link"] = "https://breached.vc/"+thread.find("a")["href"]
        ret.append(thread_data)

    return ret