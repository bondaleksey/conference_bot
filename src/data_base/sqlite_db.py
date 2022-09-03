from os import curdir
import sqlite3 as sq


def sql_start():
    global base, cur
    # base = sq.connect('conference.db')
    base = sq.connect('data/example.db')    
    base.row_factory = sq.Row
    cur = base.cursor()
    if base:
        print('Data base connection OK!')
    # base.execute('CREATE TABLE IF NOT EXISTS menu(date TEXT, title TEXT PRIMARY KEY, description TEXT, duration TEXT)')
    # base.commit()
    
# async def sql_add_command(state):
#     async with state.proxy() as data:
#         print(tuple(data.values()))
#         cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)',tuple(data.values()))
#         base.commit()

async def sql_count_votes():
    cur.execute(
        """        
        SELECT report_id ,
               title,
               SUM(vote) as 'number of votes'
        FROM voting 
            INNER JOIN report USING(report_id)
        GROUP BY report_id
        ORDER BY "Number of votes" DESC        
        """
    )
    return cur.fetchall()


async def sql_search_by_author(author_name: tuple):
    
    request =  """        
        SELECT report_id ,
            group_concat(name_author) as 'authors',
            title,
            link
        FROM author
            INNER JOIN report_author USING(author_id)
            INNER JOIN report USING(report_id)
        GROUP BY report_id
        HAVING group_concat(name_author) LIKE ?               
        """
        
    if len(author_name)>1:
        request += (len(author_name)-1)*" AND group_concat(name_author) LIKE ? "        
    request +="\nORDER BY report_id"
    # print(f"author_name = {author_name}")
    # print(f'request = {request}')
    cur.execute(request,author_name)
    return cur.fetchall()

async def sql_search_by_title(report_title: tuple):
    request = """        
        SELECT report_id as 'Индекс report_index',
            group_concat(name_author) as 'authors',
            title,
            link
        FROM author
            INNER JOIN report_author USING(author_id)
            INNER JOIN report USING(report_id)
        GROUP BY report_id
        HAVING title LIKE ?
        """         
    if len(report_title)>1:
        request += (len(report_title)-1)*" AND title LIKE ?"
        
    request +="\nORDER BY report_id"
    # print(f"report_title = {report_title}")
    # print(f'request = {request}')
    cur.execute(request, report_title)
    return cur.fetchall()

async def sql_get_all_reports():
    # выдать все статьи
    request = """
    SELECT report_id ,
        group_concat(name_author) as 'authors',
        title,
        link
    FROM author
        INNER JOIN report_author USING(author_id)
        INNER JOIN report USING(report_id)
    GROUP BY report_id
    ORDER BY report_index
    """ 
    cur.execute(request)
    return cur.fetchall()


async def sql_voting_insert_one_vote(t3vote:tuple):
    request = """
              INSERT INTO voting (report_id,telegram_id, vote)
              VALUES (?, ?, ?);
              """
    print(f"request = {request}, t3vote = {t3vote}")
    cur.execute(request,t3vote)
    base.commit()



async def sql_voting_update_one_vote(t3vote:tuple):
    request = """
              UPDATE voting 
              SET vote = ?
              WHERE report_id = ? 
                    AND telegram_id = ?;
              """
    print(f"request = {request}, t2vote = {t3vote}")    
    cur.execute(request,t3vote)
    base.commit()



async def sql_voting_request_votes_by_report_telegram(t2vote:tuple):
    
    request = """
              select *
              FROM voting
              WHERE report_id = ? 
                    AND telegram_id = ? ;
              """
    print(f"request = {request}, t2vote = {t2vote}")       
    return cur.execute(request,t2vote).fetchall()


async def sql_voting_request_votes_by_telegram(t1vote:tuple):
    request = """
                select report_id ,
                    group_concat(name_author) as 'authors',
                    title,
                    link
                FROM voting
                    INNER JOIN report USING(report_id)
                    INNER JOIN report_author USING(report_id)
                    INNER JOIN author USING(author_id)
                WHERE telegram_id = ?
                GROUP BY report_id
                HAVING MIN(vote)=1                
              """
    print(f"request = {request}, t1vote = {t1vote}")   
    return cur.execute(request,t1vote).fetchall()

async def sql_timetable_select(t2vote:tuple):
    request = """
                SELECT timetable_description,
                        event_beg,
                        event_end,
                        name_location,
                        name_author,
                        title,
                        link
                FROM timetable
                    INNER JOIN location USING(location_id)
                    INNER JOIN report USING(report_id)
                    INNER JOIN report_author USING(report_id)
                    INNER JOIN author USING(author_id)
                WHERE event_beg > ?
                    AND event_beg < ?
                GROUP BY timetable_description;
              """
    print(f"request = {request}, t2vote = {t2vote}")   
    return cur.execute(request, t2vote).fetchall()


async def sql_location_all():
    request = """
                SELECT *
                FROM location;
              """
    print(f"request = {request}")   
    return cur.execute(request).fetchall()
# UPDATE voting 
# SET vote = 0
# WHERE report_id = 4 
# 	  AND telegram_id = 76655524231213;

# select *
# FROM voting
# WHERE report_id = 4 
# 	  AND telegram_id = 6655524231213;




# выдать со словами после слова Like
# SELECT report_id as 'Индекс',
# 	   group_concat(name_author) as 'Авторы',
# 	   title as 'Название',
# 	   link as 'Сслыка на статью'
# FROM author
# 	INNER JOIN report_author USING(author_id)
# 	INNER JOIN report USING(report_id)
# GROUP BY report_id
# HAVING title LIKE '%номер%'
#  AND title LIKE '%3%'
# ORDER BY report_id

# c автором среди авторов
# SELECT report_id as 'Индекс',
# 	   group_concat(name_author) as 'Авторы',
# 	   title as 'Название',
# 	   link as 'Сслыка на статью'
# FROM author
# 	INNER JOIN report_author USING(author_id)
# 	INNER JOIN report USING(report_id)
# GROUP BY report_id
# HAVING group_concat(name_author) LIKE '%Глумова%'
# ORDER BY report_id

# SELECT report_id as 'Индекс',
# 	   group_concat(name_author) as 'Авторы',
# 	   title as 'Название',
# 	   link as 'Сслыка на статью'
# FROM author
# 	INNER JOIN report_author USING(author_id)
# 	INNER JOIN report USING(report_id)
# GROUP BY report_id
# ORDER BY report_id



# SELECT report_id as 'Индекс',
# 	   group_concat(name_author) as 'Авторы',
# 	   title as 'Название',
# 	   link as 'Сслыка на статью'
# FROM author
# 	INNER JOIN report_author USING(author_id)
# 	INNER JOIN report USING(report_id)
# WHERE report_id IN (SELECT DISTINCT report_id
# 					FROM author
# 						INNER JOIN report_author USING(author_id)
# 					WHERE name_author LIKE '%Глумов%')
# GROUP BY report_id
# ORDER BY report_id


# SELECT *
# FROM timetable
#     INNER JOIN location USING(location_id)
#     INNER JOIN report USING(report_id)
#     INNER JOIN report_author USING(report_id)
#     INNER JOIN author USING(author_id)
# WHERE event_beg > '2022-08-18T10:10:00'
#     AND event_beg < '2022-08-18T10:50:00'
# GROUP BY timetable_description;

# SELECT timetable_description,
#     event_beg,
#     event_end,
#     name_location,
#     name_author,
#     title,
#     link
# FROM timetable
#     INNER JOIN location USING(location_id)
#     INNER JOIN report USING(report_id)
#     INNER JOIN report_author USING(report_id)
#     INNER JOIN author USING(author_id)
# WHERE event_beg > '2022-08-18T10:10:00'
#     AND event_beg < '2022-08-18T10:50:00'
# GROUP BY timetable_description;