#include <iostream>
#include <cmath>
#include <algorithm>
#include <cstring>
#include <cstdio>
#include <string>
#include <cstdlib>


using namespace std;

int lcs(const string & a, const string & b, int & lcs_st_a, int & lcs_st_b) 
{
    int len_a = a.length();
    int len_b = b.length();
    
    int maxlen = max(len_a, len_b);

    int *f[2];
    f[0] = new int[maxlen+1]();
    f[1] = new int[maxlen+1]();

    int i, j, len=0, st_a=0, st_b=0;
    int now = 0;
    for (i = 0; i < len_a; ++i, now^=1)
        for (j = 0; j < len_b; ++j) {
            if (a[i]!='$' && b[j]!='$' && a[i]==b[j]) {
                f[now][j+1] = f[now^1][j]+1;
                if (f[now][j+1] > len) {
                    len = f[now][j+1];
                    st_a = i-len+1;
                    st_b = j-len+1;
                }
            } else {
                f[now][j+1] = 0;
            }
        }

    delete [] f[0];
    delete [] f[1];
    delete [] f;

    lcs_st_a = st_a;
    lcs_st_b = st_b;

    return len;
}

int solve2(char str1[], char str2[], int len1, int len2)
{
    string s1(str1);
    string s2(str2);

    int tlen = s1.length();
    int plen = s2.length();

    int ans = 0;
    int MML = 4;
    int MaxLen = MML+1;
    
    int j, now_i, k, s, t;

    while (MaxLen > MML)
    {
        MaxLen = MML;
        j = 1;
        now_i = 0;
        // mark //
        k = lcs(s1, s2, s, t);
        if (k < MaxLen)
            continue;
        if ((s+k<tlen) && (s1[s+k] != '$'))
            s1 = s1.substr(0, s) + "$" + s1.substr(s+k, tlen-s-k);
        else
            s1 = s1.substr(0, s) + s1.substr(s+k, tlen-s-k);
        tlen = s1.length();
        if ((t+k<plen) && s2[t+k] != '$')
            s2 = s2.substr(0, t) + "$" + s2.substr(t+k, plen-t-k);
        else
            s2 = s2.substr(0, t) + s2.substr(t+k, plen-t-k);

        plen = s2.length();
        ans += k;
        MaxLen = k;
    }

    return ans;
}

