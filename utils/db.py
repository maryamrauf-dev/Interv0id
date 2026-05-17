import streamlit as st
import os
from datetime import datetime
from supabase import create_client, Client

@st.cache_resource
def init_db():
    # Allow fallback to environment variables for local testing without secrets
    url = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL", ""))
    key = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY", ""))
    if not url or not key:
        raise ValueError("Supabase credentials missing. Add SUPABASE_URL and SUPABASE_KEY to secrets.")
    return create_client(url, key)

def add_history(score, target_role):
    try:
        supabase: Client = init_db()
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        data = {
            "date": date_str,
            "score": score,
            "target_role": target_role
        }
        
        supabase.table("history").insert(data).execute()
    except Exception as e:
        print(f"Error adding to Supabase: {e}")

def get_history():
    try:
        supabase: Client = init_db()
        response = supabase.table("history").select("date, score, target_role").order("id", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching from Supabase: {e}")
        return []
