from pprint import pprint

from scanner.scanner import Scanner

def main():
    main_scanner = Scanner.get_scanner_for_directory('../resources/posts')
    pprint(main_scanner._posts)

if __name__ == '__main__':
    main()
