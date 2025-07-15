# import playwright
from playwright.async_api import async_playwright
import asyncio
import json
# use playwright for web automation

# web url
category_url = {
    "electonics": "https://www.jumia.com.ng/electronics/all-products/?rating=3-5&seller_score=4-5#catalog-listing",
    "phones_tablets": "https://www.jumia.com.ng/phones-tablets/all-products/?rating=3-5&seller_score=4-5#catalog-listing",
    "computing": "https://www.jumia.com.ng/computing/all-products/?rating=3-5&seller_score=3-5#catalog-listing"
}


# jumia_scraper

async def jumia_scraper():
    try:
        async with async_playwright() as play:  # Instantiate with context manager
            # create brower instance
            browser = await play.chromium.launch(headless=True)

            # pass json to json file
            with open("jumia_data.json", "a+", encoding="utf-8") as f:
                # for variable, value in category_url.items():
                #    f.write(json.dumps(await jumia_category_data(browser, category_url=value), indent=4))
                f.write(json.dumps(await jumia_category_data(browser, category_url=category_url["electonics"]), indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await browser.close()


# jumia_category_data
async def jumia_category_data(browser, category_url):
    # create a new page
    page = await browser.new_page()

    category_data = []
    for _ in range(1, 4):
        # while True:
        # goto page
        await page.goto(category_url, wait_until="domcontentloaded")

        # Select all matching <article> elements
        articles = await page.query_selector_all("article.prd._fb.col.c-prd")

        # get all products
        for i, article in enumerate(articles, start=1):
            try:
                # Listing link
                core_link = await article.query_selector("a.core")
                href = await core_link.get_attribute("href") if core_link else None
                full_link = f"https://www.jumia.com.ng{href}" if href else None

                # Image URL
                img_tag = await article.query_selector("div.img-c img")
                image_url = (await img_tag.get_attribute("data-src") or await img_tag.get_attribute("src")) if img_tag else None

                # Title
                title_tag = await article.query_selector("div.info h3.name")
                title = await title_tag.inner_text() if title_tag else None

                # Price
                price_tag = await article.query_selector("div.info div.prc")
                price = await price_tag.inner_text() if price_tag else None

                json_data = {
                    "title": title,
                    "image": image_url,
                    "link": full_link,
                    "price_ng": price
                }
                category_data.append(json_data)
                print(f"\n--- Product {i} ---")
                print(json_data)
                print("--------------------------------")

            except Exception as e:
                print(f"Error processing article {i}: {e}")
                print("--------------------------------")
        # get next page url
        next_page_url = await get_next_page_url(page)
        if next_page_url:
            category_url = next_page_url
        else:
            break
    return category_data


async def get_next_page_url(page):
    try:
        # The "Next Page" link is the <a> tag with aria-label="Next Page"
        next_page_element = await page.query_selector('a[aria-label="Next Page"]')
        if next_page_element:
            href = await next_page_element.get_attribute("href")
            if href:
                return f"https://www.jumia.com.ng{href}"
        return None
    except Exception as e:
        print(f"Error getting next page URL: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(jumia_scraper())
