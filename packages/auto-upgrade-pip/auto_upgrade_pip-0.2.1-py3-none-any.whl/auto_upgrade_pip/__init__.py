import os
from pathlib import Path

__version__ = "0.2.1"
__all__ = ["auto", "customize", "manual"]

folder = Path(__file__).parent.resolve()
path = os.path.join(folder, "cache")

def auto():
    if os.path.exists(path):
        os.remove(path)

    os.system("pip list > "+str(path))
    with open(path,"r",encoding = "utf-8") as file:
        req = file.readlines()[2:]

    write = []

    for i in req:
        write.append(i.split(" ")[0]+"\n")

    with open(path,"w",encoding = "utf-8") as file:
        file.writelines(write)

    os.system("python -m pip install --upgrade -r "+str(path)+" -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.remove(path)

def manual():
    from time import time

    news = "\n\tAdd the customize mode.\n\tRename the select to manual."
    print(f"{'auto-upgrade-pip Version:'+__version__:#^60}\n\nNews: {news}")

    os.system("pause")

    retain = True

    create_cache = time()
    
    if os.path.exists(path):
        while True:
            i = input("Cache is found.Whether to keep：\n\tY:Keep(Need create cache,but unsafty.)\n\tN:Not keep(Need create cache,but safty.):")

            if i.upper() == "N":
                os.remove(path)
                break
            elif i.upper() == "Y":
                retain = False
                break

    if retain:
        print("Creating cache...")
        os.system("pip list > "+str(path))
        with open(path,"r",encoding = "utf-8") as file:
            req = file.readlines()[2:]
        write = []
        for i in req:
            write.append(i.split(" ")[0]+"\n")

        with open(path,"w",encoding = "utf-8") as file:
            file.writelines(write)

    create_end_cache = time()

    os.system("python -m pip install --upgrade -r "+str(path)+" -i https://pypi.tuna.tsinghua.edu.cn/simple")

    print("Delete cache...")
    delete_cache()

    end_time = time()

    print("All the package upgrade successful.")
    print(f"{'Times':-^30}")
    print("|"+"-"*30+"|")
    t1s = f"Use time : {round(end_time - create_cache, 2)}s"
    t2s = f"Create cache : {round(create_end_cache - create_cache, 2)}s"
    t3s = f"Update : {round(create_end_cache - end_time, 2)}s"
    print(f'|{t1s: <30}|\n|{30*"-"}|\n|{t2s: <30}|\n|{30*"-"}|\n|{t3s: <30}|\n|{"-"*30}|')

    os.system("pause")

def delete_cache():
    print("Delete cache...", end="")
    try:
        os.remove(path)
    except FileNotFoundError:
        print("error")
        print('Error: File not found.')
    else:
        print("done")
        print('Delete cache successful.')
 
def customize(options:list[str]):
    os.system(f"python -m pip install --upgrade {' '.join(options)}")