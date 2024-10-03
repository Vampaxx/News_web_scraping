import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


__version__ = "0.0.0"

REPO_NAME           = "News_web_scraping"     # git
AUTHOR_USER_NAME    = "Vampaxx"
SRC_REPO            = "News_web_scraping"     # src 
AUTHOR_EMAIL        = "arjunappu1001@gmail.com"


setuptools.setup(
    name            = SRC_REPO,
    version         = __version__,
    author          = AUTHOR_USER_NAME,
    author_email    = AUTHOR_EMAIL,
    description     = "News web scraping with BeautifulSoup ",
    long_description            = long_description,
    long_description_content    = "text/markdown",
    url                         = f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls                = {"text to SQL": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",},
    package_dir                 = {"": "src"},
    packages                    = setuptools.find_packages(where="src")
)