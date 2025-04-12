# `mom_scrape`

example usage:

```
from mom_scrape.scrapers import ReportScraper, StatsScraper

# this retrieves the MOM reports
# take as input the selinium webdriver
reportscraper=ReportScraper(driver=driver, 
filter_by='Reports',
save_dir='stats/reports')

results=reportscraper.get_info()

# for the StatsScraper (this retrieves the stats)
statsscraper=StatsScraper(driver=driver, 
                        dataset_of_interest=INTEREST[url], 
                        website_link=url, 
                        save_as_zip=True, 
                        save_dir='stats')
# use save_as_zip if you want to save as zip, then send out the email later

results=statsscraper.get_info()

```
## ReportScraper
This first creates a `dates` folder then dump the dates of the various repoerts in the `mom_reports.json` file. Then, the new PDFs (these are PDFs that are not already recorded in `mom_reports.json` file) are downloaded under save_dir

## StatsScraper
Likewise, this also creates dumps the seens dates in the `dates` folder. Then, for new stats, we will download and save it under `self.save_dir` folder