from worker import Worker

def main():
    main_worker = Worker.get_worker_for_directory('./posts')
    files = main_worker.filter_root_for_markdown()
    print(list(files))

if __name__ == '__main__':
    main()
