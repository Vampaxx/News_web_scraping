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
    print(chain.invoke("""Login Max McDee , 02 October 2024  's hot streak continues as the company reported record-breaking sales for September 2024. The company sold a staggering 419,426 NEVs, marking its fourth consecutive month of record sales. This impressive figure represents a 45.91% increase compared to the same period last year and a 12.42% rise from . In September, BYD sold 252,647 PHEVs, achieving a seventh consecutive record high since March 2024. This signifies an 86.17% surge year-on-year and a 13.61% jump compared to August. While still impressive, sales of battery electric vehicles (BEVs) showed more modest growth. BYD sold 164,956 BEVs, a 9.1% increase year-on-year and an 11.1% rise from August. BYD's decision to cease production of internal combustion engine vehicles in March 2022 continues paying off handsomely. The company's strategic focus on NEVs has allowed it to capitalize on the growing global demand for electric and hybrid vehicles. Of the total NEV sales, passenger vehicles accounted for the lion's share, with 417,603 units sold in September. That's a 45.56% increase year-on-year and a 12.61% rise from August. Commercial NEV sales, while significantly lower in volume, also showed steady growth, reaching 1,823 units, a 230.85% increase year-on-year. BYD also has good news about its global expansion. The company sold 33,012 vehicles in overseas markets in September, a 17.74% increase year-on-year. The company is also a major player in the power battery market. In September, BYD's installed base of power and energy storage batteries reached approximately 19.8 GWh, demonstrating a 38% increase year-on-year. As expected, the strong September performance contributed to a record-breaking third quarter. The company sold an impressive 1,134,892 NEVs in total, exceeding the 1 million unit mark for the first time in a single quarter. This signifies a 37.73% increase year-on-year and a 15.02% rise from the second quarter of 2024. BYD's Song family continues to be a top performer, achieving record sales of 89,135 units in September. This popular lineup includes models like the Song L EV, Song L DM-i, Song Pro DM-i, Song Plus EV, and Song Plus DM-i. The Qin family followed closely behind, with 75,785 units sold, further solidifying BYD's strong position in the NEV market. |   © 2022-2024 From the team behind """))
