import json
import requests
from pathlib import Path
from News_web_scraping import logger
from json.decoder import JSONDecodeError
from langchain_core.exceptions import OutputParserException
from requests.exceptions import RequestException, MissingSchema, ConnectionError, Timeout, HTTPError

from News_web_scraping.components.web_scraping import WebPageScraper
from News_web_scraping.pipeline.stage_02_prompt_and_chain import PromptAndChainPipeline




STAGE_NAME = "Combining stage"


class CombiningPipeline:
    def __init__(self, URL:Path):
        self.URL = URL
    
    def main(self):
        try:
            # Initialize the scraper and fetch the webpage content
            scraper = WebPageScraper(URL=self.URL)
            scraper.fetch_and_parse()
            page_text = scraper.clean_and_extract_text()

            # Handle the case where the content is 'No content found.'
            if page_text == "No content found.":
                logger.error("No content found on the webpage. Exiting process.")
                raise ValueError("The webpage did not contain any extractable content.")

            # Handle the case where extracted text is empty or only whitespace
            if not page_text or page_text.strip() == "":
                logger.error("The extracted content is empty or contains only whitespace.")
                raise OutputParserException("No data to extract from the provided webpage.")

            # Process the extracted text using the PromptAndChainPipeline
            prompt = PromptAndChainPipeline()
            chain = prompt.main()

            # Invoke the chain with the extracted page text
            return chain.invoke(page_text)
        
        # Handle output parsing errors if the output is invalid or empty
        except OutputParserException as e:
            logger.error(f"OutputParserException: {e}")
            return {
                "error": "Output parsing failed.",
                "message": str(e),
                "suggestion": "Ensure the webpage contains valid content for extraction."
            }

        # Handle invalid JSON outputs during the parsing phase
        except JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")
            return {
                "error": "Invalid JSON output.",
                "message": "The output from the model was not valid JSON.",
                "suggestion": "Check the model's output format and ensure it is correct."
            }

        # Handle requests-related issues such as timeouts, connection errors, etc.
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException while fetching the webpage: {e}")
            return {
                "error": "Failed to fetch the webpage.",
                "message": str(e),
                "suggestion": "Check the URL, internet connection, or server status."
            }

        # Handle cases where no content is found
        except ValueError as e:
            logger.error(f"ValueError: {e}")
            return {
                "error": "No content found.",
                "message": str(e),
                "suggestion": "Ensure the webpage has relevant content."
            }

        # General exception handling for any unexpected errors
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return {
                "error": "An unexpected error occurred.",
                "message": str(e),
                "suggestion": "Check the logs for more details or contact support."
            }


if __name__ == "__main__":
    try:
        URL     = "https://www.gsmarena.com/detailed_specs_for_samsungs_galaxy_a16_4g_and_5g_emerge-news-64767.php"
        #URL = "https://medium.com/@hamedkazemi/breaking-the-token-limits-a-journey-with-chatgpt-langchain-and-vectordb-embeddings-bonus-32352f97f5d4"
        #URL = "google.com"
        #URL = "https://techcrunch.com/2024/10/03/openai-launches-new-canvas-chatgpt-interface-tailored-to-writing-and-coding-projects/"
        logger.info(f"\n\n<<<===================== stage   {STAGE_NAME}    started =====================>>>")
        res         = CombiningPipeline(URL=URL)
        response    = res.main()
        print(response)
        logger.info(f"\n\n<<<===================== stage   {STAGE_NAME}    completed =====================>>>")

    except Exception as e:
        raise e
        

