from worker.worker import Worker
import os

if __name__ == '__main__':
    try:
        # Change the current working Directory
        os.chdir("resources/")
        print("Directory changed")
    except OSError:
        print("Can't change the Current Working Directory")

    sc = Worker()