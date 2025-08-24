import aiohttp
import asyncio
import json
import math
from tqdm.asyncio import tqdm_asyncio

BASE_URL = "https://osintapi.store/cutieee/api.php?key=jerry&type=mobile&term="

# Only numbers starting with 6 or 7
RANGES = [
    (6000000000, 6000000100),  # demo small range
    (7000000000, 7000000100),
]

BATCH_SIZE = 100  # 100 requests per burst
PAUSE = 0.01      # seconds pause after each batch

async def fetch_number(session, number):
    full_number = "+91" + str(number)
    url = BASE_URL + full_number
    while True:  # retry until success
        try:
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    if text.strip():
                        return {full_number: await resp.json()}
                    else:
                        return {full_number: None}
        except:
            await asyncio.sleep(0.01)  # retry small delay

async def run_scraper():
    async with aiohttp.ClientSession() as session:
        # Flatten all ranges into one list
        numbers = []
        for start, end in RANGES:
            numbers.extend(range(start, end + 1))
        total = len(numbers)
        batches = math.ceil(total / BATCH_SIZE)
        
        all_results = []  # store all results in one JSON

        for i in range(batches):
            batch_numbers = numbers[i*BATCH_SIZE:(i+1)*BATCH_SIZE]
            tasks = [fetch_number(session, n) for n in batch_numbers]
            
            # Run all 100 requests in parallel
            results = await tqdm_asyncio.gather(*tasks, desc=f"Batch {i+1}/{batches}")
            
            all_results.extend(results)
            
            # tiny pause before next batch
            await asyncio.sleep(PAUSE)

        # Save all results in a single JSON file
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    asyncio.run(run_scraper())
