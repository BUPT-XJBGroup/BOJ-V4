#encoding: utf-8 
from django.db import models, transaction
from django.core.exceptions import ValidationError
import math
import re
from lcs import lcs
from conf import keywords, symbol, lang, rule


mapKeywords={"g++":{},"gcc":{},"java":{}}
mapSymbol={"g++":{},"gcc":{},"java":{}}
treeMem=[] 

class QUERY:
    uid=0
    similar_score=0.0
    lan=''
    subs=[]
    def __init__(self):
        self.uid = 0
        self.similar_score = 0.0
        self.subs=[]
        lan=''

class CheckCheat(models.Model):
	
    MAX_LEN = 128
    DB_QUERY_FAILED = -1
    DB_UPDATE_FAILED=-1
    DB_UPDATE_SUCCEED=1
    DB_QUERY_SUCCEED=1
    MAX_CODE_LENGTH=1055360
    QUERY_QUEENING=-1
    QUERY_JUDGING=0
    MAX_USERS=2
	
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
    def solve2(cls,Str,len1,len2):
        tlen = len(Str[0])
        plen = len(Str[1])
    #    print Str[0]
     #   print Str[1]
       # print min(plen,tlen)
        ans = 0
        MML = 4
        MaxLen=MML+1
       # print Str[0]
       # print Str[1]
        while MaxLen>MML:
            MaxLen = MML
            j = 1
            now_i=0
            #dp=[cls.MAX_CODE_LENGTH*[0],cls.MAX_CODE_LENGTH*[0]]
            
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

    @classmethod
    def probably2(cls,s,len1,len2):
        return 2.0*float(s)/(float(len1+len2))

    @classmethod
    def probably1(cls,s,len1,len2):
        return float(s)/(float(len1+len2)*0.5)

    @classmethod
    def solve1(cls,Str,len1,len2):
        j = 1
        now_i=0
        dp=[cls.MAX_CODE_LENGTH*[0],cls.MAX_CODE_LENGTH*[0]]
        for i in xrange(1,len1+1):
            for j in xrange(1,len2+1):
                dp[now_i][j]=dp[1-now_i][j]
                if dp[now_i][j-1]>dp[now_i][j]:
                    dp[now_i][j]=dp[now_i][j-1]
                if Str[0][i-1]==Str[1][j-1]:
                    if dp[1-now_i][j-1]+1>dp[now_i][j]:
                        dp[now_i][j] = dp[1-now_i][j-1]+1
            now_i = 1-now_i

        return dp[1-now_i][j]

    @classmethod
    def test1(cls,query_info):
        length=[0]*2
        similar=0
        Str=['','']
        for j in xrange(0,2):
    	    code = query_info.subs[j]
            
           # print query_info.codes[j]
            try:
                all_code=code.decode('utf-8', 'ignore')
            finally:
          	print ("all_code mark")
            all_code = re.sub(rule["g++"],"",all_code)
        #    print all_code
            lent=len(all_code)
            temp=''
            for i in xrange(0,lent):
                temp+=all_code[i]
            temp=re.findall('\w+|{|}',temp)
            tempLen=len(temp)
         #   print mapKeywords[query_info.subs[j].code_language]
            for i in xrange(tempLen):
                if temp[i] in mapKeywords["g++"]:
                    Str[j]+=str(mapKeywords["g++"][temp[i]])#append(mapKeyword[temp[i]])
                    length[j]+=1
                if temp[i]=='{' or temp[i]=='}':
                    Str[j]+=str(temp[i])#.append(temp[i])
                    length[j]+=1
        similar=cls.solve1(Str,length[0],length[1])
        return cls.probably1(similar, length[0], length[1])*100

    @classmethod
    def test2(cls,query_info):
        length=[0]*2
        similar=0
        Str=['','']
        for j in xrange(0,2):
            code= query_info.subs[j]
            try:
                all_code=code.decode('utf-8', 'ignore')
            finally:
                print ("test2")
            all_code = re.sub(rule["g++"],"",all_code)
            lent=len(all_code)
            for i in xrange(0,lent):
                if all_code[i]!=' ' and all_code[i]!='\r' and all_code[i]!='\n' and all_code[i]!='\t':
                    Str[j]+=str(all_code[i])#.append(query_info.codes[j][i])
                    length[j]+=1

       # print "str2="
       # print Str
    #    print Str[0]
     #   print Str[1]
     #   print length[0],length[1]
        similar=cls.solve2(Str,length[0],length[1])
     #   print similar
        return cls.probably2(similar,length[0],length[1])*100

    
    @classmethod
    def solve3(cls,lanType,Str,len1,len2):
        num=[[0]*100,[0]*100]
     #   print mapSymbol[lanType]
        for j in xrange(0,2):
            lent=len(Str[j])
            for i in xrange(0,lent):
                tmp=Str[j][i]
                if not mapSymbol[lanType].has_key(tmp):
                    continue
                num[j][mapSymbol[lanType][tmp]]+=1
      #  print num[0]
       # print num[1]
        up=0
        down1=0
        down2=0
        symnum = len(symbol[lanType])
        for i in xrange(62+symnum):
            up+=float(num[0][i]*num[1][i])
            down1+=float(num[0][i]*num[0][i])
            down2+=float(num[1][i]*num[1][i])
        down1 = math.sqrt(down1)
        down2 = math.sqrt(down2)
        similar=up/down1/down2
        return similar

    @classmethod
    def test3(cls,query_info):
        length=[0,0]
        similar=0
        Str=['','']
        for j in xrange(0,2):
            code= query_info.subs[j]
            try:
                all_code=code.decode('utf-8', 'ignore')
            finally:
                print ("haha")
            all_code = re.sub(rule["g++"],"",all_code)
            lent=len(all_code)
            for i in xrange(0,lent):
                Str[j]+=str(all_code[i])
                length[j]+=1
        similar=cls.solve3("g++",Str,length[0],length[1])
        return similar*100

    @classmethod
    def similarJudge(cls,query_info):
        query_info.similar_score=0.0
        query_info.similar_score+=cls.test1(query_info)*0.5
     #   print "score1="
      #  print query_info.similar_score
        query_info.similar_score+=cls.test2(query_info)*0.5
       # print "score2="
       # print query_info.similar_score
        query_score_acos=cls.test3(query_info)
       # print "acos="
       # print query_score_acos
        if query_score_acos==100:
            query_info.similar_score=query_score_acos

    @classmethod
    def antiCheat(cls, code_a, code_b):
        cls.init()
	query_info = QUERY()
	query_info.subs.append(code_a)
	query_info.subs.append(code_b)
	cls.similarJudge(query_info)
	print query_info.similar_score, " --- "
        return query_info.similar_score		

  
# Create your models here.
