import os
from module.handle_exception import HandleException
from module.reptile import Automation, AnalysisData
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from crawler.config import Initialization as Init
from module.log_generate import Loggings
import re
import pandas as pd


logger = Loggings()

def write_iterator_to_log(iterator):
    [logger.info(read_iterator_info) for read_iterator_info in iterator]

def write_iterator_multiple_to_log(iterator):
    for outside_index, outside in enumerate(iterator, 1):
        logger.info(f'The {outside_index} iterator')
        logger.info('------------------------------------------------------')
        for inner_index, inner_iterator in enumerate(outside, 1):
            logger.info(f"The {inner_index} data is {inner_iterator}")
        logger.info('------------------------------------------------------')

def write_iterator_three_to_log(iterator):
    for outside in iterator:
        for inner_index, inner in enumerate(outside, 1):
            logger.info(f'The {inner_index} iterator')
            logger.info('------------------------------------------------------')
            for innermost_index, innermost in enumerate(inner, 1):
                logger.info(f"The {innermost_index} data is: {innermost}")
            logger.info('------------------------------------------------------')

class GoogleSearchInfo():
    def __init__(self, **crawler):
        self.__base_url = Init.base_url_list['google_search']
        self.__browser_type = Init.browser_type[0]
        self.__webdriver_path = Init.webdriver_path[self.__browser_type]
        self.__open_browser = Init.open_browser
        self.__task_id = crawler['task_id']
        self.__auth_user = crawler['auth_user']
        self.__page_count = crawler['page_count']
        self.__keyword = crawler['keyword']
        self.__search_type = crawler['data_type']

    def __check_list_none(self, check_list):
        return None in check_list

    def __wait_element_load(self, **load):
        return WebDriverWait(load['driver'], load['wait_time'], load['check_time']).until(EC.presence_of_all_elements_located(load['locator']))

    def __wait_element_load_for_clickable(self, **load):
        return WebDriverWait(load['driver'], load['wait_time'], load['check_time']).until(EC.element_to_be_clickable(load['locator']))

    def __filter_duplicate_items(self, filter_condition, filter_items):
        return re.sub(filter_condition, '', filter_items)

    def __check_float(self, potential_float):
        try:
            float(potential_float)
            return True
        except ValueError:
            return False

    def __loading_page_source(self):
        page_source_list = []
        try:
            with Automation(
                webdriver_path=self.__webdriver_path,
                open_browser=self.__open_browser,
                browser_type=self.__browser_type
            ) as d:
                browser_version = d.capabilities['browserVersion']
                browser_name = d.capabilities['browserName']
                logger.info(f"Search keyword is: {self.__keyword}, Search page count is: {self.__page_count}, Data Type is: {self.__search_type}, Browser name is: {browser_name}, Browser version is: {browser_version}")

                search_params_list = ['nws', 'vid', 'shop', 'isch', 'bks']
                country_code_list = ['en', 'zh-TW']

                if self.__search_type == 'google news':
                    search_type = search_params_list[0]
                elif self.__search_type == 'google video':
                    search_type = search_params_list[1]
                else:
                    raise Exception("No match search type option.")

                #TODO 定義 Google 搜尋的關鍵字與搜尋種類 (如: 新聞, 影片)
                search_condition = f'{self.__base_url}/search?q={self.__keyword}&tbm={search_type}&hl={country_code_list[0]}'
                logger.debug(f'search condition: {search_condition}')
                d.get(search_condition)

                page_source_list.append(d.page_source)
                logger.info(f'Load 1 page source finish')

                for _ in range(0, self.__page_count - 1):
                    next_page_button = self.__wait_element_load_for_clickable(
                        driver=d,
                        locator=(By.XPATH, "//*[@id='pnnext']/span[2]"),
                        wait_time=10,
                        check_time=1)
                    next_page_button.click()
                    self.__wait_element_load(driver=d, locator=(By.CLASS_NAME, "GyAeWb"), wait_time=10, check_time=1)
                    self.__wait_element_load(driver=d, locator=(By.CLASS_NAME, "eqAnXb"), wait_time=10, check_time=1)
                    page_source_list.append(d.page_source)
                    logger.info(f'Load {_ + 2} page source finish')
            logger.info("Get all page static source")
        except Exception as e:
            err_msg = HandleException.show_exp_detail_message(e)
            logger.error(err_msg)
            raise Exception(err_msg)
        finally:
            return page_source_list

    #TODO 獲取 Google 搜尋的新聞資訊
    def __get_news(self, page_source_list):
        info = []
        result = {
            'json_rows': ''
        }
        try:
            logger.info(f'Will load source page total: {len(page_source_list)}')
            info_columns = ['username' ,'task', 'keyword', 'title', 'summary', 'updated_time', 'url', 'newspaper', 'search_page']
            logger.info("Starting get hot news information from page source")
            for page_count, page_source in enumerate(page_source_list, 1):
                current_info_dict = []
                if page_source is None:
                    raise Exception("Load static page source failed")
                logger.info(f"Current page is: {page_count}")

                with AnalysisData(page_source, 'html.parser') as soup:
                    search_div_tag = soup.find('div', {'id': 'search'})
                    news_main_div_tag = search_div_tag.find('div', {'class': 'v7W49e'}) if page_count > 0 and search_div_tag is not None or not search_div_tag else None
                    if news_main_div_tag is None:
                        raise Exception('Not found any match news div tag')
                    else:
                        #TODO 迭代獲取當前頁面的每一筆新聞資訊
                        for current_page_news_count, current_g_card_element in enumerate(news_main_div_tag, 1):
                            #TODO 獲取當前第 n 筆的新聞資訊
                            one_of_card_div_tag = current_g_card_element.find('div', {'class': 'iRPxbe'})
                            if one_of_card_div_tag is not None:
                                #TODO 獲取新聞社名稱
                                newspaper_div_tag = one_of_card_div_tag.find('div', {'class': 'CEMjEf NUnG9d'})
                                newspaper = newspaper_div_tag.get_text().strip().replace('\n', '') if newspaper_div_tag is not None else ''
                                #TODO 獲取標題名稱
                                title_div_tag = one_of_card_div_tag.find('div', { 'class', 'mCBkyc y355M ynAwRc MBeuO nDgy9d' })
                                title = title_div_tag.get_text().strip().replace('\n', '') if title_div_tag is not None else ''
                                #TODO 獲取簡介內容
                                summary_div_tag = one_of_card_div_tag.find('div', { 'class': 'GI74Re nDgy9d' })
                                summary = summary_div_tag.get_text().strip().replace('\n', '') if summary_div_tag is not None else ''
                                #TODO 獲取新聞資訊更新的時間
                                update_time_div_tag = one_of_card_div_tag.find('div', { 'class': 'OSrXXb ZE0LJd' })
                                update_time = update_time_div_tag.find('span').get_text().strip()
                                
                                #TODO 獲取資訊連結
                                link_a_tag = current_g_card_element.find('a')
                                link = link_a_tag['href'] if link_a_tag is not None else ''
                                temp_list = [self.__auth_user, self.__task_id, self.__keyword, title, summary, update_time, link, newspaper, page_count]

                                if any(temp_list) is True:
                                    current_info_dict.append(dict(zip(info_columns, temp_list)))
                                else:
                                    logger.error(f'Found empty in current page {page_count} the {current_page_news_count} data')
                                if not newspaper and not title and not summary and not update_time and not link:
                                    raise Exception(f"Data catch empty\n{current_info_dict}")
                    info.extend(list({v['title']:v for v in current_info_dict}.values()))
            result['json_rows'] = info
            logger.info("Finish get google search news information from page source")
        except Exception as e:
            logger.error(HandleException.show_exp_detail_message(e))
        return result

    #TODO 獲取 Google 搜尋的影片資訊
    def __get_video(self, page_source_list):
        info = []
        result = {
            'json_rows': ''
        }
        try:
            logger.info(f'Will load source page total: {len(page_source_list)}')
            info_columns = ['username' ,'task', 'keyword', 'title', 'summary', 'updated_time', 'url', 'video_length', 'uploader', 'search_page']
            logger.info("Starting get video information from page source")
            for page_count, page_source in enumerate(page_source_list, 1):
                current_info_dict = []
                if page_source is None:
                    raise Exception("Load static page source failed")
                logger.info(f"Current page is: {page_count}")
                with AnalysisData(page_source, 'html.parser') as soup:
                    search_div_tag = soup.find('div', {'id': 'search'})
                    video_main_div_tag = search_div_tag.find('div', {'class': 'v7W49e'}) if page_count > 0 and search_div_tag is not None or not search_div_tag else None
                    if video_main_div_tag is None:
                        raise Exception('Not found any match video div tag')
                    else:
                        for current_page_video_count, current_video_items in enumerate(video_main_div_tag, 1):
                            video_items_outer_div_tag = current_video_items.find('div', {'class': 'g dFd2Tb'})
                            video_items_first_div_tag = video_items_outer_div_tag.find('div', {'class': 'ct3b9e'})
                            if video_items_first_div_tag is not None:
                                title_h3_tag = video_items_first_div_tag.find('h3', {'class': 'LC20lb MBeuO DKV0Md'})
                                title = title_h3_tag.getText().strip().replace('\n\r', '')
                                video_a_tag = video_items_first_div_tag.find('a')
                                link = video_a_tag['href'] if video_a_tag is not None else ''
                            else:
                                title = ''
                                link = ''
                            video_items_second_div_tag = video_items_outer_div_tag.find('div', {'class': 'dXiKIc'})
                            if video_items_second_div_tag is not None:
                                video_time_div_tag = video_items_second_div_tag.find('div', {'class': 'J1mWY'})
                                video_time = video_time_div_tag.find('div').get_text().strip() if video_time_div_tag else ''
                            else:
                                video_time = ''
                            video_items_third_div_tag = video_items_outer_div_tag.find('div', {'class': 'mSA5Bd'})
                            summary_tag = video_items_third_div_tag.find('div', {'class': 'Uroaid'})
                            summary = summary_tag.getText().strip().replace('\n\r', '')if summary_tag is not None else ''
                            uploader_and_update_time_tag = video_items_third_div_tag.find('div', {'class': 'P7xzyf'})
                            uploader_and_update_time_span_tag = uploader_and_update_time_tag.find_all('span') if uploader_and_update_time_tag is not None else None
                            if uploader_and_update_time_span_tag is not None:
                                uploader = uploader_and_update_time_span_tag[1].getText().strip().replace('\n\r', '')
                                update_time = uploader_and_update_time_span_tag[2].getText().strip().replace('\n\r', '')
                            else:
                                uploader = ''
                                update_time = ''
                            temp_list = [self.__auth_user ,self.__task_id, self.__keyword, title, summary, update_time, link, video_time, uploader, page_count]
                            if any(temp_list) is True and link:
                                current_info_dict.append(dict(zip(info_columns, temp_list)))
                            else:
                                logger.error(f'Found empty in current page {page_count} the {current_page_video_count} data')
                info.extend(list({v['title']:v for v in current_info_dict}.values()))
            result['json_rows'] = info
            logger.info("Finish get video information from page source")
        except Exception as e:
            logger.error(HandleException.show_exp_detail_message(e))
        return result

    def scrape(self):
        result = {}
        try:
            logger.debug(f'搜尋類型: {self.__search_type}')
            page_source_list = self.__loading_page_source()
            if self.__check_list_none(page_source_list) is True:
                raise Exception("Load all source page failed")
            if self.__search_type == 'google news':
                result = self.__get_news(page_source_list)
            elif self.__search_type == 'google video':
                result = self.__get_video(page_source_list)
            else:
                raise Exception(f"No match search type option. Error type is: {self.__search_type}")
        except Exception as e:
            logger.error(HandleException.show_exp_detail_message(e))
        return result