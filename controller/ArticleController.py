# -*- coding: utf-8 -*-
from model.crawl_article import CrawlArticle
from Controller import Controller
import json, logging, time

class ArticleController(Controller):
    def __init__(self, topic="crawl_article"):
        super(ArticleController, self).__init__(topic, 'article')

    def run(self):
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                dtype= data['dtype'] if "dtype" in data else "insert"
                key = data['key'] if "key" in data else "source_id"

                del data['dtype']
                if "key" in data:
                    del data['key']

                article = CrawlArticle(**data)

                with self.session_scope(self.sess) as session:
                    if dtype == 'insert':
                        query = session.query(CrawlArticle.id).filter(
                            CrawlArticle.source_id == article.source_id
                        ).one_or_none()

                        if query is None:
                            session.add(article)
                            session.flush()
                            data['id'] = article.id
                            data['dtype'] = 'insert'
                            if "body" in data:
                                self.hook_data(data)
                        else:
                            query = session.query(CrawlArticle.id).filter(
                                getattr(CrawlArticle, key) == getattr(article, key)
                            ).one_or_none()

                            if query:
                                session.query(CrawlArticle).filter(
                                    CrawlArticle.id == query[0]
                                ).update(data)
                    else:
                        if hasattr(CrawlArticle, key):
                            query = session.query(CrawlArticle).filter(
                                getattr(CrawlArticle, key) == getattr(article, key)
                            ).one_or_none()

                            if query:
                                session.query(CrawlArticle).filter(
                                    CrawlArticle.id == query.id
                                ).update(data)

                                if "body" in data:
                                    data['id'] = query.id
                                    data['dtype'] = 'insert' if not query.body else "update"
                                    data['title'] = query.title
                                    data['description'] = query.description
                                    data['image'] = query.image
                                    data['body'] = query.body
                                    data['type'] = query.type
                                    data['publish_time'] = query.publish_time.strftime("%Y-%m-%d %H:%M:%S")
                                    data['author'] = query.author
                                    data['keywords'] = query.keywords
                                    data['source_url'] = query.source_url
                                    data['source_site'] = query.source_site

                                    self.hook_data(data)
            except Exception as e:
                self.logger.error('Catch an exception.', exc_info=True)