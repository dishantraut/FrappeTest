from dotenv import load_dotenv, find_dotenv, dotenv_values


class Config:
    """Configuration class responsible for loading and managing configuration values."""

    def get_config_json(self):
        """
        Loads configuration values from a `.env` file and returns them as a dictionary.

        Returns:
            dict: A dictionary containing configuration values, or an error message if the
                `.env` file is not found.
        """

        config = None
        if load_dotenv(dotenv_path=find_dotenv(".env")):
            # print(f"Loading DotEnv from: {find_dotenv('.env')}")
            config = {
                **dotenv_values(".env"),  # Load shared development variables
            }
            # print(f"Config: {config}")
        else:
            print("DotEnv File Not Found")
            config = {"message": "DotEnv File Not Found"}

        return config


if __name__ == "__main__":
    conf = Config()
    print(f"Raw Config:\n{conf.get_config_json()}\n\n")
    for key, value in conf.get_config_json().items():
        print(f"{key}: {value}")
