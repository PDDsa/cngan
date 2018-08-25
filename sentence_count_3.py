import os

import re

def  run_prediction():
  print("读取语料")
  filepath="./chat_new2.txt"
  file1 = open(filepath)
  pagecount=0
  for line in file1:

      #if len(line)>1 :
       pagecount=pagecount+1

  file1.close()

  file2 = open(filepath)

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
  for line in file2:

   i=i+1
   if len(line)>1 :
    

     #line_split=line[56:]
   # if "session_id" not in line:
     
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
     out=out.replace("&nbsp;","")
     out=out.replace("&quot","")

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
     if i==pagecount:
          paragrapha[tag]=para
          para=[]
          break

  file2.close()

  sentence_dic={}

  for session in paragrapha:
         print(session)
         num=0
         for key in paragrapha[session]:
              u_tag=key[1]
              if (key[2],u_tag) not in sentence_dic:
                    
                    num_sessionid_list=[[session,num,u_tag]]

                    sentence_dic[(key[2],u_tag)]=[1,num_sessionid_list]
              else:
                    s_count=sentence_dic[(key[2],u_tag)][0]+1

                    num_sessionid_list=sentence_dic[(key[2],u_tag)][1]

                    num_sessionid_list.append([session,num,u_tag])

                    sentence_dic[(key[2],u_tag)]=[s_count,num_sessionid_list]
              num=num+1


  filename="./sentence_count_user_type_0.txt"
  f = open(filename, 'w')

  filename1="./sentence_count_user_type_1.txt"
  f2 = open(filename1, 'w')

  f_tag=0
  r_count=0
  r_count2=0
  for sentence in sentence_dic:
      u_tag=sentence[1]
      if u_tag=="0":

         f.writelines("result_u_"+str(f_tag)+"_"+str(r_count)+"  "+str(u_tag)+"  "+"*************************************************"+"\n")
      #else:


         print(sentence_dic[sentence])

         for txt in sentence_dic[sentence][1]:

            print(txt)


            f.writelines(txt[0]+"        "+str(txt[1])+"        "+txt[2]+"        "+sentence[0]+"\n")

         r_count=r_count+1

      else:

         f2.writelines("result_s_"+str(f_tag)+"_"+str(r_count2)+"  "+str(u_tag)+"  "+"************************************************"+"\n")
      #else:


         print(sentence_dic[sentence])

         for txt in sentence_dic[sentence][1]:

            print(txt)


            f2.writelines(txt[0]+"        "+str(txt[1])+"        "+txt[2]+"        "+sentence[0]+"\n")

         r_count2=r_count2+1

  print("用户提问分类个数：",r_count)
  print("客服回答分类个数：",r_count2)

  f.close()
  f2.close()

if __name__ == '__main__':

        run_prediction()
        print("end")
    
