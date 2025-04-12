from fetchfox_sdk import FetchFox

def main():
    fox = FetchFox(
        api_key='ff_5i423nh5fl0v0at99uf2hlpgjj1b7of2sgnw4cjx',
        host='https://staging.fetchfox.ai')

    # items = fox.crawl([
    #     "https://pokemondb.net/move/*",
    #     "https://pokemondb.net/type/*",
    # ])

    items = fox.crawl([
        "https://www.facebook.com/legal/*",
        "https://www.facebook.com/privacy/*"
    ], pull=True)

    for item in items.limit(500):
        print(item.url)

main()
