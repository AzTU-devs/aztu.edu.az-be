import sqlalchemy as sa
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys

# Configuration - UPDATE THESE CONNECTION STRINGS
OLD_DB_URL = "postgresql://user:pass@oldhost/olddb"
NEW_DB_URL = "postgresql://user:pass@newhost/newdb"

# Language mapping: assume common {1: 'en', 2: 'az', 3: 'ru'} - ADJUST BASED ON YOUR DATA
LANG_MAP = {1: 'en', 2: 'az', 3: 'ru'}  # Add more as needed

# Media type mapping if needed
MEDIA_TYPE_MAP = {1: 'image', 2: 'video'}  # Example, adjust

def main():
    old_engine = create_engine(OLD_DB_URL, echo=False)
    new_engine = create_engine(NEW_DB_URL, echo=False)
    
    old_meta = MetaData()
    old_meta.reflect(old_engine)
    
    new_meta = MetaData(bind=new_engine)
    
    # Step 1: Migrate Categories
    print("Migrating categories...")
    migrate_categories(old_engine, new_engine, old_meta, new_meta)
    
    # Step 2: Migrate News (after categories to get category_id mapping)
    print("Migrating news...")
    migrate_news(old_engine, new_engine, old_meta, new_meta)
    
    # Step 3: Migrate News Translations
    print("Migrating news translations...")
    migrate_news_translations(old_engine, new_engine, old_meta)
    
    # Step 4: Migrate Gallery (images/media)
    print("Migrating news gallery...")
    migrate_news_gallery(old_engine, new_engine, old_meta)
    
    print("Migration completed successfully!")

def migrate_categories(old_engine, new_engine, old_meta, new_meta):
    """Create news_category and news_category_translation if not exist, migrate data"""
    
    # Check/create news_category table
    news_category = Table('news_category', new_meta,
        Column('id', Integer, primary_key=True),
        Column('category_id', Integer, nullable=False, unique=True),
        Column('created_at', DateTime, nullable=False),
        Column('updated_at', DateTime),
        autoload_with=new_engine if new_engine.has_table('news_category') else None
    )
    
    # Check/create news_category_translation
    news_category_translation = Table('news_category_translation', new_meta,
        Column('id', Integer, primary_key=True),
        Column('category_id', Integer, nullable=False),
        Column('lang_code', String(2), nullable=False),
        Column('title', Text, nullable=False),
        autoload_with=new_engine if new_engine.has_table('news_category_translation') else None
    )
    
    if not new_engine.has_table('news_category'):
        news_category.create(new_engine)
        print("Created news_category table")
    
    if not new_engine.has_table('news_category_translation'):
        news_category_translation.create(new_engine)
        print("Created news_category_translation table")
    
    with old_engine.connect() as old_conn, new_engine.connect() as new_conn:
        new_conn.execute(text("TRUNCATE news_category, news_category_translation CASCADE"))
        new_conn.commit()
        
        # Migrate categories
        old_cat_table = old_meta.tables['ws_news_category']
        cats = old_conn.execute(old_cat_table.select()).fetchall()
        
        cat_id_map = {}  # old_category_id -> new_category_id
        new_cat_id = 1
        
        for cat in cats:
            old_cat_id = cat[old_cat_table.c.news_category_id]
            insert_data = {
                'id': new_cat_id,
                'category_id': new_cat_id,
                'created_at': datetime.now()
            }
            new_conn.execute(news_category.insert().values(insert_data))
            cat_id_map[old_cat_id] = new_cat_id
            new_cat_id += 1
        
        new_conn.commit()
        
        # Migrate category translations
        old_trans_table = old_meta.tables['ws_news_category_translate']
        trans = old_conn.execute(old_trans_table.select()).fetchall()
        
        for t in trans:
            old_cat_id = t[old_trans_table.c.news_category_id]
            lang_id = t[old_trans_table.c.language_id]
            title = t[old_trans_table.c.news_category_title]
            
            if old_cat_id in cat_id_map and lang_id in LANG_MAP:
                insert_data = {
                    'category_id': cat_id_map[old_cat_id],
                    'lang_code': LANG_MAP[lang_id],
                    'title': title
                }
                new_conn.execute(news_category_translation.insert().values(insert_data))
        
        new_conn.commit()
    
    print(f"Migrated {len(cats)} categories")

def migrate_news(old_engine, new_engine, old_meta, new_meta):
    """Migrate news table using category mapping"""
    
    news_table = Table('news', new_meta,
        Column('id', Integer, primary_key=True),
        Column('news_id', Integer, nullable=False, unique=True),
        Column('category_id', Integer, nullable=False),
        Column('display_order', Integer, nullable=False),
        Column('is_active', Boolean, nullable=False),
        Column('created_at', DateTime, nullable=False),
        Column('updated_at', DateTime),
        autoload_with=new_engine if new_engine.has_table('news') else None
    )
    
    if not new_engine.has_table('news'):
        news_table.create(new_engine)
        print("Created news table")
    
    old_meta.reflect(old_engine, only=['ws_news'])  # Ensure loaded
    
    with old_engine.connect() as old_conn, new_engine.connect() as new_conn:
        new_conn.execute(text("TRUNCATE news CASCADE"))
        new_conn.commit()
        
        old_news_table = old_meta.tables['ws_news']
        news_data = old_conn.execute(old_news_table.select()).fetchall()
        
        # Load category map
        cat_map_table = Table('news_category', MetaData(), autoload_with=new_engine)
        cat_map = {}
        for row in new_conn.execute(cat_map_table.select()):
            cat_map[row.category_id] = row.id
        
        new_news_id = 1
        for news in news_data:
            old_cat_id = news[old_news_table.c.news_category_id]
            new_cat_id = cat_map.get(old_cat_id, 1)  # default to 1 if missing
            
            insert_data = {
                'news_id': new_news_id,
                'category_id': new_cat_id,
                'display_order': news[old_news_table.c.news_weight] or 0,
                'is_active': bool(news[old_news_table.c.status]),
                'created_at': news[old_news_table.c.news_publish_date] or datetime.now()
            }
            new_conn.execute(news_table.insert().values(insert_data))
            new_news_id += 1
        
        new_conn.commit()
    
    print(f"Migrated {len(news_data)} news items")

def migrate_news_translations(old_engine, new_engine, old_meta):
    """Migrate news translations - assumes news.news_id sequential from 1"""
    
    with old_engine.connect() as old_conn, new_engine.connect() as new_conn:
        old_trans_table = old_meta.tables['ws_news_translate']
        trans_data = old_conn.execute(old_trans_table.select()).fetchall()
        
        new_conn.execute(text("TRUNCATE news_translation CASCADE"))
        new_conn.commit()
        
        news_translation = Table('news_translation', MetaData(bind=new_engine), autoload_with=new_engine)
        
        for trans in trans_data:
            news_id = trans[old_trans_table.c.news_id]  # Will map via sequential news_id
            lang_id = trans[old_trans_table.c.news_translate_language]
            title = trans[old_trans_table.c.news_translate_title]
            content = trans[old_trans_table.c.news_translate_content]
            
            if lang_id in LANG_MAP:
                insert_data = {
                    'news_id': news_id,
                    'lang_code': LANG_MAP[lang_id],
                    'title': title,
                    'html_content': content or ''
                }
                new_conn.execute(news_translation.insert().values(insert_data))
        
        new_conn.commit()
    
    print(f"Migrated {len(trans_data)} news translations")

def migrate_news_gallery(old_engine, new_engine, old_meta):
    """Migrate news_media to news_gallery, filter images, pick first as cover"""
    
    with old_engine.connect() as old_conn, new_engine.connect() as new_conn:
        old_media_table = old_meta.tables['ws_news_media']
        media_data = old_conn.execute(old_media_table.select()).fetchall()
        
        new_conn.execute(text("TRUNCATE news_gallery CASCADE"))
        new_conn.commit()
        
        news_gallery = Table('news_gallery', MetaData(bind=new_engine), autoload_with=new_engine)
        
        # Group by news_id
        media_by_news = {}
        for media in media_data:
            news_id = media[old_media_table.c.news_id]
            url = media[old_media_table.c.news_media_url]
            mtype = media[old_media_table.c.news_media_type]
            
            if mtype in MEDIA_TYPE_MAP and 'image' in MEDIA_TYPE_MAP[mtype]:  # Filter images
                if news_id not in media_by_news:
                    media_by_news[news_id] = []
                media_by_news[news_id].append(url)
        
        for news_id, images in media_by_news.items():
            # All images
            for i, img in enumerate(images):
                is_cover = (i == 0)
                insert_data = {
                    'news_id': news_id,
                    'image': img,
                    'is_cover': is_cover
                }
                new_conn.execute(news_gallery.insert().values(insert_data))
        
        new_conn.commit()
    
    print(f"Migrated {sum(len(imgs) for imgs in media_by_news.values())} gallery images")

if __name__ == "__main__":
    main()
