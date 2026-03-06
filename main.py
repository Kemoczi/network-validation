from clients.file_client import get_file_response

def main() -> None:
    try:
        print(get_file_response("show interfaces status gi1-10"))
        print(get_file_response("show interfaces status gi1-5"))
        print(get_file_response("Lodedede"))
    except ValueError as exc:
        print(exc)

if __name__ == "__main__":
    main()