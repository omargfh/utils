import json 
import os
import sys
import time
import pandas as pd
import requests
from pyppeteer import launch
import asyncio

# Formats
(
    PDF,
    HTML
) = range(2)

(
    PROCESSING,
    COMPLETED,
    FAILED,
    THREAD_START,
) = range(4)

# colored
error = lambda msg: print(f"\033[91m Error:\t \033[0m{msg}")
info = lambda msg: print(f"\033[94m INFO:\t \033[0m{msg}")
success = lambda msg: print(f"\033[92m Success:\t \033[0m{msg}")
warning = lambda msg: print(f"\033[93m Warning:\t \033[0m{msg}")

class SitemapScraper():
    def __init__(
            self, url: str or None = None,
            path: str or None = None,
            filter_predicate: callable or None = lambda x: True,
            naming_function: callable or None = lambda x: x.replace("http://", "").replace("https://", "").replace('/', '_').replace('.', '_').replace('.html', ''),
            cores: int = 12,
            max_retires: int = 3,
            format: str = 'pdf',
            dest: str = './scraped/',
    ):
        if (url):
            response = requests.get(url)
            self.df = pd.read_xml(response.content)
        else:
            self.df = pd.read_xml(path)
        self.links = self.df['loc']
        self.links = self.links[self.links.apply(filter_predicate)]
        self.link_map = {link: naming_function(link) for link in self.links}
        self.failed = dict() # {link: retries}
        self.completed = dict() # {link: path}
        self.format = PDF if format == 'pdf' else HTML
        self.dest = f'{dest}/{int(time.time())}'
        self.cores = cores
        self.start = time.time()
        os.makedirs(self.dest, exist_ok=True)

    async def _thread(self, idx, links, report: callable):
        browser = await launch(
            options={
                'headless': True,
                'args': [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--single-process',
                    '--disable-gpu',
                ],
            },
        )

        for link in links:
            report(link, PROCESSING)
            try:
                page = await browser.newPage()
                await page.goto(link)
                await page.waitForSelector('main')
                if self.format == PDF:
                    await page.pdf({
                        'path': f'{self.dest}/{self.link_map[link]}.pdf',
                        'format': 'A4',
                        'printBackground': False
                    })
                else:
                    await page.content({
                        'path': f'{self.dest}/{self.link_map[link]}.html',
                    })
                await page.close()
                report(link, COMPLETED)
            except Exception as e:
                error(e)
                report(link, FAILED)

        await browser.close()

    def _progress(self):
        success(f"Completed link {len(self.completed)} of {len(self.links)} with percentage {round(len(self.completed)/len(self.links)*100, 2)}% | ETA: {round(self._eta()/60, 2)} minutes")

    def _report(self, link: str, status: int):
        if status == PROCESSING:
            self.failed[link] = self.failed.get(link, 0) + 1
        elif status == COMPLETED:
            self.completed[link] = self.link_map[link]
            self._progress()
            del self.failed[link]
        elif status == THREAD_START:
            print(f"INFO: \t Starting thread {threading.get_ident()}")
        else: # if status == FAILED
            self.failed[link] = self.failed.get(link, 0) + 1
            warning(f"Failed to process link {link} with {self.failed[link] - 1} retries")

    def _eta(self):
        return (time.time() - self.start) / len(self.completed) * (len(self.links) - len(self.completed))

    async def run(self):
        # Main routine
        links = lambda idx: self.links[idx*(len(self.links)//self.cores):(idx+1)*(len(self.links)//self.cores)]
        tasks = []
        for idx in range(self.cores):
            info(f"Starting thread {idx}")
            task = asyncio.create_task(self._thread(idx, links(idx), self._report))
            tasks.append(task)

        await asyncio.gather(*tasks)

        # Failures
        while True:
            error(f"Failed to process {len(self.failed)} links")
            info(f"Retrying {len(self.failed)} links")
            retry = [link for link, retries in self.failed.items() if retries < self.max_retires]
            if len(retry) == 0:
                break
            await self._thread(self.cores, self.failed.keys(), self._report)

        # Summary
        success(f"Completed {len(self.completed)} links")
        error(f"Failed to process {len(self.failed)} links")

        # Save logs
        info(f"Saving logs to {self.dest}")
        logs = [(link, "success", None) for link in self.completed.keys()] + [(link, "failed", self.failed[link]) for link in self.failed.keys()]
        pd.DataFrame(logs, columns=['link', 'status', 'retries']).set_index('link').to_csv(f'{self.dest}/logs.csv')
        json.dump(self.completed, open(f'{self.dest}/completed.json', 'w'))

        # Info
        info(f"Completed scraping sitemap to {self.dest}")

if __name__ == '__main__':
    sitemap = SitemapScraper(
        path='*.xml'
    )
    asyncio.get_event_loop().run_until_complete(sitemap.run())
