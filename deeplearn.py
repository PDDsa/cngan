# coding: utf-8

# In[ ]:


#!/usr/bin/python3
# coding:UTF-8

import sys  
import jieba
import math
import numpy as np
from numpy import mat,matrix,array
import re
from operator import itemgetter, attrgetter
import pickle
import os
import copy 
import tensorflow as tf

def eval_cos(A,B):


               list_a=[]  
               list_b=[]
               x_2=[]
               y_2=[]
               for x in A:
        
                          list_a.append(A[x])
                    #x_2=x_2+A[x]*A[x]
                          x_2.append(A[x]**2)
      
               for y in B:
                    #if y not  in stopword:
                          list_b.append(B[y])
                    #y_2=y_2+B[y]*B[y]
                          y_2.append(B[y]**2)
     

               a=array(list_a)
               b=array(list_b)
               x2=array(x_2)
               y2=array(y_2)

               a_mul_b=a*b
               cos=a_mul_b.sum()/(math.sqrt(x2.sum())*math.sqrt(y2.sum()))
   
               return cos



def run_prediction(i):
  pcount=5000*(i+1)-1
  
  f_tag=i
  f_num=0

  f_num=5000*f_tag
	
  question_show={}

  #print("读取问题")


#print(question)
  print("读取语料")
  filepath="./chat_new2.txt"
  file = open(filepath)
  print("***********现在开始计算*************")
  s_list=[]
  i=0
  sentence2=[]
  para=[]
  paragrapha={}
  all_sentence=[]

  tag=""
  #first_tag=""
  sentence_order=[]
  for line in file:

   #i=i+1

   i=i+1
  # if i>pcount:
     #   break
   if len(line)>1 and i>f_num:
     #line_split=line[56:]
    if "session_id" not in line:
     
     #if i>12821:
     #   break
     line_split=line.split("	")
     #print(line_split[6])
     s=line_split[3]
     session_id=line_split[0]
     user_tag=line_split[2]
     user_id=line_split[1]
     #user_tag=line_split[2]
     #user_tag=int(user_tag)+1
     s_strip=s.strip()
     #s_strip=s_strip.replace("","")
     pattern = re.compile("ORDERID_\d+")
     out = re.sub(pattern, '订单号', s_strip)
     pattern2 = re.compile("\d+")
     out = re.sub(pattern2, '[数字x]', out)
     if i==1:
        tag=line_split[0]
     #tag = line_split[0]

    
     if  tag == line_split[0]:
 
        para.append([user_id,user_tag,out])

     else:
        paragrapha[tag]=para

        para=[]

        para.append([user_id,user_tag,out])


     tag=session_id
   #  print("i=",i)
    # i=i+1
     if i>pcount:
          paragrapha[tag]=para
          para=[]
          break

  file.close()
#转换成id
  id_para={}
  count=0
  dic_list=[]
  dic_gobal=[]
  #print(paragrapha)
  for session in paragrapha:

       count=count+1
       dic={}
     #  print("page count:"+str(count))
     #  print(session)
       id_list=[]
       s_and=""

       for key in paragrapha[session]:
       #      print(key)
             s=key[2]
    #print(s)
             u_id=key[0]
          #   u_tag=key[1]

             
             
          
             #for sen in s:
             s_and=s_and+" "+s


             
       seg_list = jieba.cut(s_and)
       word_list=""
    #print(" ".join(seg_list))
       sentence=" ".join(seg_list)
       word=sentence.split(" ")  


       for w in word:
               if w not in dic:
                      dic[w]=1
               else:
                      dic[w]+=1
    
       del dic['']
    #   print(dic)
       if len(dic)>0:
              dic_list.append(dic)

       for w in dic:
              if w not in dic_gobal:

                    dic_gobal.append(w)

 
 
   

  print("*****************1111111111111*****************") 
#print(dic_list)
  num=0

  idf={}

  idf_list=[]

#dic_gobal.remove('')
#dic_gobal.remove('')
  print("##################################################")
  for w in dic_gobal:
     for d in dic_list:
          #print(d)
          if w not in d:
              if w not in idf:
                   idf[w]=0
          if w in d:
              if w not in idf:
                  idf[w]=1
              else:
                  idf[w]+=1
  

  print("**********************************")       
#print(idf)
  #input()
  print("读取停用词")
  filepath="./stopwords9.txt"
  file2 = open(filepath)

  stopword=[]
  for line in file2:
         stopword.append(line.strip())

  file2.close()

 # for word in stopword:
#     if word in idf:
     #    del idf[word]



  print("################计算tf-idf######################3")

  chat_group=[]

#count=0
  

#f = open("chat_tfdf2.txt", 'w')
  list_dic_tf_idf={}

  list_weight={}
  for session in paragrapha:

       #count=count+1
       dic={}
       #print("page count:"+str(count))
       id_list=[]
       s_and=""

       dic_tf_idf={}

       for w in dic_gobal:
            dic_tf_idf[w]=0   #初始化每段对话词典 词的tdidf 值为0

       list_sent_tfidf=[]

       list_sent_tfidf2=[]
       for key in paragrapha[session]:
        #     print("***********chat group*****************")
       #      print(key)
             s=key[2]
    #print(s)
             u_id=key[0]
          #   u_tag=key[1]

             
             
          
             #for sen in s:
             s_and=s_and+" "+s


    #   print(s_and)
   
       seg_list = jieba.cut(s_and)
       word_list=""
    #print(" ".join(seg_list))
       sentence=" ".join(seg_list)
       word=sentence.split(" ")  


       for w in word:
               if w not in dic:
                      dic[w]=1
               else:
                      dic[w]+=1
                    #过滤停用词
       for word in stopword:
              if word in dic:
                    dic[word]=1
       del dic['']
       #print(dic)
       if len(dic)>0:
             d=dic
        #     print("*********************输出 d ***********************")
         #    print(d)


             total=0
             for v in d.values():
                 total=total+v
        #     print(total)

             tfidf_list=[]

      #print(d)
             weight_l=[]
             max_weight=0
             st_list=[]
             num=0
             
             list_sent_tfidf=[]
             list_sent_tfidf2=[]

             for key in paragrapha[session]:

               #     print("***********chat group*****************")
              #      print(key)
                    st=key[2]
                 #   print(st)

                    u_id=key[0]
                    u_tag=key[1]
         
             #       print("st=",st)
                    seg=jieba.cut(st)
                    sentence=" ".join(seg)

                    word=sentence.split(" ") 

           #del word['']
           #print("word:",word)
                    blank=''
                    while '' in word:
                           word.remove('')
           #print(word)
                    tfidf_list=[]
           #print(d)

                    for w in dic_gobal:
                           dic_tf_idf[w]=0   #初始化每段对话词典 词的tdidf 值为0                 

                    for key in word:
                        if key in idf:   #如果查询的词在 idf 词典里


                           tf=d[key]/total

                           tfidf=tf*math.log(count/idf[key])
                         #  tfidf=tf*(math.log((count+1)/(idf[key]+1)) +1)
                           tfidf_list.append(tfidf)
                           
                           #if u_tag!="1":

                           dic_tf_idf[key]=tfidf    #只比较用户提问的相似度

                    weight=0
                    for t in tfidf_list:
                           weight=weight+t
                  #  print("weight=",weight)
              #      print(dic_tf_idf)
                    dic_tf_idf_copy=dic_tf_idf.copy()
                   # dic_tf_idf_copy=copy.deepcopy(dic_tf_idf) #dic_tf_idf.deepcopy()

                   # del dic_tf_idf
                   # if u_tag=="0":
                    list_sent_tfidf.append([dic_tf_idf_copy,u_tag])
                    #else:
                       #   list_sent_tfidf2.append(dic_tf_idf_copy)              



             list_weight[session]=weight_l
        #     print(dic_tf_idf)
             list_dic_tf_idf[session]=list_sent_tfidf

                   # f.writelines(session+"	"+u_id+"	"+u_tag+"	"+st+"	"+str(weight)+"	"+"\n")
#f.close()
#print(paragrapha)
 # print(list_dic_tf_idf)
#计算两两相似度
 
                

  simliary={}

  c=0
  total_sess=[]


  print("计算單句的關注點和整斷對話的關注點")
# 构建 question 的 tfidf
 
  question_for_train={}
  answer_for_train=[]
  for session in list_dic_tf_idf:
     print("#######################################################"*2)

    
     question={}
     answer=[]
     num=0
     paragrapha_tfidf=[]

     for sent_tfidf in list_dic_tf_idf[session]:

          s=(paragrapha[session])[num]
       
         # print(sent_tfidf)
          print(s[2])
          line=s[2]
          seg_list = jieba.cut(line)

          sentence_tfidf=[]
          line=[]
          for word in seg_list:
            if word!=' ':
              # print(word)
               #print((sent_tfidf[0])[word])
               sentence_tfidf.append((sent_tfidf[0])[word])
               
               paragrapha_tfidf.append((sent_tfidf[0])[word])
               if num <5:                          #5句 q
                   question[num]=sentence_tfidf
          if num==5:                               #1句 a
               answer=sentence_tfidf

          num=num+1

     question_for_train[num]=question.copy()

    # print(paragrapha_tfidf)
     print("question       "+"#"*50)
     print(question)
     print("answer       "+"#"*50)
     print(answer)
     return  (answer,question_for_train,paragrapha_tfidf)

# 计算每一段洛的权，和查询的权。

if __name__ == '__main__':
   with tf.Session() as sess:

      filepath="./chat_new2.txt"
      file = open(filepath)

      ii=0


      for line in file:
             ii=ii+1
      print(ii)
      ii=250
      page=math.ceil(ii/5)
      print("page:",page)
      #input()
      for j in range(int(page)):
              (answer,question,paragrapha_tfidf)=run_prediction(j)
              #print(j)

              #print(sess.run(tf.nn.softmax(answer)))
              #print(question)
              question_weight=[]
              for key in question:
                  question_weight=[]
                  for i in  range(5):

                        #print((question[key])[i])
                        sentence_weight=0
                        for value in (question[key])[i]:
                                  
                                sentence_weight+=value

                        print(sentence_weight)
                        question_weight.append(sentence_weight)
              attention=sess.run(tf.nn.softmax(question_weight))
              print(sess.run(tf.nn.softmax(question_weight)))
             # print(paragrapha_tfidf)
             # print(answer)
              answer_weight=0
              for weight in answer:
                    answer_weight+=weight

              print("answer_weight:",answer_weight)
              array_attention=array(attention)
              array_question_weight=array(question_weight)
              target=array_attention*array_question_weight
              predict=0
              for value in target:
                     predict+=value
              print("predict:",predict)
             # print(sess.run(tf.nn.softmax(paragrapha_tfidf)))
      print("end")  
