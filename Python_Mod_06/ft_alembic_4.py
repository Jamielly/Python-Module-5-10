import alchemy


def main() -> None:
    print(alchemy.create_air())
    alchemy.create_earth()  # type: ignore[attr-defined]


if __name__ == "__main__":
    main()
