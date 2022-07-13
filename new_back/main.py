from pprint import pprint

from worker import Worker

def main():
    main_worker = Worker.get_worker_for_directory('./posts')
    pprint(main_worker._posts)

if __name__ == '__main__':
    main()
