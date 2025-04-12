<h1 align="center">
Image Crawler Utils
</h1>
<h4 align="center">
A Customizable Multi-station Image Crawler Structure
</h4>
<p align="center">
English | <a href="https://github.com/AkihaTatsu/Image-Crawler-Utils/blob/main/docs/README_zh.md">简体中文</a>
</p>

---

## About

A **rather customizable** image crawler structure, designed to download images with their information using multi-threading method.

Besides, [several classes and functions](https://github.com/AkihaTatsu/Image-Crawler-Utils/blob/main/docs/classes_and_functions.md) have been implemented to help better build a custom image crawler for yourself.

**Please follow the rules of robots.txt, and set a low number of threads with high number of delay time when crawling images. Frequent requests and massive download traffic may result in IP addresses being banned or accounts being suspended.**

## Installing

It is recommended to install it by

```Default
pip install image-crawler-utils
```

+ Requires `Python >= 3.9`.

### Attentions!

+ **[nodriver](https://github.com/ultrafunkamsterdam/nodriver)** are used to parse information from certain websites. It is suggested to **install the latest version of [Google Chrome](https://www.google.com/chrome/)** first to ensure the crawler will be correctly running.

## Features (Partial)

+ Currently supported websites:
  + [Danbooru](https://danbooru.donmai.us/) - features supported:
    + Downloading images searched by tags
  + [yande.re](https://yande.re/) / [konachan.com](https://konachan.com/) / [konachan.net](https://konachan.net/) - features supported:
    + Downloading images searched by tags
  + [Gelbooru](https://gelbooru.com/) - features supported:
    + Downloading images searched by tags
  + [Safebooru](https://safebooru.org/) - features supported:
    + Downloading images searched by tags
  + [Pixiv](https://www.pixiv.net/) - features supported:
    + Downloading images searched by tags
    + Downloading images uploaded by a certain member
  + [Twitter / X](https://x.com/) - features supported:
    + Downloading images from searching result
    + Downloading images uploaded by a certain user
+ Logging of crawler operations onto the console and (optional) into a file.
+ Using `rich` bars and logging messages to denote the progress of crawler (Jupyter Notebook support is included).
+ Save or load the settings of a crawler.
+ Save or load the information of images for future downloading.
+ Several classes and functions for custom image crawler designing.

## How to Use

Please refer to [tutorials](https://github.com/AkihaTatsu/Image-Crawler-Utils/blob/main/docs/tutorials.md) and [notes for tasks](https://github.com/AkihaTatsu/Image-Crawler-Utils/blob/main/docs/notes_for_tasks.md) for detailed instructions.

### Quick Start

Image Crawler Utils provides three independent modules for an image crawler:

+ **CrawlerSettings:** Basic configuration to adjust the downloading and debugging settings of the crawler. Every argument except station_url is optional, and will use the default values (see [tutorials](https://github.com/AkihaTatsu/Image-Crawler-Utils/blob/main/docs/tutorials.md)) when omitted. A list of parameters in a CrawlerSettings is like:

```Python
from image_crawler_utils import CrawlerSettings
from image_crawler_utils.configs import DebugConfig

crawler_settings = CrawlerSettings(
    # Configs restrict downloading numbers and capacity
    image_num: int | None=None,
    capacity: float | None=None,
    page_num: int | None=None,
    # Configs about parameters in downloading
    headers: dict | Callable | None=None,
    proxies: dict | Callable | None=None,
    thread_delay: float=5,
    fail_delay: float=3,
    randomize_delay: bool=True,
    thread_num: int=5,
    timeout: float | None=10,
    max_download_time: float | None=None,
    retry_times: int=5,
    overwrite_images: bool=True,
    # Configs define which types of messages are shown on the console.
    debug_config=DebugConfig(
        show_debug: bool=False,
        show_info: bool=True,
        show_warning: bool=True,
        show_error: bool=True,
        show_critical: bool=True,
    ),
    # Logging settings
    detailed_console_log: bool=False,
    # Extra configs for custom use
    extra_configs={
        "arg_name": config, 
        "arg_name2": config2, 
        ...
    },
)
```

+ **Parser:** Parsing the arguments provided, visiting and crawling the sites, and finally return a list of image URLs with information. Different tasks may require different parsers. A functional parser should work like this:

```Python
# import SomeParser from image_crawler_utils.stations.some_station

parser = SomeParser(crawler_settings, parser_args)
image_info_list = parser.run()


# Example
from image_crawler_utils.stations.booru import DanbooruKeywordParser

parser = DanbooruKeywordParser(
    crawler_settings=crawler_settings,
    standard_keyword_string="kuon_(utawarerumono) AND rating:safe",
)
image_info_list = parser.run()
```

+ **Downloader:** Downloading images with the list generated by parser and filtered by the image_filter. A list of parameters in a Donwloader is like:

```Python
from image_crawler_utils import Downloader

downloader = Downloader(
    crawler_settings: CrawlerSettings=CrawlerSettings(),
    image_info_list: Iterable[ImageInfo],
    store_path: str | Iterable[str]='./',
    image_info_filter: Callable | bool=True,
    cookies: Cookies | list | dict | str | None=Cookies(),
)
total_size, succeeded_image_list, failed_image_list, skipped_image_list = downloader.run()
```

### Examples

Running this [example](https://github.com/AkihaTatsu/Image-Crawler-Utils/blob/main/examples/example.py) will download the first 20 images from [Danbooru](https://danbooru.donmai.us/) with keyword / tag `kuon_(utawarerumono)` and `rating:general` into the "Danbooru" folder. Information of images will be stored in `image_info_list.json` at same the path of your program. Pay attention that the proxies may need to be changed manually.

```Python
from image_crawler_utils import CrawlerSettings, Downloader, save_image_infos
from image_crawler_utils.stations.booru import DanbooruKeywordParser

crawler_settings = CrawlerSettings(
    image_num=20,
    # If you do not use system proxies, remove '#' and set this manually
    # proxies={"https": "socks5://127.0.0.1:7890"},
)

parser = DanbooruKeywordParser(
    crawler_settings=crawler_settings,
    standard_keyword_string="kuon_(utawarerumono) AND rating:general",
)
image_info_list = parser.run()
save_image_infos(image_info_list, "image_info_list")
downloader = Downloader(
    crawler_settings=crawler_settings,
    store_path='Danbooru',
    image_info_list=image_info_list,
)
downloader.run()
```

Information of an image in the saved `image_info_list.json` is like:

<details>
<summary><b>ImageInfo Structure in JSON</b></summary>

```json
{
    "url": "https://cdn.donmai.us/original/cd/91/cd91f0000b9574bf142d125a1e886e5c.png",
    "name": "Danbooru 4994142 cd91f0000b9574bf142d125a1e886e5c.png",
    "info": {
        "info": {
            "id": 4994142,
            "created_at": "2021-12-21T08:02:13.706-05:00",
            "uploader_id": 772564,
            "score": 10,
            "source": "https://i.pximg.net/img-original/img/2020/08/11/12/41/43/83599609_p0.png",
            "md5": "cd91f0000b9574bf142d125a1e886e5c",
            "last_comment_bumped_at": null,
            "rating": "s",
            "image_width": 2000,
            "image_height": 2828,
            "tag_string": "1girl absurdres animal_ears black_eyes black_hair coat grabbing_own_breast hair_ornament hairband highres holding holding_mask japanese_clothes kuon_(utawarerumono) long_hair looking_at_viewer mask ponytail shirokuro_neko_(ouma_haruka) smile solo utawarerumono utawarerumono:_itsuwari_no_kamen",
            "fav_count": 10,
            "file_ext": "png",
            "last_noted_at": null,
            "parent_id": null,
            "has_children": false,
            "approver_id": null,
            "tag_count_general": 17,
            "tag_count_artist": 1,
            "tag_count_character": 1,
            "tag_count_copyright": 2,
            "file_size": 4527472,
            "up_score": 10,
            "down_score": 0,
            "is_pending": false,
            "is_flagged": false,
            "is_deleted": false,
            "tag_count": 23,
            "updated_at": "2024-07-10T12:21:31.782-04:00",
            "is_banned": false,
            "pixiv_id": 83599609,
            "last_commented_at": null,
            "has_active_children": false,
            "bit_flags": 0,
            "tag_count_meta": 2,
            "has_large": true,
            "has_visible_children": false,
            "media_asset": {
                "id": 5056745,
                "created_at": "2021-12-21T08:02:04.132-05:00",
                "updated_at": "2023-03-02T04:43:15.608-05:00",
                "md5": "cd91f0000b9574bf142d125a1e886e5c",
                "file_ext": "png",
                "file_size": 4527472,
                "image_width": 2000,
                "image_height": 2828,
                "duration": null,
                "status": "active",
                "file_key": "nxj2jBet8",
                "is_public": true,
                "pixel_hash": "5d34bcf53ddde76fd723f29aae5ebc53",
                "variants": [
                    {
                        "type": "180x180",
                        "url": "https://cdn.donmai.us/180x180/cd/91/cd91f0000b9574bf142d125a1e886e5c.jpg",
                        "width": 127,
                        "height": 180,
                        "file_ext": "jpg"
                    },
                    {
                        "type": "360x360",
                        "url": "https://cdn.donmai.us/360x360/cd/91/cd91f0000b9574bf142d125a1e886e5c.jpg",
                        "width": 255,
                        "height": 360,
                        "file_ext": "jpg"
                    },
                    {
                        "type": "720x720",
                        "url": "https://cdn.donmai.us/720x720/cd/91/cd91f0000b9574bf142d125a1e886e5c.webp",
                        "width": 509,
                        "height": 720,
                        "file_ext": "webp"
                    },
                    {
                        "type": "sample",
                        "url": "https://cdn.donmai.us/sample/cd/91/sample-cd91f0000b9574bf142d125a1e886e5c.jpg",
                        "width": 850,
                        "height": 1202,
                        "file_ext": "jpg"
                    },
                    {
                        "type": "original",
                        "url": "https://cdn.donmai.us/original/cd/91/cd91f0000b9574bf142d125a1e886e5c.png",
                        "width": 2000,
                        "height": 2828,
                        "file_ext": "png"
                    }
                ]
            },
            "tag_string_general": "1girl animal_ears black_eyes black_hair coat grabbing_own_breast hair_ornament hairband holding holding_mask japanese_clothes long_hair looking_at_viewer mask ponytail smile solo",
            "tag_string_character": "kuon_(utawarerumono)",
            "tag_string_copyright": "utawarerumono utawarerumono:_itsuwari_no_kamen",
            "tag_string_artist": "shirokuro_neko_(ouma_haruka)",
            "tag_string_meta": "absurdres highres",
            "file_url": "https://cdn.donmai.us/original/cd/91/cd91f0000b9574bf142d125a1e886e5c.png",
            "large_file_url": "https://cdn.donmai.us/sample/cd/91/sample-cd91f0000b9574bf142d125a1e886e5c.jpg",
            "preview_file_url": "https://cdn.donmai.us/180x180/cd/91/cd91f0000b9574bf142d125a1e886e5c.jpg"
        },
        "family_group": null,
        "tags": [
            "1girl",
            "absurdres",
            "animal_ears",
            "black_eyes",
            "black_hair",
            "coat",
            "grabbing_own_breast",
            "hair_ornament",
            "hairband",
            "highres",
            "holding",
            "holding_mask",
            "japanese_clothes",
            "kuon_(utawarerumono)",
            "long_hair",
            "looking_at_viewer",
            "mask",
            "ponytail",
            "shirokuro_neko_(ouma_haruka)",
            "smile",
            "solo",
            "utawarerumono",
            "utawarerumono:_itsuwari_no_kamen"
        ],
        "tags_class": {
            "1girl": "general",
            "animal_ears": "general",
            "black_eyes": "general",
            "black_hair": "general",
            "coat": "general",
            "grabbing_own_breast": "general",
            "hair_ornament": "general",
            "hairband": "general",
            "holding": "general",
            "holding_mask": "general",
            "japanese_clothes": "general",
            "long_hair": "general",
            "looking_at_viewer": "general",
            "mask": "general",
            "ponytail": "general",
            "smile": "general",
            "solo": "general",
            "kuon_(utawarerumono)": "character",
            "utawarerumono": "copyright",
            "utawarerumono:_itsuwari_no_kamen": "copyright",
            "shirokuro_neko_(ouma_haruka)": "artist",
            "absurdres": "meta",
            "highres": "meta"
        }
    },
    "backup_urls": [
        "https://i.pximg.net/img-original/img/2020/08/11/12/41/43/83599609_p0.png"
    ]
}
```

</details>

## Documentation

+ [Tutorials](https://github.com/AkihaTatsu/Image-Crawler-Utils/blob/main/docs/tutorials.md): A detailed tutorial about how to set up configurations, construct a image crawler and downloading images by keywords / tags from Danbooru.
+ [Notes for tasks](https://github.com/AkihaTatsu/Image-Crawler-Utils/blob/main/docs/notes_for_tasks.md): Including notes and examples for every supported sites and crawling tasks.
+ [Classes and Functions](https://github.com/AkihaTatsu/Image-Crawler-Utils/blob/main/docs/classes_and_functions.md): Providing extra information about the structure of this project and information of usable classes and functions.
