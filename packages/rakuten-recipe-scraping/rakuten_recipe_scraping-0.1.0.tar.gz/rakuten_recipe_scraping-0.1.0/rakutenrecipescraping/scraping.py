import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional


class rakutenrecipescraping:

    def __init__(self, url: str):

        self.url = url
        self.soup = self._get_soup()
        self.recipe_id = self._extract_recipe_id()

    def _get_soup(self) -> BeautifulSoup:
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def _extract_recipe_id(self) -> str:

        return self.url.rstrip('/').split('/')[-1]

    def get_title(self) -> Optional[str]:
        title_tag = self.soup.find('h1', class_='page_title__text')
        return title_tag.get_text(strip=True) if title_tag else None

    def get_ingredients(self) -> List[Dict[str, str]]:

        results = []
        items = self.soup.find_all('li', class_='recipe_material__item')
        for item in items:
            name_tag = item.find('span', class_='recipe_material__item_name')
            amount_tag = item.find('span', class_='recipe_material__item_serving')
            name = name_tag.get_text(strip=True) if name_tag else ''
            amount = amount_tag.get_text(strip=True) if amount_tag else ''
            results.append({'Ingredient': name, 'Amount': amount})
        return results

    def get_material_amount(self) -> Optional[str]:

        section = self.soup.find('h2', class_='contents_title contents_title_mb')
        return section.get_text(strip=True) if section else None

    def get_steps(self) -> List[Dict[str, str]]:

        results = []
        steps = self.soup.find_all('li', class_='recipe_howto__item')
        for step in steps:
            order_tag = step.find('span', class_='ico_recipe_howto_order')
            text_tag = step.find('span', class_='recipe_howto__text')
            order = order_tag.get_text(strip=True) if order_tag else ''
            text = text_tag.get_text(strip=True) if text_tag else ''
            results.append({'Step Order': order, 'Step Text': text})
        return results

    def get_reason(self) -> Optional[str]:
        
        section = self.soup.find('div', class_='recipe_note__inner recipe_note__trigger pt21')
        if section:
            p_tag = section.find('p', class_='recipe_note__inner_text recipe_note__trigger_text')
            return p_tag.get_text(strip=True) if p_tag else None
        return None

    def get_tips(self) -> Optional[str]:

        section = self.soup.find('div', class_='recipe_note__inner recipe_note__tips')
        if section:
            p_tag = section.find('p', class_='recipe_note__inner_text recipe_note__tips_text')
            return p_tag.get_text(strip=True) if p_tag else None
        return None

    def get_published_date(self) -> Optional[str]:

        date_tag = self.soup.find('li', class_='recipe_note__date')
        if date_tag:
            text = date_tag.get_text(strip=True)
            if '：' in text:
                return text.split('：')[-1]
        return None

    def get_metadata(self) -> Dict[str, List[str]]:

        categories, keywords, recipe_names = [], [], []
        section = self.soup.find('section', class_='relation_info')

        if section:
            lists = section.find_all('dl', class_='relation_info__list')
            for relation in lists:
                dt = relation.find('dt', class_='relation_info__head')
                dd = relation.find('dd', class_='relation_info__item')
                if not dt or not dd:
                    continue
                label = dt.get_text(strip=True)
                links = [a.get_text(strip=True) for a in dd.find_all('a')]
                if label == 'カテゴリ':
                    categories = links
                elif label == '関連キーワード':
                    keywords = links
                elif label == '料理名':
                    recipe_names = links

        return {
            'Categories': categories,
            'Keywords': keywords,
            'Recipe Names': recipe_names
        }

    def get_all(self) -> Dict[str, Optional[str] or List]:
        
        metadata = self.get_metadata()

        return {
            'Recipe ID': self.recipe_id,
            'Title': self.get_title(),
            'Ingredients': self.get_ingredients(),
            'Material Amount': self.get_material_amount(),
            'Steps': self.get_steps(),
            'Reason': self.get_reason(),
            'Tips': self.get_tips(),
            'Published Date': self.get_published_date(),
            'Categories': metadata.get('Categories', []),
            'Keywords': metadata.get('Keywords', []),
            'Recipe Names': metadata.get('Recipe Names', [])
        }
