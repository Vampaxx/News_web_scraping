from News_web_scraping import logger 
from News_web_scraping.components.Model import ModelSetup
from News_web_scraping.config.configuration import ConfigurationManager
from News_web_scraping.entity.config_entity import ModelConfig

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser




class PromptAndChain(ModelSetup):

    def __init__(self,model_config: ModelConfig,):
        
        super().__init__(model_config)
        self.llm                        = self.model_setup()
        self.parser                     = JsonOutputParser()

    def prompt_and_chain(self): 

        logger.info(f"Prompting and chain has started")

        json_prompt = """
You are an expert information extractor. Your task is to extract relevant data from the following text and organize it into a structured JSON format.

Instructions:
    1. Carefully read the following text.
    2. Extract key information and format it into a JSON object.
    3. Ensure that the keys in the JSON are relevant to the content. Use meaningful key names based on the context of the text.

Text:
{document_text}

Output:
Provide a JSON object containing the extracted relevant information.
"""

        example_prompt  = PromptTemplate(
            input_variables = ["document_text"],
            template        = json_prompt)

        chain = (
            {
                "document_text" : RunnablePassthrough() 
            }
            | example_prompt 
            | self.llm
            | self.parser
        )
        return chain 





if __name__ == "__main__":
    manager             = ConfigurationManager()
    model_config        = manager.get_model_config()
    prompt_and_chain    = PromptAndChain(model_config=model_config)
    chain               = prompt_and_chain.prompt_and_chain()
    print(chain.invoke("British Foreign Minister David Lammy said the deal settled the contested sovereignty of Britain’s last overseas territory in Africa, while securing the long-term future of the Diego Garcia military base, jointly operated by the UK and the US."))
