from django.db import models
from submission.models import Submission
from contest.models import Contest
from conf import keywords, symbol, lang, rule
from django.core.cache import cache
from multiprocessing import Pool
import json


mapKeywords={"g++":{},"gcc":{},"java":{}}
mapSymbol={"g++":{},"gcc":{},"java":{}}
treeMem=[]


class Pair(models.Model):
    sub1 = models.ForeignKey(Submission, related_name='submissions')
    sub2 = models.ForeignKey(Submission, related_name='submissions')
    ratio = models.FloatField()

    def __init__(self, *args, **kwargs):
        super(Pair, self)._init__(*args, **kwargs)
    
    def __unicode__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('cheat:pair-detail', kwargs={'pk': self.pk})

    @property
    def sub1(self):
        return self.sub1
    @sub1.setter
    def sub1(self, value):
        self.sub1 = value
 
    @property
    def sub2(self):
        return self.sub2
    @sub2.setter
    def sub2(self, value):
        self.sub2 = value

    @property
    def ratio(self):
        return self.ratio
    @ratio.setter
    def ratio(self, value):
        self.ratio = value
	
    @classmethod
    def probably2(cls,s,len1,len2):
        return 2.0*float(s)/(float(len1+len2))

    @classmethod
    def probably1(cls,s,len1,len2):
        return float(s)/(float(len1+len2)*0.5)
    
    # expect re-write into cpp
    @classmethod
    def solve2(cls,Str,len1,len2):
        tlen = len(Str[0])
        plen = len(Str[1])
        ans = 0
        MML = 4
        MaxLen=MML+1
        while MaxLen>MML:
            MaxLen = MML
            j = 1
            now_i=0
            k,s,t = lcs(Str[0],Str[1])
            if k<MaxLen:
                continue
            if s+k<tlen and Str[0][s+k]!='$':
                Str[0] = Str[0][0:s]+"$"+Str[0][s+k:tlen]
            else:
                Str[0] = Str[0][0:s]+Str[0][s+k:tlen]
            tlen=len(Str[0])
            if t+k<plen and Str[1][t+k]!='$':
                Str[1] = Str[1][0:t]+"$"+Str[1][t+k:plen]
            else:
                Str[1] = Str[1][0:t]+Str[1][t+k:plen]
            plen=len(Str[1])
            ans+=k
            MaxLen = k
        return ans

    def test1(self):
        Str1 = cache.get('re_code:' + str(self.sub1.pk))
        Str2 = cache.get('re_code:' + str(self.sub2.pk))
        len1 = cache.get('re_len:' + str(self.sub1.pk))
        len2 = cache.get('re_len:' + str(self.sub2.pk))
        len1 = int(len1)
        len2 = int(len2)
        try:
            similar= gcclib.lcs(Str1, Str2)
        except:
            pass
        return cls.probably1(similar, len1, len2)*100

    def test2(self):
        Str1 = cache.get('lcs_code:' + str(self.sub1.pk))
        Str2 = cache.get('lcs_code:' + str(self.sub2.pk))
        len1 = cache.get('lcs_len:' + str(self.sub1.pk))
        len2 = cache.get('lcs_len:' + str(self.sub2.pk))
        len1 = int(len1)
        len2 = int(len2)
        similar=cls.solve2([Str1, Str2], len1, len2)
	return cls.probably2(similar, len1, len2)*100

    def test3(self):
        length=[0,0]
        similar=0
        Str=['','']
	subs = [sub1, sub2]
        for j in xrange(0,2):
            all_code = cache.get('code_' + str(subs[j].pk))
            lent=len(all_code)
            for i in xrange(0,lent):
                try:
                    Str[j]+=str(all_code[i])
                    length[j]+=1
                except:
                    pass
        similar = gcclib.compare_similar(Str[0], Str[1])
        return similar
    
    def get_ratio(self):
        self.ratio = 0.0
        self.ratio += self.test1()*0.5
        self.ratio += self.test2()*0.5
        score_acos = self.test3()	
        if score_acos == 100:
            self.ratio = score_acos

class CheatMethod(object):

    @classmethod
    def AntiCheat(cls, pairs):
        for i in pairs:
            i.get_ratio()
        Pair.objects.bulk_create(pairs) # mark 

    @classmethod
    def cheat_handler(cls, contest_id):
        init()
        problem_list = Contest.objects.filter(pk = contest_id).problem.all()
        pairs = create_pairs(problem_list)
        #Multithreading Part
        p = Pool(8)

        ta = len(pairs)
        he = 0
        barrel_size = 200
        while (he < ta):
            if he + barrel_size < ta:
                tmp_pairs = pairs[he:he+barrel_size]
            else:
                tmp_pairs = pairs[he:ta]
            p.apply_async(AntiCheat, args=(tmp_pairs, ))
            he += barrel_size
        p.close()
        p.join()
        return True

    @classmethod
    def creat_pairs(cls, problem_list):
        pair_list = []
        usertable = {}
        for pp in problem_list:
            subs = Submisson.objects.filter(problem = pp, status = 'AC').order_by('pk') # mysql operation
            cache_init(subs) # initial the submissions
            for ss in subs:
                user = ss.user
            if user in usertable:
                if ss.create_time < usertable[user].create_time:
                    usertable[user] = ss
            else:
                usertable[user] = ss
            
            subs = []
            for i in usertable.values():
                subs.append(i)
            
            cls.init_redis(subs)

            for i in subs:
                for j in subs:
                    if i.pk < j.pk and i.language == j.language:
                        pair_list.append(Pair(i, j)) # xxx

        return pair_list
    
    @classmethod
    def init(cls):
        lent = len(lang)
        for i in xrange(0,lent):
            lanType=lang[i]
            keyLen = len(keywords[lanType])
            for j in xrange(0,keyLen):
                mapKeywords[lanType][keywords[lanType][j]] = chr(j+ord('a'))
            for j in xrange(0,26):
                tmp = chr(ord('a')+j)
                tmp2 = chr(ord('A')+j)
                mapSymbol[lanType][tmp] = j
                mapSymbol[lanType][tmp2] = j+26
                if j<10:
                    tmp3 = chr(ord('0')+j)
                    mapSymbol[lanType][tmp3] = j+52
            symLen = len(symbol[lanType])
            for j in xrange(0,symLen):
                tmp = symbol[lanType][j]
                mapSymbol[lanType][tmp] = 62+j

    @classmethod
    def cache_init(cls, subs):
        for sub in subs:
            all_code = re.sub(rule[sub.language],"", sub.code) # delete sth. through regular expression
            cache.set('code:' + str(sub.pk), all_code, 18000)

            lent=len(all_code)
            temp=''
            for i in xrange(0,lent):
                try:
                    temp+=str(all_code[i])
                except:
                    pass
            re_code = ""
            re_len = 0
            temp=re.findall('\w+|{|}',temp)
            tempLen=len(temp)

            for i in xrange(tempLen):
                if temp[i] in mapKeywords[sub.code_language]:
                    re_code +=str(mapKeywords[sub.code_language][temp[i]]) # append(mapKeyword[temp[i]])
                    re_len += 1
                if temp[i]=='{' or temp[i]=='}':
                    try:
                        re_code += str(temp[i]) #.append(temp[i])
                        re_len += 1
                    except:
                        pass

            cache.set('re_code:' + str(sub.pk), re_code, 18000)
            cache.set('re_len:' + str(sub.pk), re_len, 18000)

            lcs_code = ""
            lcs_len = 0

            for i in xrange(0,lent):
                if all_code[i] != ' ' and all_code[i]!='\r' and all_code[i]!='\n' and all_code[i]!='\t':
                    try:
                        lcs_code += str(all_code[i])#.append(query_info.codes[j][i])
                        lcs_len+=1
                    except:
                        pass

            cache.set('lcs_code:' + str(sub.pk), lcs_code, 18000)
            cache.set('lcs_len:' + str(sub.pk), lcs_len, 18000)


