# Import required modules
import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
from sqlalchemy import create_engine

# Connect to db (sqlalchemy)
engine = create_engine("postgresql+psycopg2://postgres:QazmkO10!)@68.183.183.56/ProjectwiseSalesDB")

# Connect to the db (psycopg2)
conn = psycopg2.connect(
    host="68.183.183.56",
    database="ProjectwiseSalesDB",
    user="postgres",
    password="QazmkO10!)")
cur = conn.cursor()

# Read in all the tables
project_df = pd.read_sql("select * from project", con=engine)
subproject_df = pd.read_sql("select * from subproject", con=engine)
brand_df = pd.read_sql("select * from brand", con=engine)
attr_df = pd.read_sql("select * from attribute", con=engine)
subproject_brand_df = pd.read_sql("select * from brand_for_projects_subs", con=engine)

# Create page navigation for insertion and update
pages_option = st.sidebar.selectbox("Go to", ["Insertion", "Update", "Addition"])

# Set title
st.title("Projectwise Sales Dashboard Portal")

# If "Insertion" is selected
if pages_option=="Insertion":
    st.subheader("Welcome to Insertion Page")

    # Dropdown to select date
    date_options = st.date_input("Select a date")

    # Dropdown to select project
    project_options = st.selectbox("Select a project", project_df.name)


    # Dropdown to select subproject by the id of project
    # Show only the subproject under the selected "project"
    selected_project_id = project_df[project_df.name==project_options].id.iloc[0]
    subproject_options = st.selectbox("Select a subproject", subproject_df[subproject_df.project_id==selected_project_id].name)


    # Dropdown to select brand
    # Show only the brand under the selected "project" and "project"
    # Get selected subproject id
    try:
        selected_subproject_id = subproject_df[subproject_df.name==subproject_options].id.iloc[0]
        brand_options = subproject_brand_df[(subproject_brand_df.project_id==selected_project_id) & (subproject_brand_df.subproject_id==selected_subproject_id)].brand_id.unique()
        brand_options = st.selectbox("Select a brand", brand_df[brand_df.id.isin(brand_options)].name.unique())
    except:
        brand_options = subproject_brand_df[subproject_brand_df.project_id==selected_project_id].brand_id.unique()
        brand_options = st.selectbox("Select a brand", brand_df[brand_df.id.isin(brand_options)].name.unique())


    # Dropdown to select attribute
    attribute_options = st.selectbox("Select an attribute", attr_df.name)

    # Insert value from the user
    value_options = st.number_input("Enter a value")


    # Enter note from the user
    note_options = st.text_area("Enter note")

    # Get the id of the selected brand
    selected_brand_id = brand_df[brand_df.name==brand_options].id.iloc[0]

    # If the project is "Reed"
    if selected_project_id==1:

        # Get "project_subs_id" for the project
        project_subs_id = subproject_brand_df[(subproject_brand_df.project_id==1) & (subproject_brand_df.brand_id==selected_brand_id)].id.iloc[0]

        # Create a dataframe
        df = pd.DataFrame({
            "date":date_options,
            "brand_projects_subs_id":project_subs_id,
            "attribute_id":attr_df[attr_df.name==attribute_options].id.iloc[0],
            "value":value_options,
            "note":note_options}, index=[0])

        st.markdown("**Records to insert**")

        # This row will be inserted
        st.write(df)


    # If the project "Web" is selected from dropdown
    if selected_project_id==2:

        # Get "project_subs_id" for the project
        project_subs_id = subproject_brand_df[(subproject_brand_df.project_id==2) & (subproject_brand_df.brand_id==selected_brand_id)].id.iloc[0]

        # Create a dataframe
        df = pd.DataFrame({
            "date":date_options,
            "brand_projects_subs_id":project_subs_id,
            "attribute_id":attr_df[attr_df.name==attribute_options].id.iloc[0],
            "value":value_options,
            "note":note_options}, index=[0])

        st.markdown("**Records to insert**")

        # This row will be inserted
        st.write(df)


    # If the project "Awarding Body is selected from dropdown
    if selected_project_id==6:

        # Get "project_subs_id" for the project
        project_subs_id = subproject_brand_df[(subproject_brand_df.project_id==6) & (subproject_brand_df.brand_id==selected_brand_id)].id.iloc[0]

        # Create a dataframe
        df = pd.DataFrame({
            "date":date_options,
            "brand_projects_subs_id":project_subs_id,
            "attribute_id":attr_df[attr_df.name==attribute_options].id.iloc[0],
            "value":value_options,
            "note":note_options}, index=[0])

        st.markdown("**Records to insert**")

        # This row will be inserted
        st.write(df)


    # If the projects are not "Reed", "Web", or "Ararding Body"
    else:
        try:
            # Get "project_subs_id" for the project
            project_subs_id = subproject_brand_df[(subproject_brand_df.project_id==selected_project_id) & (subproject_brand_df.subproject_id==selected_subproject_id) & (subproject_brand_df.brand_id==selected_brand_id)].id.iloc[0]

            # Create a dataframe
            df = pd.DataFrame({
                "date":date_options,
                "brand_projects_subs_id":project_subs_id,
                "attribute_id":attr_df[attr_df.name==attribute_options].id.iloc[0],
                "value":value_options,
                "note":note_options}, index=[0])

            st.markdown("**Records to insert**")

            # This row will be inserted
            st.write(df)
        except:
            pass

    # Button to insert data once clicked
    with st.form(key='my_form'):
        submit_button = st.form_submit_button(label='Insert')
        if submit_button:
            try:
                # If submit button is clicked, append the data to the central_entry db
                df.to_sql("central_entry", if_exists="append", index=False, con=engine)
                st.success("Values inserted successfully!")
                st.markdown("**Records after insertion**")
                st.write(pd.read_sql("select * from central_entry", con=engine).tail(1).reset_index(drop=True))
            except:
                st.error("Values already inserted!")



# If update page is selected
if pages_option=="Update":
    st.subheader("Welcome to Update Page")

    # Dropdown to update date
    date_options = st.date_input("Select a date")
    
    # Dropdown to update project
    project_options = st.selectbox("Select a project", project_df.name)


    # Dropdown to select subproject by the id of project
    # Show only the subproject under the selected "project"
    selected_project_id = project_df[project_df.name==project_options].id.iloc[0]
    subproject_options = st.selectbox("Select a subproject", subproject_df[subproject_df.project_id==selected_project_id].name)

    # Dropdown to select brand
    # Show only the brand under the selected "project" and "project"
    # Get selected subproject id
    try:
        selected_subproject_id = subproject_df[subproject_df.name==subproject_options].id.iloc[0]
        brand_options = subproject_brand_df[(subproject_brand_df.project_id==selected_project_id) & (subproject_brand_df.subproject_id==selected_subproject_id)].brand_id.unique()
        brand_options = st.selectbox("Select a brand", brand_df[brand_df.id.isin(brand_options)].name.unique())
    except:
        brand_options = subproject_brand_df[subproject_brand_df.project_id==selected_project_id].brand_id.unique()
        brand_options = st.selectbox("Select a brand", brand_df[brand_df.id.isin(brand_options)].name.unique())
    

    # Dropdown to select attribute
    attribute_options = st.selectbox("Select an attribute", attr_df.name)

    # Get attribute id
    selected_att_id = attr_df[attr_df.name==attribute_options].id.iloc[0]


    # Extract the selected brand id
    selected_brand_id = brand_df[brand_df.name==brand_options].id.iloc[0]

    # Filter by project_id, project_subs_id, date, attribute_id and brand_id
    # If the project is "Reed"
    if selected_project_id==1:

        # Get "project_subs_id" for the project
        project_subs_id = subproject_brand_df[(subproject_brand_df.project_id==1) & (subproject_brand_df.brand_id==selected_brand_id)].id.iloc[0]
        update_central_entry = pd.read_sql("select * from central_entry", con=engine)
        filter_df = update_central_entry[(update_central_entry.date==date_options) & (update_central_entry.brand_projects_subs_id==project_subs_id) & (update_central_entry.attribute_id==selected_att_id)]
        st.markdown("**Record before update**")

        # The row to update
        st.write(filter_df)

        # Get the update_id if filter_df exists
        if filter_df.shape[0]!=0:
            update_id = filter_df.id.iloc[0]
            
            # Insert value from the user to update with
            value_options = st.number_input("Enter a value to update with")

            with st.form(key='my_form1'):
                submit_button = st.form_submit_button(label='Update')
                if submit_button:
                    # Update a value
                    cur.execute(f"update central_entry set value={value_options} where id={update_id}")
                    conn.commit()
                    st.success("Updated successfully!")
                    st.markdown("**Record after update**")

                    # Read the updated value
                    after_update_df = pd.read_sql("select * from central_entry", con=engine)
                    st.write(after_update_df[after_update_df.id==update_id])
        else:
            st.error("Record not exists!")
    


    # Filter by project_id, project_subs_id, date, attribute_id and brand_id
    # If the project is "Web"
    if selected_project_id==2:
        project_subs_id = subproject_brand_df[(subproject_brand_df.project_id==2) & (subproject_brand_df.brand_id==selected_brand_id)].id.iloc[0]
        update_central_entry = pd.read_sql("select * from central_entry", con=engine)
        filter_df = update_central_entry[(update_central_entry.date==date_options) & (update_central_entry.brand_projects_subs_id==project_subs_id) & (update_central_entry.attribute_id==selected_att_id)]
        st.markdown("**Record before update**")
        st.write(filter_df)
        if filter_df.shape[0]!=0:
            update_id = filter_df.id.iloc[0]
            
            # Insert value from the user to update with
            value_options = st.number_input("Enter a value to update with")

            with st.form(key='my_form2'):
                submit_button = st.form_submit_button(label='Update')
                if submit_button:
                    # Update a value
                    cur.execute(f"update central_entry set value={value_options} where id={update_id}")
                    conn.commit()
                    st.success("Updated successfully!")
                    st.markdown("**Record after update**")
                    after_update_df = pd.read_sql("select * from central_entry", con=engine)
                    st.write(after_update_df[after_update_df.id==update_id])
        else:
            st.error("Record not exists!")

    
    # Filter by project_id, project_subs_id, date, attribute_id and brand_id
    # If the project is "Awarding Body"
    if selected_project_id==6:
        project_subs_id = subproject_brand_df[(subproject_brand_df.project_id==6) & (subproject_brand_df.brand_id==selected_brand_id)].id.iloc[0]
        update_central_entry = pd.read_sql("select * from central_entry", con=engine)
        filter_df = update_central_entry[(update_central_entry.date==date_options) & (update_central_entry.brand_projects_subs_id==project_subs_id) & (update_central_entry.attribute_id==selected_att_id)]
        st.markdown("**Record before update**")
        st.write(filter_df)
        if filter_df.shape[0]!=0:
            update_id = filter_df.id.iloc[0]
            
            # Insert value from the user to update with
            value_options = st.number_input("Enter a value to update with")

            with st.form(key='my_form3'):
                submit_button = st.form_submit_button(label='Update')
                if submit_button:
                    # Update a value
                    cur.execute(f"update central_entry set value={value_options} where id={update_id}")
                    conn.commit()
                    st.success("Updated successfully!")
                    st.markdown("**Record after update**")
                    after_update_df = pd.read_sql("select * from central_entry", con=engine)
                    st.write(after_update_df[after_update_df.id==update_id])
        else:
            st.error("Record not exists!")

    # If the project is not "Reed", "Web", and "Awarding Body"
    if selected_project_id!=1 and selected_project_id!=2 and selected_project_id!=6:
        project_subs_id = subproject_brand_df[(subproject_brand_df.project_id==selected_project_id) & (subproject_brand_df.brand_id==selected_brand_id)].id.iloc[0]
        update_central_entry = pd.read_sql("select * from central_entry", con=engine)
        filter_df = update_central_entry[(update_central_entry.date==date_options) & (update_central_entry.brand_projects_subs_id==project_subs_id) & (update_central_entry.attribute_id==selected_att_id)]
        st.markdown("**Record before update**")
        st.write(filter_df)
        if filter_df.shape[0]!=0:
            update_id = filter_df.id.iloc[0]
            
            # Insert value from the user to update with
            value_options = st.number_input("Enter a value to update with")

            with st.form(key='my_form4'):
                submit_button = st.form_submit_button(label='Update')
                if submit_button:
                    # Update a value
                    cur.execute(f"update central_entry set value={value_options} where id={update_id}")
                    conn.commit()
                    st.success("Updated successfully!")
                    st.markdown("**Record after update**")
                    after_update_df = pd.read_sql("select * from central_entry", con=engine)
                    st.write(after_update_df[after_update_df.id==update_id])
        else:
            st.error("Record not exists!")


# If "Addition" page is selected
if pages_option=="Addition":
    st.subheader("Welcome to Addition Page")
    
    # Add project
    with st.form(key="my_form5"):
        st.markdown("**Project Addition**")

        # Take project name as user input
        add_project = st.text_input("Enter a project").title()

        submit_button = st.form_submit_button(label='Add Project')
        if submit_button:
            # Check if the project already exists
            project_exists = project_df[project_df.name.str.contains(add_project, case=False)]
            if project_exists.shape[0]<1:
                cur.execute(f"INSERT INTO project(name) VALUES('{add_project}')")
                conn.commit()
                st.success(f"Project '{add_project}' added successfully!")
            else:
                st.error(f"Project '{add_project}' already exists!")
    

    # Add subproject
    with st.form(key="my_form6"):
        st.markdown("**Subproject Addition**")

        # Take subproject name as user input
        add_subproject = st.text_input("Enter a subproject").title()

        # The project the subproject lies under
        add_project = st.text_input("Enter project").title()

        # Check if the project exists
        project_exists = project_df[project_df.name.str.contains(add_project, case=False)]

        # Check if the subproject exists
        subproject_exists = subproject_df[subproject_df.name.str.contains(add_subproject, case=False)]

        submit_button = st.form_submit_button(label='Add Subproject')
        if submit_button:
            # If the project esists, get the id
            if project_exists.shape[0]>0:
                added_project_id = project_exists.id.iloc[0]

            # If the project doesn't exist, insert it into 'project' table. Also get its id after insertion
            else:
                cur.execute(f"INSERT INTO project(name) VALUES('{add_project}')")
                conn.commit()
                project_df = pd.read_sql("select * from project", con=engine)
                added_project_id = project_df[project_df.name.str.contains(add_project, case=False)].id.iloc[0]
            

            # Check if the subprojects exists. If doesn't exist, insert it into the subproject table
            if subproject_exists.shape[0]==0:
                cur.execute('INSERT INTO subproject(name, project_id) VALUES(%s, %s)', (add_subproject, added_project_id))
                conn.commit()
                st.success(f"Subproject '{add_subproject}' under project '{add_project}' added successfully!")
            else:
                st.error(f"Subproject '{add_subproject}' already exists!")
    



    # Add brand
    with st.form(key="my_form7"):
        st.markdown("**Brand Addition**")

        # Take brand name as user input
        add_brand = st.text_input("Enter a brand").title()

        # The subproject the brand lies under
        add_subproject = st.text_input("Enter subproject").title()

        # The project the brand lies under
        add_project = st.text_input("Enter project").title()

        # Check if the brand exists
        brand_exists = brand_df[brand_df.name.str.contains(add_brand, case=False)]
        if brand_exists.shape[0]>0:
            added_brand_id = brand_exists.id.iloc[0]
        else:
            cur.execute(f"INSERT INTO brand(name) VALUES('{add_brand}')")
            conn.commit()
            brand_df = pd.read_sql("select * from brand", con=engine)
            added_brand_id = brand_df[brand_df.name.str.contains(add_brand, case=False)].id.iloc[0]        

        # Check if the subproject exists. If doesn't exists,  insert it into subproject table
        subproject_exists = subproject_df[subproject_df.name.str.contains(add_subproject, case=False)]
        if subproject_exists.shape[0]>0:
            added_sub_id = subproject_exists.id.iloc[0]
        else:
            cur.execute(f"INSERT INTO subproject(name) VALUES('{add_subproject}')")
            conn.commit()
            subproject_df = pd.read_sql("select * from subproject", con=engine)
            added_sub_id = subproject_df[subproject_df.name.str.contains(add_subproject, case=False)].id.iloc[0]
        

        # Check if the project exists. If doesn't exists,  insert it into project table
        project_exists = project_df[project_df.name.str.contains(add_project, case=False)]
        if project_exists.shape[0]>0:
            added_project_id = project_exists.id.iloc[0]
        else:
            cur.execute(f"INSERT INTO project(name) VALUES('{add_project}')")
            conn.commit()
            project_df = pd.read_sql("select * from project", con=engine)
            added_project_id = project_df[project_df.name.str.contains(add_project, case=False)].id.iloc[0]
        
        submit_button = st.form_submit_button(label='Add Brand')
        if submit_button:
            # Execute if a sub_project is given
            if add_subproject:
                cur.execute('INSERT INTO brand_for_projects_subs(project_id, subproject_id, brand_id) VALUES(%s, %s, %s)', (added_project_id, added_sub_id, added_brand_id))
                conn.commit()
                st.success(f"Brand '{add_brand}' under subproject '{add_subproject}' under project '{add_project}' added successfully!")
            
            # Execute if a sub_project isn't given
            else:
                added_sub_id = None
                cur.execute('INSERT INTO brand_for_projects_subs(project_id, subproject_id, brand_id) VALUES(%s, %s, %s)', (added_project_id, added_sub_id, added_brand_id))
                conn.commit()
                st.success(f"Brand '{add_brand}' under project '{add_project}' added successfully!")
    


    # Add attribute
    with st.form(key="my_form8"):
        st.markdown("**Attribute Addition**")

        # Take attribute name as user input
        add_attribute = st.text_input("Enter an attribute").title()
        submit_button = st.form_submit_button(label='Add Attribute')
        if submit_button:
            # Check if the attribute already exists
            attribute_exists = attr_df[attr_df.name.str.contains(add_attribute, case=False)]
            if attribute_exists.shape[0]<1:
                cur.execute(f"INSERT INTO attribute(name) VALUES('{add_attribute}')")
                conn.commit()
                st.success(f"Attribute '{add_attribute}' added successfully!")
            else:
                st.error(f"Attribute '{add_attribute}' already exists!")