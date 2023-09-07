import pandas as pd

########################
# 第一列為基本能力值
# 第二列為階級上升量
# 第三列為到17級強化量
# 第四列為17-20級強化量
########################

# 使用集合（Set）來檢查是否有重複的數值
def has_duplicates(list):
    seen = set()
    for item in list:
        if item in seen:
            return True
        seen.add(item)
    return False

# 使用集合（Set）來檢查是否有重複的指定數值
def has_duplicate_value(lst, value):
    seen = set()
    for item in lst:
        if item == value and item in seen:
            return True
        seen.add(item)
    return False

df = pd.read_csv('numeric.txt', sep=" ", header=None, names=['接觸/控球', '力量/球威', '選球/體力', '速度/直球', '守備/變化'])

df.iloc[2,:] = df.iloc[2,:] + df.iloc[3,:]
df = df.drop(3)
df.reset_index(drop=True, inplace=True) # 重製索引以填補被刪除的行

df.iloc[0,:] = df.iloc[0,:] + df.iloc[1,:]
df = df.drop(1)
df.reset_index(drop=True, inplace=True) # 重製索引以填補被刪除的行

# HasDuplicates = df.iloc[1].duplicated().any() # 判斷一橫列中有無重複的數字

Reinforcement_Max = df.iloc[1].max() # 判斷一橫列中最大值
has_duplicates_as_max = has_duplicate_value(df.iloc[1],Reinforcement_Max)

values = df.iloc[1].tolist()

while Reinforcement_Max in values:
    values.remove(Reinforcement_Max)
Reinforcement_second_largest = max(values)  # 取第二大值
has_duplicates_as_second = has_duplicate_value(df.iloc[1],Reinforcement_second_largest)

while Reinforcement_second_largest in values:
    values.remove(Reinforcement_second_largest)
Reinforcement_third_largest = max(values)  # 取第三大值

num = 0
for i in range(5):
    if df.iloc[1,i] == Reinforcement_Max:
        num += 1


if not has_duplicates_as_max and not has_duplicates_as_second: #大中小
    print("block1\n")
    train = [0,0,0,0,0]
    count1 = 0
    count2 = 0
    count3 = 0
    for i in range(5):
        if df.iloc[1,i] == Reinforcement_Max and count1 != 1:
            train[i] = 12
            count1 += 1
        elif df.iloc[1,i] == Reinforcement_second_largest and count2 != 1:
            train[i] = 10
            count2 += 1
        elif df.iloc[1,i] == Reinforcement_third_largest and count3 != 1:
            train[i] = 4
            count3 += 1 
        else:
            train[i] = 0   
        if count1 == 1 and count2 == 1 and count3 == 1:
            break
    df.loc[len(df)] = train # 将列表插入 DataFrame 作为新行

elif has_duplicates_as_max and not has_duplicates_as_second: #兩大一小 OR 三個一樣
    print("block2\n")
    train = [0,0,0,0,0]
    choose = [False,False,False,False,False]
    basic_up = []

    if num == 2:
        for i in range(5):
            if df.iloc[1,i] == Reinforcement_second_largest:
                train[i] = 4
            if df.iloc[1,i] == Reinforcement_Max:
                choose[i] = True
        for i in range(5):
            if choose[i] == True:
                basic_up.append(df.iloc[0,i])
            
        basic_up_max =  max(basic_up)
        has_duplicates_basic_up_max = has_duplicates(basic_up)

        if has_duplicates_basic_up_max: # 階級上升量+基本能力值一樣->由左而右
            for i in range(5):
                if df.iloc[0,i] == basic_up_max and choose[i] == True:
                    train[i] = 12
                    for j in range(i+1,5):
                        if df.iloc[0,j] == basic_up_max and choose[i] == True:
                            train[j] = 10
                            break
                    break
        else:
            values = basic_up
            values.remove(basic_up_max)
            basic_up_second_largest = max(values)  # 取第二大值

            for i in range(5):
                if df.iloc[0,i] == basic_up_max and choose[i] == True:
                    train[i] = 12
                if df.iloc[0,i] == basic_up_second_largest and choose[i] == True:
                    train[i] = 10
    else: # num == 3
        print("block4\n")
        for i in range(5):
            if df.iloc[1,i] == Reinforcement_Max:
                choose[i] = True
        for i in range(5):
            if choose[i] == True:
                basic_up.append(df.iloc[0,i])

        basic_up_max =  max(basic_up)
        has_duplicates_basic_up = has_duplicates(basic_up)    
        num = 0
        for i in basic_up:
            if i == basic_up_max:
                num += 1

        if has_duplicates_basic_up and num == 3: # 階級上升量+基本能力值都一樣->由左而右
            for i in range(5):
                if df.iloc[0,i] == basic_up_max and choose[i] == True:
                    train[i] = 12
                    for j in range(i+1,5):
                        if df.iloc[0,j] == basic_up_max and choose[j] == True:
                            train[j] = 10
                            for k in range(j+1,5):
                                if df.iloc[0,k] == basic_up_max and choose[k] == True:
                                    train[k] = 4
                                    break
                            break
                    break
        elif has_duplicates_basic_up and num == 2: # 階級上升量+基本能力值兩大一小
            values = basic_up
            while basic_up_max in values:
                values.remove(basic_up_max)
            basic_up_second_largest = max(values)
            for i in range(5):
                if df.iloc[0,i] == basic_up_max and choose[i] == True:
                    train[i] = 12
                    for j in range(i+1,5):
                        if df.iloc[0,j] == basic_up_max and choose[j] == True:
                            train[j] = 10
                            break
                    break
            for i in range(5):
                if df.iloc[0,i] == basic_up_second_largest and choose[i] == True:
                    train[i] = 4
        elif has_duplicates_basic_up and num == 1:# 階級上升量+基本能力值一大兩小
            values = basic_up
            while basic_up_max in values:
                values.remove(basic_up_max)
            basic_up_second_largest = max(values)
            for i in range(5):
                    if df.iloc[0,i] == basic_up_max and choose[i] == True:
                        train[i] = 12
            for i in range(5):
                if df.iloc[0,i] == basic_up_second_largest and choose[i] == True:
                    train[i] = 10
                    for j in range(i+1,5):
                        if df.iloc[0,j] == basic_up_second_largest and choose[j] == True:
                            train[j] = 4
                            break
                    break             
        else: # 階級上升量+基本能力值大中小
            values = basic_up
            while basic_up_max in values:
                values.remove(basic_up_max)
            basic_up_second_largest = max(values)
            while basic_up_second_largest in values:
                values.remove(basic_up_second_largest)
            basic_up_third_largest = max(values)

            for i in range(5):
                if df.iloc[0,i] == basic_up_max and choose[i] == True:
                    train[i] = 12
            for i in range(5):
                if df.iloc[0,i] == basic_up_second_largest and choose[i] == True:
                    train[i] = 10
            for i in range(5):
                if df.iloc[0,i] == basic_up_third_largest and choose[i] == True:
                    train[i] = 4
    df.loc[len(df)] = train # 將列表插入 DataFrame 作為新行

elif not has_duplicates_as_max and has_duplicates_as_second: # 一大兩小
    print("block3\n")
    train = [0,0,0,0,0]
    choose = [False,False,False,False,False]
    basic_up = []

    for i in range(5):
        if df.iloc[1,i] == Reinforcement_Max:
            train[i] = 12
        if df.iloc[1,i] == Reinforcement_second_largest:
            choose[i] = True
    for i in range(5):
        if choose[i] == True:
            basic_up.append(df.iloc[0,i])
    
    basic_up_max =  max(basic_up)
    has_duplicates_basic_up_max = has_duplicates(basic_up)

    if has_duplicates_basic_up_max: # 階級上升量+基本能力值一樣->由左而右
        for i in range(5):
            if df.iloc[0,i] == basic_up_max and choose[i] == True:
                train[i] = 10
                for j in range(i+1,5):
                    if df.iloc[0,j] == basic_up_max and choose[i] == True:
                        train[j] = 4
                        break
                break
    else:
        values = basic_up
        values.remove(basic_up_max)
        basic_up_second_largest = max(values)# 取第二大值

        for i in range(5):
            if df.iloc[0,i] == basic_up_max and choose[i] == True:
                train[i] = 10
            if df.iloc[0,i] == basic_up_second_largest and choose[i] == True:
                train[i] = 4
    
    df.loc[len(df)] = train # 將列表插入 DataFrame 作為新行

column_sum = df.sum()
print(column_sum)
print(train)