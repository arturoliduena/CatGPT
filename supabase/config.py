from configparser import ConfigParser


def get_config(config_file='./config.ini', section=None):
    parser = ConfigParser()
    parser.read(config_file)

    params = parser.items()
    if section is None:
        return {s: dict(parser.items(s)) for s in parser.sections()}

    out = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            out[param[0]] = param[1]

    return out


if __name__ == "__main__":
    print(get_config('./config.ini'))
    print(get_config('./config.ini', 'postgresql'))
