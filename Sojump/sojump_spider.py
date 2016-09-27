#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import csv
import time
import requests


def collectId():
    keywords = raw_input('Enter keywords: ')
    url_det = 'http://www.sojump.com/publicsurveys.aspx?keyword=' + keywords
    page_det = requests.get(url_det).text
    pattern_page_upper = re.compile(r'.*?</ul>.*?<span class="text" style="padding-left: 10px">.*?<span id="ctl00_ContentPlaceHolder1_lbTotal" class="biaoti">(.*?)</span>.*?</span>.*?</div>.*?</div>.*?', re.S)
    page_upper = re.search(pattern_page_upper, page_det)
    page_upper_num = int(page_upper.group(1))
    print '\nFind %d reports' % page_upper_num
    page_upper = (page_upper_num / 8) + 1
    with open('id.csv', 'w') as file_write:
        writer = csv.writer(file_write)
        for num in range(1, page_upper):
            url = 'http://www.sojump.com/publicsurveys.aspx?keyword=%s&sort=1&pagenumber=%d' % (keywords, num)
            response = requests.get(url)
            page = response.text
            pattern = re.compile(r"<div class='post_item'><div class='post_item_body'><h3><a href='.*?/jq/(.*?).aspx'  target='_blank'>.*?<div class='clear'></div></div>", re.S)
            id_all = re.findall(pattern, page)
            for id in id_all:
                writer.writerow([id])
    print 'Get all id'


def collectData():
    if not os.path.exists('report'):
        os.makedirs('report')
    with open('id.csv', 'r') as file_read:
        reader = csv.reader(file_read)
        print 'Spider start!\n'
        count = 0
        for id in reader:
            url = 'http://www.sojump.com/report/%s.aspx' % id[0]
            response = requests.get(url)
            page = response.text

            check_finish = re.compile(r".*?<!DOCTYPE.*?", re.S)
            finished = re.search(check_finish, page)
            check_readable = re.compile(r'.*?<div id="divSumData">.*?', re.S)
            readable = re.search(check_readable, page)
            able = finished and readable

            if not able:
                continue

            else:
                count += 1
                filename = id[0] + '.csv'
                path = os.path.join('report', filename)
                with open(path, 'w') as file_write:
                    writer = csv.writer(file_write)

                    # Get all questions
                    pattern_part = re.compile(r".*?<div style='border-bottom:1px solid #eeeeff;padding:5px 0 10px;'>(.*?)<div style='clear:both;'></div></div></div>.*?", re.S)
                    part_all = re.findall(pattern_part, page)

                    for part in part_all:

                        # Get the title of question
                        pattern_title = re.compile(r".*?<div style='margin:5px 0;line-height: 24px;'>(.*?)<span style='color:#0066FF;'>.*?", re.S)
                        result_title = re.search(pattern_title, part)
                        title = result_title.group(1)
                        writer.writerow([title])

                        # Get all options
                        pattern_option = re.compile(r"<td val='.*?'>.*?</td><td align='center'>.*?</td><td percent='.*?'><div class='bar'><div style='width:.*?%; display: block;' class='precent'><img height='13' width='149' alt='' src='.*?'></div></div><div style='margin-top:3px;float:left;'>.*?</div><div style='clear:both;'></div></td></tr>", re.S)
                        option_all = re.finditer(pattern_option, part)

                        writer.writerow(['选项', '小计', '比例'])
                        total = 0
                        for option in option_all:
                            pattern_data = re.compile(r".*?<td val='.*?'>(.*)(&nbsp;)?.*?</td><td align='center'>(.*?)</td><td percent='(.*?)'><div class='bar'><div style='width:.*?", re.S)
                            data = re.search(pattern_data, option.group())
                            a, b, c = data.group(1), data.group(3), data.group(4)
                            c += '%'
                            writer.writerow([a, b, c])
                            total += int(b)

                        writer.writerow(['本题有效填写人次', str(total)])
                        writer.writerow([''])

                now_time = time.strftime("[%H:%M:%S]", time.localtime())
                print '%s %s' % (now_time, filename)

    print '\n%d reports have been collected!' % count


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print 'Wellcome to Sojump spider!'
    collectId()
    collectData()
