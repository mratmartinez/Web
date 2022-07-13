from worker import Worker

def main():
    main_worker = Worker.get_worker_for_directory('./posts')
    posts = main_worker.get_posts()
    print(posts)

if __name__ == '__main__':
    main()
