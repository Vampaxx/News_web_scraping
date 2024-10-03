from News_web_scraping import logger
from News_web_scraping.config.configuration import ConfigurationManager
from News_web_scraping.components.Model import ModelSetup
from News_web_scraping.components.prompt_and_chain import PromptAndChain




STAGE_NAME = "Prompt and chaining stage"


class PromptAndChainPipeline:
    def __init__(self):
        pass 
    def main(self):
        try:
            manager             = ConfigurationManager()
            model_config        = manager.get_model_config()
            prompt_and_chain    = PromptAndChain(model_config=model_config)
            chain               = prompt_and_chain.prompt_and_chain()
            return chain 
        except Exception as e:
            raise e
        

if __name__ == "__main__":
    try:
        logger.info(f"\n\n<<<===================== stage   {STAGE_NAME}    started =====================>>>")
        obj     = PromptAndChainPipeline()
        llm     = obj.main()
        logger.info(f"\n\n<<<===================== stage   {STAGE_NAME}    completed =====================>>>")

    except Exception as e:
        raise e
        

