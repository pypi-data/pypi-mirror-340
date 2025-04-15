from ten_utils.env_loader import EnvLoader


def main():
    env_loader = EnvLoader(".env")
    test = env_loader.load("TEST", bool)
    print(test, type(test))


if __name__ == "__main__":
    main()
