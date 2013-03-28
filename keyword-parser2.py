#--coding=utf-8--
import urllib2
from BeautifulSoup import BeautifulSoup , NavigableString

###키워드를 받아서 구글에 검색하고 거기서 자료를 받아오는 함수.
def keyword_parser(keyword):
    keywords = ""
    a = keyword.split(' ')
    if len(a) == 1:
        keywords = keyword;
    else:
        for word in a:
            keywords = keywords + "+" + word;
        keywords = keywords[1:]

    req = urllib2.Request("http://www.google.co.kr/search?q=" + keywords, headers={'User-Agent' : "Magic Browser"})
    iter1 = urllib2.urlopen(req);
    soup = BeautifulSoup(iter1);

    ### <a class = "spell" ....>을 모은다.
    links = soup.findAll("a", { "class" : "spell" })

    ### 한글 오타의 경우 is_ng로 따로 분류되는 듯
    is_ng = soup.findAll("span" , {"class" : "spell ng"})

    if len(links) == 0 :
        if len(is_ng) == 0 :
            ### 그냥 모든 띄워쓰기를 제거하고 반환.
            just_zip ="";
            b = keyword.split(' ');
            for word in b:
                just_zip = just_zip + word;
            print just_zip;
            return just_zip;
        else:
            ### 한글오타 처리 루틴 (아직 약간의 버그 있는듯.) 
            power_em = soup.findAll("em");
            print ((power_em[0].contents[0]).decode("utf-8")).encode('iso-8859-1' , 'replace')
            return power_em[0].contents[0]
    else:
        iter_man = links[0].contents;
        if len(iter_man) == 1 :
            iter2 = iter_man[0];
            iter3 = iter2.contents;
            iter4 = iter3[0]
            print (iter4.decode("utf-8")).encode('iso-8859-1' , 'replace');
            return iter4
        else:
            return_val = ""
            for word in iter_man:
                if isinstance(word, NavigableString):
                    return_val = return_val + word;
                else:
                    return_val = return_val + word.contents[0];
                    print (return_val.decode("utf-8")).encode('iso-8859-1' , 'replace');
                    return return_val        
            
        
    
    print "should not be reached" 
    return ;
