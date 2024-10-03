from News_web_scraping import logger
from News_web_scraping.config.configuration import ConfigurationManager
from News_web_scraping.components.Model import ModelSetup




STAGE_NAME = "Model setup stage"


class ModelPipeline:
    def __init__(self):
        pass 
    def main(self):
        try:
            manager         = ConfigurationManager()
            model_config    = manager.get_model_config()
            llm             = ModelSetup(config=model_config).model_setup()
            return llm
        except Exception as e:
            raise e
        

if __name__ == "__main__":
    try:
        logger.info(f"<<<    stage   {STAGE_NAME}    started >>>")
        obj     = ModelPipeline()
        llm     = obj.main()
        logger.info(f"<<<    stage   {STAGE_NAME}    completed \n\n===========================================>>>")

    except Exception as e:
        raise e
        

