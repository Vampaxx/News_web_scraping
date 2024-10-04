import os
from dotenv import load_dotenv
from News_web_scraping import logger
from News_web_scraping.constants import *
from News_web_scraping.utils.common import *
from News_web_scraping.entity.config_entity import (ModelConfig,
                                                    WebScrapingConfig)
                                                      



class ConfigurationManager:
    def __init__(self,
                 config_filepath    = CONFIG_FILE_PATH,
                 params_filepath    = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])


    def get_model_config(self) -> ModelConfig:
        params  = self.params
        logger.info("Model config initialized")
        load_dotenv()
        model_config = ModelConfig(Model_name   = params.MODEL_NAME,
                                   temperature  = params.TEMPERATURE,
                                   max_token    = params.MAX_TOKEN,
                                   api_key      = os.getenv("GROQ_API_KEY"))

        return model_config


    def get_web_scraping_config(self) -> WebScrapingConfig:
        config              = self.config
        web_scraping_config = self.config.Web_scraping

        logger.info("web scraping initialized")
        web_scraping_config = WebScrapingConfig(headers         = config.headers,
                                                extracted_path  = web_scraping_config.extracted_path)
        return web_scraping_config
    

if __name__ == "__main__":
    manager = ConfigurationManager()


    

