from worker import Worker

def main():
    main_worker = Worker.get_worker_for_directory('./posts')
    posts = main_worker.get_posts()
    first_post_header = posts[0]['header']
    print(main_worker.read_header(first_post_header))

if __name__ == '__main__':
    main()
