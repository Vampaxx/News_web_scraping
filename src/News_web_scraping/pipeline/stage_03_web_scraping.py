from News_web_scraping import logger
from News_web_scraping.components.web_scraping import WebPageScraper
from News_web_scraping.pipeline.stage_02_prompt_and_chain import PromptAndChainPipeline




STAGE_NAME = "Web scraping stage"


class WebScrapingPipeline:
    def __init__(self,URL):
        self.URL = URL 
    def main(self):
        try:
            scraper     = WebPageScraper(URL=self.URL)
            scraper.fetch_and_parse()
            page_text   = scraper.clean_and_extract_text()
            return page_text
        except Exception as e:
            raise e
        

if __name__ == "__main__":
    try:
        URL     = "https://www.gsmarena.com/detailed_specs_for_samsungs_galaxy_a16_4g_and_5g_emerge-news-64767.php"
        #URL = "google.com"
        logger.info(f"\n\n<<<===================== stage   {STAGE_NAME}    started =====================>>>")
        obj     = WebScrapingPipeline(URL)
        scraper = obj.main()

        obj     = PromptAndChainPipeline()
        llm     = obj.main()

        print(llm.invoke(scraper))
        logger.info(f"\n\n<<<===================== stage   {STAGE_NAME}    completed =====================>>>")

    except Exception as e:
        raise e
        

