from module.handle_exception import HandleException
from module.reptile import RequestAnalysisData
from crawler.config import Initialization as Init
from module.log_generate import Loggings
import re
from module.call_api import APIRequest


logger = Loggings()

class PttInfoObtain:
    def __init__(self, ** crawler):
        """
            base url: obtain info ptt board url
            board_name: obtain ptt article board name
            task_id: celery create task id
            auth_user: current request username
        """
        self.__base_url = crawler['base_url']
        self.__article_title_filter = Init.article_title_filter
        self.__board_name = crawler['board_name']
        self.__task_id = crawler['task_id']
        self.__auth_user = crawler['auth_user']
        self.__info_columns = ['task', 'username', 'name', 'title', 'url', 'push_count', 'author', 'date', 'page']
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }

    def __check_include_match_items(self, check_string=None, pattern=None):
        return re.search(pattern, check_string)

    def ptt_scrape_by_page_count(self, search_page_count=1):
        info = []
        result = {
            'json_rows': ''
        }
        try:
            if self.__base_url is None:
                raise Exception('The base url is required.')
            full_url = self.__base_url
            is_last_page = False
            for current_page_count in range(0, search_page_count):
                current_page_article_image_related = []
                logger.info(f'Obtain article from the url: {full_url}')
                with RequestAnalysisData(
                    url=full_url, mode=False, cookies={'over18': '1'}, headers=self.__headers
                ) as soup:
                    main_container_div_tag = soup.find('div', {'id': 'main-container'})
                    # topbar_container_div_tag = soup.find('div', {'id': 'topbar-container'})

                    if main_container_div_tag is None:
                        raise Exception("Load main container div tag failed.")

                    # article_topbar_div_tag = topbar_container_div_tag.find('div', {'id': 'topbar', 'class': 'bbs-content'})
                    # article_topbar_a_tag = article_topbar_div_tag.find_all('a')[1] if article_topbar_div_tag is not None else None
                    # board_name = article_topbar_a_tag.getText().strip().replace('看板 ', '') if article_topbar_a_tag is not None else 'Unknown'

                    # if not result['task_mark']:
                    #     result['task_mark'] = board_name

                    # logger.info(f"Task mark the article type is: {result['task_mark']}")

                    article_div_tag = main_container_div_tag.find('div', {'class': 'r-list-container action-bar-margin bbs-screen'})
                    all_article_div_tag = article_div_tag.find_all('div', {'class': 'r-ent'}) if article_div_tag is not None else None
                    
                    if all_article_div_tag is None:
                        raise Exception("Load all article page div tag failed.")
                    
                    action_bar_div_tag = main_container_div_tag.find('div', {'id': 'action-bar-container'})
                    go_back_div_tag = action_bar_div_tag.find('div', {'class': 'btn-group btn-group-paging'})
                    go_back_a_tag = go_back_div_tag.find_all('a', {'class': 'btn wide'}, string="‹ 上頁")
                    
                    if go_back_a_tag is None or not go_back_a_tag:
                        is_last_page = True
                    else:
                        full_url = "https://www.ptt.cc/" + go_back_a_tag[0]['href']

                    for index, one_of_article in enumerate(all_article_div_tag, 1):
                        # logger.info(f'Staring get the {index} article')
                        title_div_tag = one_of_article.find('div', {'class': 'title'})
                        title_and_link_a_tag = title_div_tag.find('a') if title_div_tag is not None else None
                        title = title_and_link_a_tag.getText().strip() if title_and_link_a_tag is not None else ''
            
                        if title and self.__check_include_match_items(check_string=title, pattern=self.__article_title_filter) is None:
                            # logger.info(f'Obtain article title is: {title}')
                            link = "https://www.ptt.cc" + title_and_link_a_tag['href'] if title_and_link_a_tag is not None else ''
                            push_count_div_tag = one_of_article.find('div', {'nrec'})
                            
                            if push_count_div_tag is not None:
                                push_count = str(push_count_div_tag.get_text().strip())
                                if push_count and push_count.isdigit() is True:
                                    push_count = int(push_count)
                                elif push_count and push_count.isdigit() is False and push_count.find('爆') != -1:
                                    push_count = 100
                                elif push_count and push_count.isdigit() is False and push_count.find('X') != -1:
                                    push_count = -1
                                else:
                                    push_count = 0
                            
                            author_date_div_tag = one_of_article.find('div', {'class': 'meta'})
                            if author_date_div_tag is not None:
                                author_div_tag = author_date_div_tag.find('div', {'class': 'author'})
                                author = author_div_tag.getText().strip() if author_div_tag is not None else ''
                                date_div_tag = author_date_div_tag.find('div', {'class': 'date'})
                                date = date_div_tag.get_text().strip() if date_div_tag is not None else ''
                            
                            if date:
                                try:
                                    date_split = date.split('/')
                                    month = int(date_split[0])
                                    day = int(date_split[1])
                                    if day > 0 and day < 10:
                                        day = f'0{day}'
                                    if month > 0 and month < 10:
                                        date = f'0{month}-{day}'
                                    else:
                                        date = f'{month}-{day}'
                                except ValueError:
                                    logger.error(f'Obtain date of month failed: {date}')
                                else:
                                    temp_one_of_article = [
                                        self.__task_id, self.__auth_user, self.__board_name,
                                        title, link, push_count,
                                        author, date, current_page_count + 1
                                    ]
                                    # logger.debug(temp_one_of_article)
                                    info.append(dict(zip(self.__info_columns, temp_one_of_article)))
                current_page_article_image_related.clear()
                if is_last_page is True:
                    break
            # info = sorted(info, key=lambda x: x['date'], reverse=True)
            info = sorted(info, key=lambda x: x['page'], reverse=False)
            result['json_rows'] = info
            
        except Exception as e:
            logger.error(HandleException.show_exp_detail_message(e))
        return result

    def ptt_scrape_by_keyword(self, keyword=None, search_page_limit=1, page_search_over_limit=False):
        info = []
        result = {
            'json_rows': ''
        }
        try:
            if self.__base_url is None:
                raise Exception('The base url is required.')
            full_url = self.__base_url if keyword is None or not keyword else self.__base_url.replace('/index.html', '') + f'/search?q={keyword}'
            current_page_count = 0
            is_last_page = False
            while True:
                current_page_article_title = []
                logger.info(f'Obtain article from the url: {full_url}')
                with RequestAnalysisData(
                    url=full_url, mode=False, cookies={'over18': '1'}, headers=self.__headers
                ) as soup:
                    main_container_div_tag = soup.find('div', {'id': 'main-container'})
                    # topbar_container_div_tag = soup.find('div', {'id': 'topbar-container'})

                    if main_container_div_tag is None:
                        raise Exception("Load main container div tag failed.")

                    # article_topbar_div_tag = topbar_container_div_tag.find('div', {'id': 'topbar', 'class': 'bbs-content'})
                    # article_topbar_a_tag = article_topbar_div_tag.find_all('a')[1] if article_topbar_div_tag is not None else None
                    # board_name = article_topbar_a_tag.getText().strip().replace('看板 ', '') if article_topbar_a_tag is not None else 'Unknown'

                    # if not result['task_mark']:
                    #     result['task_mark'] = board_name

                    # logger.info(f"Task mark the article type is: {result['task_mark']}")

                    article_div_tag = main_container_div_tag.find('div', {'class': 'r-list-container action-bar-margin bbs-screen'})
                    all_article_div_tag = article_div_tag.find_all('div', {'class': 'r-ent'}) if article_div_tag is not None else None
                    
                    if all_article_div_tag is None:
                        raise Exception("Load all article page div tag failed.")
                    
                    action_bar_div_tag = main_container_div_tag.find('div', {'id': 'action-bar-container'})
                    go_back_div_tag = action_bar_div_tag.find('div', {'class': 'btn-group btn-group-paging'})
                    go_back_a_tag = go_back_div_tag.find_all('a', {'class': 'btn wide'}, string="‹ 上頁")
                    
                    if go_back_a_tag is None or not go_back_a_tag:
                        is_last_page = True
                    else:
                        full_url = "https://www.ptt.cc/" + go_back_a_tag[0]['href']

                    logger.info(f'Go back article link is: {full_url}')

                    for index, one_of_article in enumerate(all_article_div_tag, 1):
                        # logger.info(f'Staring get the {index} article')
                        title_div_tag = one_of_article.find('div', {'class': 'title'})
                        title_and_link_a_tag = title_div_tag.find('a') if title_div_tag is not None else None
                        title = title_and_link_a_tag.getText().strip().replace(u'\u3000', u'') if title_and_link_a_tag is not None else ''
            
                        if title and self.__check_include_match_items(check_string=title, pattern=self.__article_title_filter) is None:
                            # logger.info(f'Obtain article title is: {title}')
                            link = "https://www.ptt.cc" + title_and_link_a_tag['href'] if title_and_link_a_tag is not None else ''
                            push_count_div_tag = one_of_article.find('div', {'nrec'})
                            
                            if push_count_div_tag is not None:
                                push_count = str(push_count_div_tag.get_text().strip())
                                if push_count and push_count.isdigit() is True:
                                    push_count = int(push_count)
                                elif push_count and push_count.isdigit() is False and push_count.find('爆') != -1:
                                    push_count = 100
                                elif push_count and push_count.isdigit() is False and push_count.find('X') != -1:
                                    push_count = -1
                                else:
                                    push_count = 0
                            
                            author_date_div_tag = one_of_article.find('div', {'class': 'meta'})
                            if author_date_div_tag is not None:
                                author_div_tag = author_date_div_tag.find('div', {'class': 'author'})
                                author = author_div_tag.getText().strip() if author_div_tag is not None else ''
                                date_div_tag = author_date_div_tag.find('div', {'class': 'date'})
                                date = date_div_tag.get_text().strip() if date_div_tag is not None else ''
                            
                            if date:
                                try:
                                    date_split = date.split('/')
                                    month = int(date_split[0])
                                    day = int(date_split[1])
                                    if day > 0 and day < 10:
                                        day = f'0{day}'
                                    if month > 0 and month < 10:
                                        date = f'0{month}-{day}'
                                    else:
                                        date = f'{month}-{day}'
                                except ValueError:
                                    logger.error(f'Obtain date of month failed: {date}')
                                else:
                                    current_page_article_title.append(title)
                                    temp_one_of_article = [
                                        self.__task_id, self.__auth_user, self.__board_name,
                                        title, link, push_count,
                                        author, date, current_page_count + 1
                                    ]
                                    # logger.debug(temp_one_of_article)
                                    info.append(dict(zip(self.__info_columns, temp_one_of_article)))
                # logger.warning(current_page_article_title)
                current_page_count += 1
                if page_search_over_limit is False and current_page_count == search_page_limit or is_last_page is True or any([True for one_of_title in current_page_article_title if one_of_title.find(keyword) != -1]) is False:
                    logger.info(f'Not found keyword {keyword} info or page has been last page.')
                    current_page_article_title.clear()
                    break
                current_page_article_title.clear()
            info = sorted(info, key=lambda x: x['page'], reverse=False)
            result['json_rows'] = info
            # write_iterator_to_log(result['task_mark'])
        except Exception as e:
            logger.error(HandleException.show_exp_detail_message(e))
        return result