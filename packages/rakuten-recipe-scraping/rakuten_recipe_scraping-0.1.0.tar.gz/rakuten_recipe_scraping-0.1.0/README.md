# rakuten_recipe_scraping

楽天レシピからレシピ情報をスクレイピングするPythonライブラリ。

## 使い方

### インストール

```bash
pip install rakuten_recipe_scraping
```

### サンプルコード

```python
from rakutenrecipescraping import rakutenrecipescraping

rakuten = rakutenrecipescraping("https://recipe.rakuten.co.jp/recipe/1000000000/")
data = rakuten.get_all()
print(data)
```

## LICENSE

このプロジェクトは MITライセンス のもとで公開されています。

## 注意事項

本プロジェクトは教育目的で作成されたものです。スクレイピングを行う際はターゲットサイトの `robots.txt` や利用規約に従ってリクエストを過度に送信しないよう注意してください。