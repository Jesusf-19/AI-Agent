from functions.get_files_info import get_files_info

def main():
    print("Result for current directory:")
    print(get_files_info("calculator", "."))

    print("\nResult for 'pkg' directory:")
    print(get_files_info("calculator", "pkg"))

    print("\nResult for the '/bin' directory:")
    print(get_files_info("calculator", "/bin"))

    print("\nResult for the '../' directory:")
    print(get_files_info("calculator", "../"))

if __name__ == "__main__":
    main()