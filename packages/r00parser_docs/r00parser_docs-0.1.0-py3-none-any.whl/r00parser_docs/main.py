import argparse
import asyncio
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup
import httpx
from markdownify import markdownify as md

# Логгер пока не импортируем, добавим позже или используем print для простоты первого шага
# from r00logger import log # Пример импорта

# ----- Временная заглушка парсера -----
# (Позже это будет в parsers.py)

class BaseParser:
    def __init__(self, base_url, output_file):
        self.base_url = base_url
        self.output_file = output_file
        self.visited_urls = set()
        # Используем асинхронный клиент httpx
        self.client = httpx.AsyncClient(follow_redirects=True, timeout=15.0)
        # Получаем "корень" сайта для корректного соединения относительных ссылок
        parsed_uri = urlparse(base_url)
        self.scheme = parsed_uri.scheme
        self.domain = parsed_uri.netloc
        self.root_url = f"{self.scheme}://{self.domain}"

    async def close_client(self):
        """Закрывает httpx клиент."""
        await self.client.aclose()

    async def fetch_page(self, url):
        """Получает HTML контент страницы."""
        if url in self.visited_urls:
            # print(f"Skipping already visited: {url}") # Для отладки
            return None, None
        self.visited_urls.add(url)
        try:
            # print(f"Fetching: {url}") # Для отладки
            response = await self.client.get(url)
            response.raise_for_status() # Проверка на ошибки HTTP (4xx, 5xx)
            # Указываем кодировку явно, если возможно, иначе BeautifulSoup попробует угадать
            response.encoding = response.apparent_encoding
            return response.text, response.url # Возвращаем текст и финальный URL (после редиректов)
        except httpx.HTTPStatusError as e:
            print(f"HTTP error fetching {url}: {e.response.status_code} {e.response.reason_phrase}")
        except httpx.RequestError as e:
            print(f"Request error fetching {url}: {e}")
        except Exception as e:
            print(f"Unexpected error fetching {url}: {e}")
        return None, None

    def extract_content(self, html_content, url):
        """Извлекает основной контент (зависит от движка)."""
        # Базовый метод, должен быть переопределен
        raise NotImplementedError

    def find_links(self, soup, current_url):
        """Находит ссылки на другие страницы документации."""
        # Базовый метод, должен быть переопределен
        raise NotImplementedError

    def convert_to_markdown(self, html_element, **options):
        """Конвертирует HTML фрагмент в Markdown."""
        if not html_element:
            return ""
        # Используем markdownify. Указываем базовый URL для корректного преобразования ссылок
        # Дополнительно можно настроить теги для заголовков, код и т.д.
        # heading_style="ATX" - использовать # для заголовков
        # code_language_callback - для определения языка в ``` ``` блоках (если возможно)
        return md(str(html_element), base_url=urljoin(self.root_url, "/"), heading_style="ATX", **options).strip()

    async def parse_page(self, url):
        """Основная логика парсинга одной страницы."""
        html_content, final_url = await self.fetch_page(url)
        if not html_content or not final_url:
            return None, []

        soup = BeautifulSoup(html_content, 'html.parser')
        content_element = self.extract_content(soup, str(final_url))
        if not content_element:
            # print(f"No main content found on {final_url}") # Для отладки
            return None, []

        markdown_content = self.convert_to_markdown(content_element)
        links = self.find_links(soup, str(final_url))

        # Преобразуем относительные ссылки в абсолютные и фильтруем
        valid_links = set()
        for link in links:
            abs_link = urljoin(str(final_url), link)
            # Оставляем только ссылки внутри того же домена и не на файлы/якоря
            if abs_link.startswith(self.root_url) and '#' not in abs_link.split('/')[-1] and '.' not in abs_link.split('/')[-1][-5:]:
                 # Простое условие для исключения файлов и якорей, можно улучшить
                 # Проверяем что ссылка ведет не туда же откуда пришли и еще не обработана
                 if abs_link != str(final_url) and abs_link not in self.visited_urls:
                     valid_links.add(abs_link)

        return markdown_content, list(valid_links)

    async def run(self):
        """Запускает процесс парсинга, начиная с базового URL."""
        urls_to_parse = [self.base_url]
        all_markdown_content = []

        processed_count = 0
        max_pages = 1000 # Ограничение на всякий случай

        while urls_to_parse and processed_count < max_pages:
            url = urls_to_parse.pop(0)
            # Пропускаем уже посещенные URL на всякий случай (хотя fetch_page тоже проверяет)
            if url in self.visited_urls:
                continue

            markdown_content, new_links = await self.parse_page(url)
            processed_count += 1

            if markdown_content:
                # Добавляем URL и разделитель перед контентом страницы
                header = f"# URL: {url}\n\n"
                all_markdown_content.append(header + markdown_content)
                # print(f"Processed: {url} ({len(markdown_content)} chars)") # Для отладки

            for link in new_links:
                if link not in self.visited_urls and link not in urls_to_parse:
                    urls_to_parse.append(link)

            # Небольшая пауза, чтобы не нагружать сервер
            await asyncio.sleep(0.1)

        # Записываем все в файл
        if all_markdown_content:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write("\n\n---\n\n".join(all_markdown_content))
            print(f"Successfully parsed {len(self.visited_urls)} pages and saved to {self.output_file}")
        else:
            print("No content was parsed.")

        await self.close_client()


class SphinxParser(BaseParser):
    """Парсер для сайтов, созданных с помощью Sphinx (часто на ReadTheDocs)."""

    def extract_content(self, soup, url):
        """Извлекает основной контент для тем Sphinx/ReadTheDocs."""
        # Ищем основной контентный блок. Селекторы могут отличаться в разных темах.
        # Theme "sphinx_rtd_theme" (как у python-arango) использует <div role="main">
        content = soup.find('div', role='main')
        if not content:
            # Попробуем другой распространенный селектор
            content = soup.find('section', id='main-content') # Пример другого возможного селектора
        # Можно добавить еще селекторы для других тем Sphinx

        # Удаляем ненужные элементы внутри контента, если нужно
        # Например, кнопки "Edit on GitHub", навигацию внутри страницы и т.д.
        if content:
            for element in content.find_all(['div', 'section'], class_=['rst-footer-buttons', 'admonition']):
                 # Пример удаления ненужных блоков (можно расширить список классов)
                 # Пока оставим все для полноты
                 pass
                 # element.decompose() # Раскомментировать для удаления

        return content # Возвращаем найденный тег BeautifulSoup

    def find_links(self, soup, current_url):
        """Находит ссылки в основной контентной области и боковой панели Sphinx."""
        links = set()
        # 1. Ссылки из боковой панели навигации (toctree)
        # У темы "sphinx_rtd_theme" это обычно <div class="wy-menu wy-menu-vertical">
        nav_menu = soup.find('div', class_='wy-menu-vertical')
        if nav_menu:
            for a in nav_menu.find_all('a', href=True):
                links.add(a['href'])

        # 2. Ссылки "Next" / "Previous"
        # Обычно это ссылки с rel="next" или rel="prev"
        for rel_type in ['next', 'prev']:
             link_tag = soup.find('a', rel=rel_type, href=True)
             if link_tag:
                 links.add(link_tag['href'])

        # 3. Можно добавить поиск ссылок внутри основного контента, если нужно глубокое сканирование
        # main_content = self.extract_content(soup, current_url)
        # if main_content:
        #     for a in main_content.find_all('a', href=True):
        #         links.add(a['href'])

        # Фильтруем ссылки, чтобы оставить только относительные или ведущие на тот же сайт
        valid_links = []
        parsed_current = urlparse(current_url)
        for link in links:
            parsed_link = urlparse(link)
            # Пропускаем пустые ссылки, якоря и внешние ссылки
            if not link or link.startswith('#') or (parsed_link.netloc and parsed_link.netloc != parsed_current.netloc):
                continue
            valid_links.append(link)

        return valid_links


async def run_parser(site_url, output_file):
    """Определяет тип парсера (пока только Sphinx) и запускает его."""
    # TODO: Добавить логику определения движка сайта
    # Пока что просто используем SphinxParser
    parser = SphinxParser(base_url=site_url, output_file=output_file)
    print(f"Using SphinxParser for {site_url}")
    await parser.run()


def main():
    parser = argparse.ArgumentParser(description="Parse documentation websites.")
    parser.add_argument("--site", required=True, help="URL of the documentation site to parse.")
    parser.add_argument("--output", required=True, help="Path to the output Markdown file.")
    args = parser.parse_args()

    print(f"Starting parser for site: {args.site}")
    print(f"Output will be saved to: {args.output}")

    # Используем asyncio для запуска асинхронных функций httpx
    asyncio.run(run_parser(args.site, args.output))

    print("Parsing finished.")


if __name__ == "__main__":
    exit()
    main()