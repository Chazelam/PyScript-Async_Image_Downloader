import asyncio
import aiohttp

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'uk,en-US;q=0.9,en;q=0.8,ru;q=0.7',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}


def write_img(data, path, name):
    '''
    Function to save image data to a local file.
    Arguments:
      - data: The binary data of the image.
      - path: The name of the directory where the image will be saved.
      - name: The name of the file to save the image as.
    '''
    file_name = f"{path}/{name}"
    with open(file_name, 'wb') as file:
        file.write(data)


async def get_img(url, session, path, name):
    '''
    Asynchronous function to fetch an image from a given URL.
    Arguments:
      - url: The URL of the image to fetch.
      - session: An aiohttp session object to perform the request.
      - path: The name of the directory where the image will be saved.
      - name: The name of the file to save the image as.
    '''
    async with session.get(url, allow_redirects=True, headers=headers) as response:
        data = await response.read()
        write_img(data, path, name)



async def download_images(img_urls: list, path: str):
    '''
    Asynchronous function to download multiple images concurrently.
    Arguments:
    - img_urls: A list of image URLs to download.
    - path: The name of the directory where all images will be saved.
    '''
    tasks = []

    async with aiohttp.ClientSession() as session: 
        for url in img_urls:
            name = url.split('/')[-1]
            task = asyncio.create_task(get_img(url, session, path, name))
            tasks.append(task)
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    img_urls = ["", ""]
    path = "downloads/test"
    asyncio.run(download_images(img_urls, path))