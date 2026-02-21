import streamlit as st
import pandas as pd
from data_validator import UserRecord, logging, load_to_postgres # load_to_postgres import kiya
from pydantic import ValidationError

st.title("ETL Service")

st.markdown("---") # Partition line

# --- CSV Upload Section ---
st.subheader("Bulk Upload via CSV")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.write("Preview of Uploaded Data:")
    st.dataframe(df.head())
    
    # Button ka naam thoda badal diya kyunki ab ye DB mein bhi daalega
    if st.button("Validate, Log & Push to DB"):
        records = df.to_dict(orient='records')
        
        valid_records = []  # Valid data store karne ke liye balti
        error_count = 0
        
        for i, row in enumerate(records):
            try:
                # Row validate ho rahi hai
                validated_model = UserRecord(**row)
                
                # Agar sahi hai, toh list mein add karo
                valid_records.append(validated_model.model_dump())
                logging.info(f"Row {i+1}: Validation Successful for {row.get('name')}")
                
            except ValidationError as e:
                error_count += 1
                error_msg = f"Row {i+1} Error: {e.errors()[0]['msg']}"
                st.error(error_msg)
                logging.error(error_msg)

        # --- Final Step: Database Loading ---
        if valid_records:
            with st.spinner("Inserting into Database"):
                success = load_to_postgres(valid_records) # data_validator wali file ka function
                
            if success:
                st.success(f"Woahhh! {len(valid_records)} valid records has been inserted to postgres.")
                if error_count == 0:
                    st.balloons()
        
        if error_count > 0:
            st.warning(f"Total {error_count} records are failed.")