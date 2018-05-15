# -*- coding: utf-8 -*-
from dotenv import load_dotenv
from os import environ

load_dotenv('.env')
DATABASE = {
    'drivername': 'mysql+pymysql',
    'host':     environ.get('db_host'),
    'port':     environ.get('db_port'),
    'username': environ.get('db_username'),
    'password': environ.get('db_password'),
    'database': environ.get('db_database'),
    'query': {'charset': 'utf8'}
}

kafka = {
    'host': environ.get('cafca_host'),
    'port': environ.get('cafca_port')
}

redis_config = {
    'host': environ.get('redis_host'),
    'port': environ.get('redis_port')
}

data_formatter = {
    'article': {
        'post_url_lists': [
            'http://ad.cn/api/test_article'
        ],
        'data_format': {
            'id': 'id',
            'title': 'title',
            'description': 'description',
            'image': 'image',
            'body': 'body',
            'type': 'type',
            'publish_time': 'publish_time',
            'author': 'author',
            'keywords': 'keywords',
            'source_url': 'source_url',
            'source_site': 'source_site',
            'dtype': 'data_type'
        }
    },
    'cftc': {
        'post_url_lists': [
            'http://ad.cn/api/test_cftc'
        ],
        'data_format': {
            'id': 'id',
            'cftc_name': 'cftc_name',
            'net_long': 'net_long',
            'net_short': 'net_short',
            'publish_time': 'publish_time',
            'source_site': 'source_site',
            'dtype': 'data_type'
        }
    },
    'calendar': {
        'post_url_lists': [
            "http://ad.cn/api/test_calendar"
        ],
        'data_format': {
            'id': 'id',
            'former_value': 'former_value',
            'predicted_value': 'predicted_value',
            'published_value': 'published_value',
            'country': 'country',
            'importance': 'importance',
            'quota_name': 'quota_name',
            'pub_time': 'pub_time',
            'source_id': 'source_id',
            'influence': 'influence',
            'source_site': 'source_site',
            'dtype': 'data_type'
        }
    },
    'event': {
        'post_url_lists': [
            "http://ad.cn/api/test_event"
        ],
        'data_format': {
            "id": "id",
            'importance': 'importance',
            'event': 'event',
            'city': 'city',
            'country': 'country',
            'time': 'time',
            'source_id': 'source_id',
            'source_site': 'source_site',
            'dtype': 'data_type'
        }
    },
    'holiday': {
        'post_url_lists': [
            "http://ad.cn/api/test_holiday"
        ],
        'data_format': {
            "id": "id",
            'country': 'country',
            'time': 'time',
            'market': 'market',
            'holiday_name': 'holiday_name',
            'detail': 'detail',
            'date': 'date',
            'source_id': 'source_id',
            'source_site': 'source_site',
            'dtype': 'data_type'
        }
    },
    'kuaixun': {
        'post_url_lists': [
            "http://ad.cn/api/test_kuaixun"
        ],
        'data_format': {
            "id": "id",
            'publish_time': 'publish_time',
            'body': 'body',
            'time_detail': 'time_detail',
            'importance': 'importance',
            'more_link': 'more_link',
            'image': 'image',
            'type': 'type',
            'real_time': 'real_time',
            'former_value': 'former_value',
            'predicted_value': 'predicted_value',
            'published_value': 'published_value',
            'country': 'country',
            'influnce': 'influnce',
            'star': 'star',
            'calendar_id': 'calendar_id',
            'source_site': 'source_site',
            'dtype': 'data_type',
            'typename': 'typename'
        }
    },
    'stock': {
        'post_url_lists': [
            "http://ad.cn/api/test_stock"
        ],
        "data_format": {
            'id': 'id',
            'publish_time': 'publish_time',
            'position': 'position',
            'iod': 'iod',
            'type': 'type'
        }
    },
    'fxssi': {
        'post_url_lists': [
            "http://ad.cn/api/test_fxssi"
        ],
        "data_format": {
            'day': 'day',
            'data': 'data'
        }
    },
    'jiedu': {
        'post_url_lists': [
            "http://ad.cn/api/test_jiedu"
        ],
        "data_format": {
            'id': 'id',
            'dataname_id': 'dataname_id',
            'next_pub_time': 'next_pub_time',
            'pub_agent': 'pub_agent',
            'pub_frequency': 'pub_frequency',
            'count_way': 'count_way',
            'data_influence': 'data_influence',
            'data_define': 'data_define',
            'funny_read': 'funny_read',
            'source_site': 'source_site',
            'dtype': 'data_type',
        }
    },
    'delete_calendar': {
        'post_url_lists': [
            "http://ad.cn/api/test_delete_calendar"
        ],
        "data_format": {
            'id': 'id',
            'dtype': 'data_type',
            'type': 'type',
            'source_site': 'source_site'
        }
    }
}
