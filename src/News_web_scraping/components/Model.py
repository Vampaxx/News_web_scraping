from News_web_scraping import logger
from langchain_groq import ChatGroq
from News_web_scraping.config.configuration import ConfigurationManager
from News_web_scraping.entity.config_entity import ModelConfig


class ModelSetup:

    def __init__(self,config = ModelConfig):
        self.config = config

    def model_setup(self):
        logger.info("Model setup initialized")
        llm     = ChatGroq(model        = self.config.Model_name,
                           temperature  = self.config.temperature,
                           max_tokens   = self.config.max_token,
                           api_key      = self.config.api_key,)
        
        logger.info(f"model----{(self.config.Model_name).split('/')[-1]}----created")
        return llm 
    



if __name__ == "__main__":
    manager         = ConfigurationManager()
    model_config    = manager.get_model_config()
    llm             = ModelSetup(config=model_config).model_setup()
    print(llm.invoke("hey"))