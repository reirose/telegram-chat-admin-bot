def parameters_parser(argv: list) -> dict:
    params: dict = {}

    try:
        if "--token" not in argv:
            raise RuntimeError("No Telegram bot token found. Please check README for more info")

        TOKEN_index = argv.index("--token") + 1
        params.update({"TOKEN": argv[TOKEN_index]})

    except (IndexError, AttributeError):
        raise RuntimeError("No Telegram bot token found. Please check README for more info")

    return params
