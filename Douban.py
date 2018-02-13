import urllib.request
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/60.0.3112.113 Safari/537.36'}
Category = {'Drama': '剧情',
            'Comedy': '喜剧',
            'Thriller': '惊悚',
            'Action': '动作',
            'Romantic': '爱情',
            'Adventure': '冒险',
            'Crime': '犯罪',
            'Fiction': '科幻',
            'Suspense': '悬疑',
            'Terror': '恐怖',
            'Fantasy': '奇幻',
            'Family': '家庭',
            'Biography': '传记',
            'Animation': '动画',
            'Documentary': '纪录片',
            'War': '战争',
            'History': '历史',
            'Music': '音乐',
            'Sport': '运动',
            'Westernes': '西部',
            'Disaster': '武侠',
            'Child': '儿童',
            'Custume': '古装',
            'Wuxia': '武侠',
            'Absurd': '荒诞',
            'Song & Music': '歌舞',
            'Erotic': '情色',
            'Noir': '黑色电影'}

Country = {'Mainland China': '大陆',
           'The United States': '美国',
           'Hong Kong': '香港',
           'Taiwan': '台湾',
           'Japan': '日本',
           'Korea': '韩国',
           'The United Kingdom': '英国',
           'France': '法国',
           'Germany': '德国',
           'Italia': '意大利',
           'Spain': '西班牙',
           'India': '印度',
           'Thailand': '泰国',
           'Russia': '俄罗斯',
           'Iran': '伊朗',
           'Canada': '加拿大',
           'Australia': '澳大利亚',
           'Brazil': '巴西',
           'Sweden': '瑞典',
           'Denmark': '丹麦',
           'Ireland': '爱尔兰'}

def url_request(number):
    url = str('https://movie.douban.com/subject/' + number[1:])
    try:
        req = urllib.request.Request(url=url, headers=headers)
        content = res = urllib.request.urlopen(req).read()
        content = content.decode()
        return content
    except:
        print('invalid url: ' + url)
        return ''

def get_information(number):
    content = url_request(number)
    if content != '':
        mark_beg = content.find('<span property="v:itemreviewed">')
        content = content[mark_beg:]
        mark_end = content.find('\n')
        title = (content[len('<span property="v:itemreviewed">'): mark_end - 7])
        rating_mark = '<strong class="ll rating_num" property="v:average">'
        rating = content[content.find(rating_mark)+len(rating_mark): content.find(rating_mark)+len(rating_mark) + 3]
        mark_beg = content.find("导演</span>")
        mark_end = content.find('<div id="interest_sectl">')
        content = content[mark_beg: mark_end].replace(' ','').replace('-', '').split('\n')[:9]
        if content[0] != '':
            (directors, screenwriters, actors, categories, countries, year, time) = get_detail(content)
            print(number + ',,', title +',,', rating+',,', str(directors)+',,', str(screenwriters)+',,', str(actors)+',,', str(categories)+',,', str(countries)+',,', year + ',,' + time)
            return (title, rating, directors, screenwriters, actors, categories, countries, year, time)
        else:
            print('invalid url')
            return''
    else:
        return ''

def get_detail(content):
    directors = []
    actors = []
    screenwriters = []
    categories = []
    countries = []
    country = ''
    category = ''
    screenwriter = ''
    director = ''
    actor = ''
    year = ''
    time = ''
    for n in content[0]:
        if n.isdigit():
            director += n
        elif director != '':
            if len(director) > 5:
                directors.append(director)
            director = ''
    for n in content[1]:
        if n.isdigit():
            screenwriter += n
        elif screenwriter != '':
            if len(screenwriter) > 5:
                screenwriters.append(screenwriter)
            screenwriter = ''
    for n in content[2]:
        if n.isdigit():
            actor += n
        elif actor != '':
            if len(actor) > 5:
                actors.append(actor)
            actor = ''
    for n in content[3]:
        if u'\u4e00' <= n <= u'\u9fff':
            category += n
        elif category != '':
            categories.append(category)
            category = ''
    for n in content[5]:
        if u'\u4e00' <= n <= u'\u9fff':
            country += n
        elif country != '':
            countries.append(country)
            country = ''
    for n in content[7]:
        if n.isdigit():
            year += n
        elif year != '':
            break
    for n in content[8]:
        if n.isdigit():
            time += n
        elif time != '':
            break
    categories = categories[1:]
    countries = countries[2:]
    return (directors, screenwriters, actors, categories, countries, year[:4], time)

def get_list(requirement):
    menu = []
    url = 'https://movie.douban.com/tag/'
    utfcode = requirement[0].encode('utf-8')
    utfcode = str(utfcode)
    url += utfcode[2:-1].replace("\\", '%').replace('x', '')
    for i in requirement[1:]:
        if not i.isdigit():
            utfcode = i.encode('utf-8')
            utfcode = str(utfcode)
            url += ('%20' + utfcode[2:-1].replace("\\", '%').replace('x', ''))
        else:
            url += ('%20' + i)
    base_url = url + '?start='
    first_url = base_url + '&type=T'
    print(first_url)
    req = urllib.request.Request(url=first_url, headers=headers)
    content = urllib.request.urlopen(req).read()
    content = content.decode()
    number = ''
    if '没有找到符合条件的电影' in content:
        print('No item found')
        return
    elif '<span class="thispage" data-total-page="' not in content:
        print('Less than 20 items to be crawled')
        number = '1'
    else:
        mark = content.find('data-total-page="') + len('data-total-page="')
        for n in content[mark:]:
            if n.isdigit():
                number += n
            else:
                break
        print('About ' + str(int(number) * 20) + ' item to be crawled')
    for i in range(0, int(number)):
        if i % 10 == 0 and i != 0:
            input('Pleasse change IP addreess, press \'Enter\' when ready')
        crawling_url = base_url + str(i * 20) + '&type=T'
        req = urllib.request.Request(url=crawling_url, headers=headers)
        content = urllib.request.urlopen(req).read()
        content = content.decode()
        print('Crawling ' + str(i * 20 + 1) + ' - ' + str(i * 20 + 20) +' items')
        while('subject' in content):
            a = content.find('movie.douban.com/subject/')
            content = content[a + 25:]
            m_number = ''
            for n in content:
                if n.isdigit():
                    m_number += n
                elif m_number != '':
                    if m_number not in menu:
                        menu.append(m_number)
                    break
        for m_number in menu:
            get_information('m' + m_number)
            menu = []
    return

def main():
    categories = list(Category.keys())
    countries = list(Country.keys())
    print('Choose the country interested:')
    for i in range(len(countries)):
        print(str(i) + '. ' + countries[i])
    country = input('Enter the number only, leave blank for not specific.\nTo select multiple items, separate with a comma.\n')
    print('Choose the category interested:')
    for i in range(len(categories)):
        print(str(i) + '. ' + categories[i])
    category = input('Enter the number only, leave blank for not specific.\nTo select multiple items, separate with a comma.\n')
    category = category.split(',')
    country = country.split(',')
    if category != ['']:
        for i in range(len(category)):
            category[i] = Category[categories[int(category[i])]]
    if country != ['']:
        for i in range(len(country)):
            country[i] = Country[countries[int(country[i])]]
    requirement = ['电影'] + category + country
    while '' in requirement:
        requirement.remove('')
    get_list(requirement)

main()

# result explanation:
# m1292720    ,, 阿甘正传 Forrest Gump        ,, 9.4   ,, ['1053564']     ,, ['1000393']           ,, ['1054450', '1002676', '1031848', '1031912', '1041112', '1025137'],, ['剧情', '爱情']               ,, ['美国']          ,, 1994     ,,142
# movie number,, Chinese name + English name,, rating,, list of directors,, list of screen writers,, list of actors and actresses                                      ,, category('drama', 'romantic'),, country(the U.S.),, year made,, runtime

# how to find movie website?
# go to https://movie.douban.com/subject/   +    movie number(without the 'm')

# how to find director/screen writer/actor/actress website?
# go to https://movie.douban.com/celebrity/  +   celebrity number in the list