import hfst_dev
from hfst_dev import compile_lexc_script, compile_lexc_file
from hfst_dev import HfstTransducer
import streamlit as st
from PIL import Image
import pandas as pd


first_generator=compile_lexc_file("lex1.lexc")
second_generator =compile_lexc_file("lex2.lexc")

first_analyzer = HfstTransducer(first_generator)
first_analyzer.invert()
first_analyzer.minimize()
second_analyzer = HfstTransducer(second_generator)


def find_correct_form(input_word):

	try:
		first_result = first_analyzer.lookup(input_word)

		out=first_result[0][0]
		ek_list=out.split('+')[0:]
		vowels = ["ö","ü","a","ı","e","u","o","i"]
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
		    ek_list[0] = ek_list[0][:-1]

		new_order=[]
		for elt in ek_list[1:]:
		  new_order.append((order_list[elt],elt))
		new_order.sort()

		corrected_string=ek_list[0]
		for ek in new_order:
		  corrected_string=corrected_string+"+"+ek[1]


		second_result = second_analyzer.lookup(corrected_string)
	
	except Exception as e:
		final_result="Sorry, we couldn't find your verb :( But we are working on it!)"
		return final_result

	final_result=second_result[0][0]
	if final_result==input_word:
		final_result=final_result+" - Good job :)"
	else:
		final_result="Here's the correct form: "+final_result
	return final_result





image = Image.open('bitter-mood.png')

st.image(image)
st.title('Project Ekler')	

input_word = st.text_input('Enter your verb', 'ekledikmüş')
st.write(find_correct_form(input_word))
df=pd.read_csv("exceptionlist.csv",names=["Lemma","Aorist Form"])
df.sort_values(by=['Lemma'],inplace=True)
st.header("Exceptions")
st.markdown("""\n
Project Ekler doesn’t take into consideration the irregularities of the aorist marker. \n 
**Here are the most common irregular forms:**""")
st.dataframe(df)
st.header("Github")
st.markdown("""\n
	[Project Ekler Repository](https://github.com/eklerproject/ekler)\n
	#### Collaborators ####
	* [Arif Arabacı](https://github.com/arifcarmaker)
	* [Damla Özden](https://github.com/damlaozden)
	* [Doruk Alkan](https://github.com/dorukalkan)
	* [Seray Akkülah](https://github.com/serayakkulah)
""")
