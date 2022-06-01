# Project Ekler

#You don't need to run this code. It is the data we used. There are bunch of verbs.
import requests
file = requests.get("https://raw.githubusercontent.com/Loodos/zemberek-python/master/zemberek/resources/lexicon.csv")


lemma_list = sorted({line.split("\t")[2] for line in file.text.split("\n")[:-1] 
                     if line.split("\t")[2].isalpha() and 
                        (line.split("\t")[0].endswith("Verb"))
                        and len(line.split("\t")[2]) > 2
                        })

#No need to run also.
#Our good HFST has 8 lexicons, according to the last vowel of the verb and to the last character, if it is a consonant.
#Lexicon 1 -> last vowel: "a" or "ı", last consonant: voiced
#Lexicon 2 -> last vowel: "a" or "ı", last consonant: voiceless 
#(The correct numbering of lexicons is not like this. For example, Lexicon V1 is "ü, ö" and voiced. But to get the idea... Numbering of these lexicons was arbitrary. No one knows what Arif was thinking, even himself.)
Verbs=lemma_list
consonants_v=["b","c","d","g","ğ","j","l","m","n","r","v","y","z"]
consonant_vs=["ç","f","h","k","p","s","ş","t"]
vowel1=["ö","ü"]
vowel2=["a","ı"]
vowel3=["u","o"]
vowel4=["e","i"]
vowel5= ["ö","ü","a","ı","e","u","o","i"]
#Code below deletes the final character if it is a vowel. Because we handled "ünlü daralması" with deleting the character if it is a vowel and intorducing "-(v)yor" with (v) = the correct vowel.
for verb in Verbs:
  if verb[-1] in vowel5:
    verb=verb[:-1]
    Verbs.append(verb)
with open("lemma_list_for_good_hfst.lexc","w") as f: #opens a file
  f.write("Verbs\n")
  for verb in Verbs:
    if verb[-1] in vowel1:  #if last character is ö or ü
        f.write("\t"+verb+"\tV1;\n") #goes to Lexicon V1
    if verb[-1] in vowel2:
        f.write("\t"+verb+"\tV2;\n") #if a, ı goes to Lexicon V2 and goes on...
    if verb[-1] in vowel3:
        f.write("\t"+verb+"\tV3;\n")
    if verb[-1] in vowel4:
        f.write("\t"+verb+"\tV6;\n")
    elif verb[-1] in consonants_v: #if last character is a consonant and voiced
      if verb[-2] in consonants_v: #if second from the last is a consonant and voiced too,
        if verb[-3] in vowel1:  #looks at the third from the last to find a vowel. Rest is the same, assigns to the correct lexicon
          f.write("\t"+verb+"\tV1;\n")
        if verb[-3] in vowel2:
          f.write("\t"+verb+"\tV2;\n")
        if verb[-3] in vowel3:
          f.write("\t"+verb+"\tV3;\n")
        if verb[-3] in vowel4:
          f.write("\t"+verb+"\tV6;\n")

      if verb[-2] in consonant_vs: #if second from the last is a consonant and voiceless
        if verb[-3] in vowel1: #looks at the third, and same.
          f.write("\t"+verb+"\tV1;\n")
        if verb[-3] in vowel2:
          f.write("\t"+verb+"\tV2;\n")
        if verb[-3] in vowel3:
          f.write("\t"+verb+"\tV3;\n")
        if verb[-3] in vowel3:
          f.write("\t"+verb+"\tV3;\n")
        if verb[-3] in vowel4:
          f.write("\t"+verb+"\tV6;\n")

      if verb[-2] in vowel1: #if last vowel is consonant looks at the second from last to find a vowel.
        f.write("\t"+verb+"\tV1;\n")
      if verb[-2] in vowel2:
        f.write("\t"+verb+"\tV2;\n")
      if verb[-2] in vowel3:
        f.write("\t"+verb+"\tV3;\n")
      if verb[-2] in vowel4:
        f.write("\t"+verb+"\tV6;\n")
    elif verb[-1] in consonant_vs: #if last vowel is a consonant and voiceless.
      if verb[-2] in vowel1: #assigns verbs to the voiceless lexicons.
        f.write("\t"+verb+"\tV4;\n")
      if verb[-2] in vowel2:
        f.write("\t"+verb+"\tV5;\n")
      if verb[-2] in vowel3:
        f.write("\t"+verb+"\tV8;\n")
      if verb[-2] in vowel4:
        f.write("\t"+verb+"\tV7;\n")

#No need to run this code.
#This code below is exactly the same but it is for bad HFST, so it only assigns to one lexicon which is "Lexicon V"
Verbs=lemma_list
consonants_v=["b","c","d","g","ğ","j","l","m","n","r","v","y","z"]
consonant_vs=["ç","f","h","k","p","s","ş","t"]
vowel1=["ö","ü"]
vowel2=["a","ı"]
vowel3=["u","o"]
vowel4=["e","i"]
vowel5= ["ö","ü","a","ı","e","u","o","i"]
for verb in Verbs:
  if verb[-1] in vowel5:
    verb=verb[:-1]
    Verbs.append(verb)
with open("lemma_list_for_bad_hfst.lexc","w") as f:
  f.write("Verbs\n")
  for verb in Verbs:
    f.write("\t"+verb+"\tV;\n")

#No need to run this as well.
#This is a short code that we used to generate bad suffix forms like "-aceksinuz" for bad HFST.
vowels= ["ö","ü","a","ı","e","u","o","i"]

for v in vowels:
  for v1 in vowels:
    print(f"\t+Past_3pl:t{v}l{v1}r\tV;")

#Introducing HFST
#Run this
!pip install hfst-dev
import hfst_dev
from hfst_dev import compile_lexc_script, compile_lexc_file

#Run this after uploading "bad_hfst.lexc" and "good_hfst.lexc"
from hfst_dev import HfstTransducer
generatorTR=compile_lexc_file("bad_hfst.lexc")  #Because the HFST we wrote has more than 12k lines, we introduce the HFST as a file.
GeneratorTR_iyi =compile_lexc_file("good_hfst.lexc")

analyzer = HfstTransducer(generatorTR)  #Introducing HFST analyzer, we take the output thanks to this code.
analyzer.invert()
analyzer.minimize()



analyzer1 = HfstTransducer(GeneratorTR_iyi) #Good HFST analyzer.

#This is the magic. Run this and write your word.
input = input("Kelimenizi girin: ") #Input
gorgor = analyzer.lookup(input)   #Takes the input at puts it into the bad HFST as an input

out=gorgor[0][0]    #HFST gives the output as an array. Something like this -> ((gelirler, 00)). We get rid of parentheses and take only the actual output

ek_list=out.split('+')[0:] #The suffixes are seperated with "+" we also get rid of these because "+" makes it harder to sort the suffixes in the following code.

vowels = ["ö","ü","a","ı","e","u","o","i"] #Introducing vowels

#The code below gets everything in the correct order. In case there is a suffix wrongly placed, this code places it in the correct position.
order_list={"Neg":1,"Neg1":1,"Aorist_c":2,"Aorist_v":2,"Aorist_Neg":2,"Aorist_c_1sg":2,"Aorist_c_2sg":2,"Aorist_c_1pl":2,"Aorist_c_2pl":2,"Aorist_c_3pl":2,
            "Aorist_v_1sg":2,"Aorist_v_2sg":2,"Aorist_v_1pl":2,"Aorist_v_2pl":2,"Aorist_v_3pl":2,
            "Aorist_Neg1sg":2,"Aorist_Neg2sg":2,"Aorist_Neg3sg":2,"Aorist_Neg1pl":2,"Aorist_Neg2pl":2,"Aorist_Neg3pl":2,
            "Prog":2,
            "Prog_1sg":2,"Prog_2sg":2,"Prog_1pl":2,"Prog_2pl":2,"Prog_3pl":2,
            "Future_c":3,"Future_v":3,
            "Future_c_1sg":3,"Future_c_2sg":3,"Future_c_1pl":3,"Future_c_2pl":3,"Future_c_3pl":3,
            "Future_v_1sg":3,"Future_v_2sg":3,"Future_v_1pl":3,"Future_v_2pl":3,"Future_v_3pl":3,
            "Past_Ev":4,"Past":5,"Past1":5,
            "Past_Ev_1sg":4,"Past_Ev_2sg":4,"Past_Ev_1pl":4,"Past_Ev_2pl":4,"Past_Ev_3pl":4,
            "Past_1sg":5,"Past_2sg":5,"Past_1pl":5,"Past_2pl":5,"Past_3pl":5
            }

if "+Prog" in out:
  if ek_list[0][-1] in vowels:
    ek_list[0] = ek_list[0][:-1]  #We handled "ünlü daralması" by deleting the last vowel, if any, in the word and introducing "+Prog" with the correct vowel.
#So, our HFST does not have a "-yor" suffix only "-iyor", "-ıyor" etc. When +Prog placed wrongly, our HFST does not delete the last vowel of the word. 
#The code above makes sure the last vowel is deleted when "+Prog" is introduced

#Correct ordering of suffixes by using ".sort" function.
new_order=[]
for elt in ek_list[1:]:
  new_order.append((order_list[elt],elt))
new_order.sort()
corrected_string=ek_list[0]
#Introducing "+" again because we deleted it before.
for ek in new_order:
  corrected_string=corrected_string+"+"+ek[1]


gargar = analyzer1.lookup(corrected_string) #Good HFST analyzer.

#The output. If the input matches the final output, it gives a "this is correct" message. If it is not, gives the correct form.
if portakal == gargar[0][0]:
  print("Good Job!")
else:
  print(f"Here is the correct spelling: {gargar[0][0]}")