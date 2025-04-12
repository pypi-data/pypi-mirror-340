import asyncio

from playwright.async_api import BrowserContext, Page

from .cache import Cache
from .constants import PLATZI_URL
from .models import Chapter, TypeUnit, Unit, Video
from .utils import get_m3u8_url, get_subtitles_url, slugify


@Cache.cache_async
async def get_course_title(page: Page) -> str:
    SELECTOR = ".CourseInfo_CourseInfo__Title__4Fwov"
    EXCEPTION = Exception("No course title found")
    try:
        title = await page.locator(SELECTOR).first.text_content()
        if not title:
            raise EXCEPTION
    except Exception:
        await page.close()
        raise EXCEPTION

    return title


@Cache.cache_async
async def get_draft_chapters(page: Page) -> list[Chapter]:
    SELECTOR = ".Syllabus_Syllabus__bVYL_ article"
    EXCEPTION = Exception("No sections found")
    try:
        locator = page.locator(SELECTOR)

        chapters: list[Chapter] = []
        for i in range(await locator.count()):
            chapter_name = await locator.nth(i).locator("h2").first.text_content()

            if not chapter_name:
                raise EXCEPTION

            block_list_locator = locator.nth(i).locator(
                ".SyllabusSection_SyllabusSection__Materials__C2hlu a"
            )

            units: list[Unit] = []
            for j in range(await block_list_locator.count()):
                ITEM_LOCATOR = block_list_locator.nth(j)

                unit_url = await ITEM_LOCATOR.get_attribute("href")
                unit_title = await ITEM_LOCATOR.locator("h3").first.text_content()

                if not unit_url or not unit_title:
                    raise EXCEPTION

                units.append(
                    Unit(
                        type=TypeUnit.VIDEO,
                        title=unit_title,
                        url=PLATZI_URL + unit_url,
                        slug=slugify(unit_title),
                    )
                )

            chapters.append(
                Chapter(
                    name=chapter_name,
                    slug=slugify(chapter_name),
                    units=units,
                )
            )

    except Exception as e:
        await page.close()
        raise EXCEPTION from e

    return chapters


@Cache.cache_async
async def get_unit(context: BrowserContext, url: str) -> Unit:
    TYPE_SELECTOR = ".VideoPlayer"
    TITLE_SELECTOR = ".MaterialDesktopHeading_MaterialDesktopHeading-info__title__luzx8"
    EXCEPTION = Exception("Could not collect unit data")

    if "/quiz/" in url:
        return Unit(
            url=url,
            title="Quiz",
            type=TypeUnit.QUIZ,
            slug=slugify("Quiz"),
        )

    try:
        page = await context.new_page()
        await page.goto(url)

        await asyncio.sleep(5)  # delay to avoid rate limiting

        title = await page.locator(TITLE_SELECTOR).first.text_content()

        if not title:
            raise EXCEPTION

        if await page.locator(TYPE_SELECTOR).count() == 0:
            type = TypeUnit.LECTURE
            video = None

        else:
            content = await page.content()
            type = TypeUnit.VIDEO
            video = Video(
                url=get_m3u8_url(content),
                subtitles_url=get_subtitles_url(content),
            )

        return Unit(
            url=url,
            title=title,
            type=type,
            video=video,
            slug=slugify(title),
        )

    except Exception:
        raise EXCEPTION

    finally:
        await page.close()
