
def f(x, cur):
    if x == '':
        return [cur]
    if x[0] == '-':
        return f(x[1:], cur*2) + f(x[1:], cur*2+1)
    else:
        return f(x[1:], cur*2+int(x[0]))

# Find EPI
def find_epi(n, ans):
    ang = [ 0 for i in range(0,2**n)]
    for i in range(0, len(ans)):
        yas = f(ans[i], 0) # ex) 0--1 = [1, 3, 5, 7]
        for x in yas:
            if ang[x] != 0:
                ang[x] = -1
            else:
                ang[x] = i+1

    ans2 = []    
    for i in ang:
        if i > 0 and i-1 not in ans2:
            ans2.append(i-1)
    ans2.sort()
    return ans2

# Column dominance
# 각각의 PI에 대해서 하나의 minterm이 다른 하나의 minterm에 완전히 겹친다면 작은 것만 가져감
def column_dominance(nepi, remain):
    nn = len(remain)
    check = [0 for i in range(0,nn)]
    cover = [f(pi,0) for pi in nepi]
    for i in range(0, nn):
        for j in range(i+1, nn):
            set_i = set()
            set_j = set()
            for idx in range(0,len(cover)):
                if remain[i] in cover[idx]:
                    set_i.add(idx)
                if remain[j] in cover[idx]:
                    set_j.add(idx)
            
            if set_i == set_i & set_j:   # i가 j에 포함된다!
                check[j] = 1
            elif set_j == set_i & set_j: # j가 i에 포함된다!
                check[i] = 1
    
    second_remain = []
    for i in range(0,nn):
        if check[i] == 0:
            second_remain.append(remain[i])
    
    return second_remain

# Row dominance
# nepi에 대해서 자신을 dominance하는 다른 nepi 찾기
def row_dominance(nepi, remain):
    nn = len(nepi)
    check = [0 for i in range(0,nn)]
    cover = [f(pi,0) for pi in nepi]
    for i in range(0,nn):
        for j in range(i+1,nn):
            set_i = set(cover[i]) & set(remain)
            set_j = set(cover[j]) & set(remain)
            
            if set_i == set_j:
                check[i if len(cover[i]) < len(cover[j]) else j] = 1
            elif set_i == set_i & set_j:
                check[i] = 1
            elif set_j == set_i & set_j:
                check[j] = 1
    
    second_epi = []
    for i in range(0,nn):
        if check[i] == 0:
            second_epi.append(nepi[i])

    return second_epi


def main():
    minterm = list(map(int, input().split()))

    ans = []
    n = minterm[0]
    m = minterm[1]
    pi = [[[] for j in range(0,n+1-i)] for i in range(0,n+1)]
    chk = {}
    # pi['-' 개수][1 bit 개수][원소 index]
    # Combined를 나타낼 chk 배열도 같음
    for i in range(0,m):
        x = minterm[i+2]
        a = ''
        cnt = 0
        while x > 0:
            a += str(x%2)
            cnt += x%2
            x = x//2
        while len(a) != n:
            a += '0'
        pi[0][cnt].append(a[::-1])
        chk[a[::-1]] = 0
    # (1) Find all PIs to construct a PI table
    for i in range(0,n):
        for j in range(0,n-i):
            for x in pi[i][j]:
                for y in pi[i][j+1]:
                    ang = -1
                    for l in range(0,n):
                        if x[l] != y[l]:
                            if ang != -1 or x[l] == '2' or y[l] == '2':
                                ang = -1
                                break
                            else:
                                ang = l
                    
                    if ang != -1:
                        chk[x] = chk[y] = 1
                        s = x[:ang] + '2' + x[ang+1:]
                        if s not in chk:
                            pi[i+1][j].append(s)
                            chk[s] = 0
        
        for j in range(0,n-i+1):
            for x in pi[i][j]:
                if chk[x] == 0:
                    ans.append(x)
    ans.sort()
    for i in range(0,len(ans)):
        ans[i] = ans[i].replace('2','-')
        
    '''
    (1) Find all PIs to construct a PI table
    (2) Find EPIs to simplify the table
            •No NEPI remained? Then quit.
    (3) Apply column dominance raw
    (4) Apply row dominance raw
    (5) Any simplification made from (2) and (3)?
            •Yes: go to (2)
            •No: move on to the next slide to learn Petrick’smethod
    '''
    minterm = minterm[2:]
    while (True):
        # (2) Find EPIs to simplify the table
        ans2 = find_epi(n, ans)
        remain = []         #remain minterms
        epi = []            #epis
        nepi = list(ans)    #non epis
        
        for i in ans2:      # nepi에 epi들 삭제
            epi.append(ans[i])
            nepi.remove(ans[i])
        
        if len(nepi) == 0:
            break
        
        print("\n\nPI:",end='')
        print(ans)
        print("\nEPI:",end='')
        print(epi)
        print("NEPI:",end='')
        print(nepi)
        
        ang = [ 0 for i in range(0,2**n)]
        for i in ans2:              # epi들이 cover하는 minterm들을 찾아 2로 초기화
            yas = f(ans[i],0)
            for x in yas:
                ang[x] = 1
        
        for i in minterm:       # 2가 아닌(epi가 cover하지 않은) minterm들 remain에 저장
            if ang[i] != 1:
                remain.append(i)

        print("\nremain:",end='')
        print(remain)
        
        remain = column_dominance(nepi, remain) # Column dominance
        second_pi = row_dominance(nepi, remain) # Row dominance
        minterm = remain
        ans = list(second_pi)
        
        print("second_remain:",end='')
        print(remain)
        print("\nsecond_pi:",end='')
        print(second_pi)
    
                
    

main()