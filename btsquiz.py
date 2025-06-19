import streamlit as st
st.title('hey!')
st.write("welcome! let's play")




que1 = st.radio(   'who is the leader of BTS?',('JK','V','RM', 'Jin')
)
if que1 == 'RM':
    st.success('correct!😊👍 you are an ARMY')

else:
    st.error('not correct, solali are fake army😒')    



    
    
que2 = st.radio('who is the maknae of BTS?',('JK','V','RM', 'Jin')
)
if que2 == 'JK':
    st.success('correct!,You are an ARMY')

else:
    st.error('not correct, you are fake army😒')    



   
que3 = st.radio('who is the sunshine of BTS?',('JK','V','JHope', 'Jin')
)
if que3 == 'JHope':
    st.success('correct!,You are an ARMY')

else:
    st.error('not correct, you are fake army😒')   





que4 = st.radio('who is the most handsome man?',('JK','V','JHope', 'BTS')
)
if que4 == 'BTS':
    st.success('correct!,You are an ARMY')

else:
    st.error('not correct, you are fake army😒')    




que5 = st.radio('who is from daegu?',('JK','V','JHope', 'RM')
)
if que5 == 'V':
    st.success('correct!,You are an ARMY')

else:
    st.error('not correct, you are fake army😒')   




que6 = st.radio('who are from busan?',('JK and jhope','JK and Jimin','JHope and V', 'RM and JIN')
)
if que6 == 'JK and Jimin':
    st.success('correct!,You are an ARMY')

else:
    st.error('not correct, you are fake army😒')   





st.subheader('* No. of in BTS group')
que7 = st.selectbox(
    'choose what no. of BTS you think are in BTS:',
    ['7','8','9','4']
)
if que7 == '7':
    st.success('correct!,You are an ARMY')

else:
    st.error('not correct, you are fake army😒')   


    

st.subheader('Pick all the BTS quallities you admire')
qua = st.multiselect(
    'you can choose more than one dont worry',
    ['Vocals', 'Rapping', 'Stage Presence', 'Dance', 'Smoking', 'Drinking', 'Studying','Desttruction Skills']
)
st.write('you admire:', qua)


st.subheader('On a scale of 1 to 100, How much do you love BTS?')
love = st.slider('your BTS love meter:', 1, 50, 100)
st.write('you love BTS ONLY:', love, 'why not infinity')


v = st.select_slider(
    'how much do you care that they are in relationship?',
    options = ['Not much','A Little','moderately', 'a lot' ]
)
st.write('you care about their relations:', v)

