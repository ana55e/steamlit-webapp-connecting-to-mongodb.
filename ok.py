import streamlit as st
import plotly.graph_objects as go
import calendar
from datetime import datetime
from streamlit_option_menu import option_menu
# settings:
import database as db
incomes=['Salary','Blog','Other Income']
expenses=['Rent','Utilities','Bills','Miscellaneous']
currency='MAD'
page_title='Income and expense tracker'
page_icon=":moneybag:" # emoji code from https://emojipedia.org/
layout='wide' # 'centered' or 'wide'

# setting page layout

st.set_page_config(page_title=page_title,page_icon=page_icon,layout=layout)

st.title(page_title+' '+page_icon)

#Drop down period selector

years=[datetime.today().year-1,datetime.today().year,datetime.today().year+1]
months=[calendar.month_name[i] for i in range(1,13)]


# database interface
def get_all_periods():
    return db.fetch_all_periods()

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# navigation menu
selected=option_menu(menu_title='choose your player...ahemmm..i mean option',options=['data entry','plotting'],
                     icons=["pencil-square",'bar-chart-steps'],
                     orientation='horizontal') # the icons are from https://icons.getbootstrap.com/ just copy the name of the icon



# inputs and save periods
if selected=='data entry':
    st.header(f'data entry is in {currency}')
    with st.form(key='entry_form',clear_on_submit=True):
        col1,col2=st.columns(2)
        col1.selectbox("Select month",months,key='month')
        col2.selectbox("Select year",years,key='year')


        "---"

        with st.expander('Incomes'):
            for income in incomes:
                st.number_input(income,min_value=0.0,max_value=100000.0,format='%f',step=10.0,key=income)

        with st.expander('Expenses'):
            for expense in expenses:
                st.number_input(expense,min_value=0.0,max_value=100000.0,format='%f',step=10.0,key=expense)


        with st.expander('Comments'):
            comment=st.text_area('use this field to comment',placeholder='Comments',key='comments')

        "---"

        submitted=st.form_submit_button('Save data')
        if submitted:
            period= str(st.session_state["year"])+'-'+str(st.session_state["month"])
            incomes={income:st.session_state[income] for income in incomes} # dictionary of incomes, key is income name, value is amount, e.g. {'Salary': 1000, 'Blog': 200}
            expenses={expense:st.session_state[expense] for expense in expenses}
            db.insert_period(period,incomes,expenses,comment)
            st.success(f'data saved successfully')
    


#  plot peiods
if selected=='plotting':     
    st.header('Plotting data')
    with st.form(key='plot_form',clear_on_submit=True):
        #Todo: get periods from database
        period=st.selectbox('Select period:', get_all_periods())
        submitted=st.form_submit_button('Plot data')
        if submitted:
            #todo get data from database
            period_data=db.get_period(period)
            comment=period_data.get('comments','')
            incomes=period_data.get('incomes',{})
            expenses=period_data.get('expenses',{}) # {} is the default value if the key is not found

            # create metrics
            total_income=sum(incomes.values())
            total_expense=sum(expenses.values())
            savings=total_income-total_expense
            #savings_percentage=round(savings/total_income*100,2)
            col1,col2,col3=st.columns(3)
            col1.metric('Total income',f'{total_income} {currency}')
            col2.metric('Total expense',f'{total_expense} {currency}')
            col3.metric('Savings',f'{savings} {currency}')
            st.text(f"comment: {comment}")


            label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]
            value = list(incomes.values()) + list(expenses.values())

                # Data to dict, dict to sankey
            link = dict(source=source, target=target, value=value)
            node = dict(label=label, pad=20, thickness=30, color="#E694FF")
            data = go.Sankey(link=link, node=node)

                # Plot it!
            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
            st.plotly_chart(fig, use_container_width=True)
